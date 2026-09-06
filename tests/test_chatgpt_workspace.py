from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import chatgpt_workspace  # noqa: E402
from _chatgpt_workspace import (  # noqa: E402
    Decision,
    Identity,
    LockObservation,
    Receipt,
    Status,
    build_publication_plan,
    classify_acquisition,
    classify_gc,
    classify_release,
    classify_write_entry,
    create_snapshot,
    validate_snapshot,
    verify_release,
)
from _chatgpt_workspace.git_state import GitInspectionError  # noqa: E402

SHA_A = "a" * 40
SHA_B = "b" * 40
IDENTITY = Identity("ManuelBouza/agent-governance", "chat-1", "T058", "feat/t058")


def git(repository: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def repository(tmp_path: Path) -> tuple[Path, str, str]:
    root = tmp_path / "source"
    root.mkdir()
    git(root, "init", "-b", "feat/t058")
    git(root, "config", "user.name", "T058 Test")
    git(root, "config", "user.email", "t058@example.invalid")
    (root / "one.txt").write_text("one\n", encoding="utf-8")
    git(root, "add", "one.txt")
    git(root, "commit", "-m", "fixture")
    return root, git(root, "rev-parse", "HEAD"), git(root, "rev-parse", "HEAD^{tree}")


def receipt(head: str, tree: str) -> Receipt:
    return Receipt(
        schema="chatgpt-portable-workspace/v1",
        repository=IDENTITY.repository,
        owner=IDENTITY.owner,
        work_unit=IDENTITY.work_unit,
        topic_branch=IDENTITY.topic_branch,
        target_branch="develop",
        remote_head_sha=head,
        remote_tree_sha=tree,
        local_snapshot_head_sha=head,
        local_snapshot_tree_sha=tree,
        working_tree_clean=True,
        lock_branch="coordination/chatgpt-workspaces",
    )


def lock(
    *, present: bool = True, owner: str = IDENTITY.owner, observed: str = SHA_A
) -> LockObservation:
    return LockObservation(
        expected_lock_head=SHA_A,
        observed_lock_head=observed,
        sentinel_present=present,
        repository=IDENTITY.repository if present else None,
        owner=owner if present else None,
        work_unit=IDENTITY.work_unit if present else None,
        topic_branch=IDENTITY.topic_branch if present else None,
        state="ACTIVE" if present else None,
        sentinel_blob_sha=SHA_B if present else None,
    )


def valid_snapshot(tmp_path: Path) -> tuple[Decision, str, str]:
    root, head, tree = repository(tmp_path)
    archive = tmp_path / "snapshot.tar.gz"
    checksum = create_snapshot(root, receipt(head, tree), archive)
    result = validate_snapshot(
        archive,
        tmp_path / "extracted",
        expected_archive_sha256=checksum,
        expected_identity=IDENTITY,
        expected_remote_head=head,
        expected_remote_tree=tree,
        require_remote_tree_equivalence=True,
    )
    return result, head, tree


def test_full_snapshot_round_trip(tmp_path: Path) -> None:
    result, head, tree = valid_snapshot(tmp_path)
    assert result.status is Status.SNAPSHOT_VALID
    assert result.details["local_head"] == head
    assert result.details["local_tree"] == tree
    assert (Path(result.details["repository_path"]) / ".git").is_dir()


def test_matching_identity_and_freshness_allow_write(tmp_path: Path) -> None:
    snapshot, head, tree = valid_snapshot(tmp_path)
    result = classify_write_entry(
        snapshot,
        expected_identity=IDENTITY,
        lock_observation=lock(),
        observed_remote_head=head,
        observed_remote_tree=tree,
        require_tree_equivalence=True,
    )
    assert result.status is Status.WRITE_ALLOWED


def test_wrong_worktree_receipt_is_blocked(tmp_path: Path) -> None:
    root, head, tree = repository(tmp_path)
    wrong = receipt(head, tree)
    wrong = Receipt(**{**wrong.as_dict(), "work_unit": "T999"})
    archive = tmp_path / "wrong.tar.gz"
    checksum = create_snapshot(root, wrong, archive)
    result = validate_snapshot(
        archive,
        tmp_path / "out",
        expected_archive_sha256=checksum,
        expected_identity=IDENTITY,
        expected_remote_head=head,
        expected_remote_tree=tree,
    )
    assert result.status is Status.BLOCKED_IDENTITY_MISMATCH


@pytest.mark.parametrize("bad_checksum", ["0" * 64, "not-a-sha"])
def test_corrupt_or_invalid_checksum_fails_before_qualification(
    tmp_path: Path, bad_checksum: str
) -> None:
    root, head, tree = repository(tmp_path)
    archive = tmp_path / "snapshot.tar.gz"
    create_snapshot(root, receipt(head, tree), archive)
    result = validate_snapshot(
        archive,
        tmp_path / "extracted",
        expected_archive_sha256=bad_checksum,
        expected_identity=IDENTITY,
        expected_remote_head=head,
        expected_remote_tree=tree,
    )
    assert result.status is Status.BLOCKED_INVALID_SNAPSHOT
    assert not (tmp_path / "extracted").exists()


@pytest.mark.parametrize(
    "name", ["../escaped", "repository/../../escaped", "..\\escaped", "C:/escaped"]
)
def test_unsafe_archive_paths_are_rejected(tmp_path: Path, name: str) -> None:
    archive = tmp_path / "unsafe.tar.gz"
    with tarfile.open(archive, "w:gz") as bundle:
        directory = tarfile.TarInfo("repository")
        directory.type = tarfile.DIRTYPE
        bundle.addfile(directory)
        receipt_info = tarfile.TarInfo("receipt.json")
        receipt_info.size = 2
        bundle.addfile(receipt_info, io.BytesIO(b"{}"))
        bad = tarfile.TarInfo(name)
        bad.size = 1
        bundle.addfile(bad, io.BytesIO(b"x"))
    result = validate_snapshot(
        archive,
        tmp_path / "out",
        expected_archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
        expected_identity=IDENTITY,
        expected_remote_head=SHA_A,
        expected_remote_tree=SHA_B,
    )
    assert result.status is Status.BLOCKED_INVALID_SNAPSHOT
    assert not (tmp_path / "escaped").exists()


@pytest.mark.parametrize("link_type", [tarfile.SYMTYPE, tarfile.LNKTYPE])
def test_archive_links_are_rejected(tmp_path: Path, link_type: bytes) -> None:
    archive = tmp_path / "link.tar.gz"
    with tarfile.open(archive, "w:gz") as bundle:
        root = tarfile.TarInfo("repository")
        root.type = tarfile.DIRTYPE
        bundle.addfile(root)
        receipt_info = tarfile.TarInfo("receipt.json")
        receipt_info.size = 2
        bundle.addfile(receipt_info, io.BytesIO(b"{}"))
        link = tarfile.TarInfo("repository/link")
        link.type = link_type
        link.linkname = "../../escaped"
        bundle.addfile(link)
    result = validate_snapshot(
        archive,
        tmp_path / "out",
        expected_archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
        expected_identity=IDENTITY,
        expected_remote_head=SHA_A,
        expected_remote_tree=SHA_B,
    )
    assert result.status is Status.BLOCKED_INVALID_SNAPSHOT


def test_archive_without_git_repository_is_invalid(tmp_path: Path) -> None:
    archive = tmp_path / "not-git.tar.gz"
    receipt_bytes = json.dumps(receipt(SHA_A, SHA_B).as_dict()).encode()
    with tarfile.open(archive, "w:gz") as bundle:
        root = tarfile.TarInfo("repository")
        root.type = tarfile.DIRTYPE
        bundle.addfile(root)
        ordinary = tarfile.TarInfo("repository/file.txt")
        ordinary.size = 1
        bundle.addfile(ordinary, io.BytesIO(b"x"))
        receipt_info = tarfile.TarInfo("receipt.json")
        receipt_info.size = len(receipt_bytes)
        bundle.addfile(receipt_info, io.BytesIO(receipt_bytes))
    result = validate_snapshot(
        archive,
        tmp_path / "out",
        expected_archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
        expected_identity=IDENTITY,
        expected_remote_head=SHA_A,
        expected_remote_tree=SHA_B,
    )
    assert result.status is Status.BLOCKED_INVALID_SNAPSHOT


def test_acquisition_matching_absence_allowed_but_existing_owner_blocks() -> None:
    assert classify_acquisition(lock(present=False)).status is Status.ACQUIRE_ALLOWED
    assert classify_acquisition(lock()).status is Status.BLOCKED_OWNER_EXISTS


def test_unknown_sentinel_state_is_ambiguous() -> None:
    observation = LockObservation(**{**lock().__dict__, "state": "UNKNOWN"})
    assert classify_acquisition(observation).status is Status.BLOCKED_AMBIGUOUS_LOCK


def test_stale_lock_head_wins_without_retry_or_transition() -> None:
    result = classify_acquisition(lock(present=False, observed=SHA_B))
    assert result.status is Status.BLOCKED_STALE_LOCK_HEAD


def test_wrong_owner_blocks_write_entry(tmp_path: Path) -> None:
    snapshot, head, _ = valid_snapshot(tmp_path)
    result = classify_write_entry(
        snapshot,
        expected_identity=IDENTITY,
        lock_observation=lock(owner="other-chat"),
        observed_remote_head=head,
    )
    assert result.status is Status.WRITE_BLOCKED
    assert result.reason == Status.BLOCKED_IDENTITY_MISMATCH.value


def test_target_branch_mismatch_blocks_snapshot(tmp_path: Path) -> None:
    root, head, tree = repository(tmp_path)
    wrong = Receipt(**{**receipt(head, tree).as_dict(), "target_branch": "main"})
    archive = tmp_path / "wrong-target.tar.gz"
    checksum = create_snapshot(root, wrong, archive)
    result = validate_snapshot(
        archive,
        tmp_path / "out",
        expected_archive_sha256=checksum,
        expected_identity=IDENTITY,
        expected_remote_head=head,
        expected_remote_tree=tree,
    )
    assert result.status is Status.BLOCKED_IDENTITY_MISMATCH


@pytest.mark.parametrize("protected_branch", ["develop", "main"])
def test_protected_branch_never_qualifies_for_write_or_publication(
    tmp_path: Path, protected_branch: str
) -> None:
    root, head, tree = repository(tmp_path)
    git(root, "branch", "-m", protected_branch)
    protected_identity = Identity(
        IDENTITY.repository, IDENTITY.owner, IDENTITY.work_unit, protected_branch
    )
    protected_receipt = Receipt(
        **{
            **receipt(head, tree).as_dict(),
            "topic_branch": protected_branch,
        }
    )
    snapshot = Decision(
        Status.SNAPSHOT_VALID,
        "synthetic protected-branch snapshot",
        {"receipt": protected_receipt.as_dict()},
    )
    protected_lock = LockObservation(
        **{
            **lock().__dict__,
            "topic_branch": protected_branch,
        }
    )
    write = classify_write_entry(
        snapshot,
        expected_identity=protected_identity,
        lock_observation=protected_lock,
        observed_remote_head=head,
    )
    assert write.status is Status.WRITE_BLOCKED
    assert write.reason == Status.BLOCKED_IDENTITY_MISMATCH.value

    publication = build_publication_plan(
        root,
        repository=IDENTITY.repository,
        work_unit=IDENTITY.work_unit,
        topic_branch=protected_branch,
        expected_remote_head=head,
        changed_paths=["one.txt"],
    )
    assert publication.status is Status.BLOCKED_IDENTITY_MISMATCH


def test_stale_remote_head_blocks_even_when_tree_matches(tmp_path: Path) -> None:
    snapshot, _, tree = valid_snapshot(tmp_path)
    result = classify_write_entry(
        snapshot,
        expected_identity=IDENTITY,
        lock_observation=lock(),
        observed_remote_head=SHA_A,
        observed_remote_tree=tree,
        require_tree_equivalence=True,
    )
    assert result.reason == Status.BLOCKED_STALE_BASE.value


def test_invalid_snapshot_can_never_enter_write_mode() -> None:
    result = classify_write_entry(
        Decision(Status.BLOCKED_INVALID_SNAPSHOT, "corrupt"),
        expected_identity=IDENTITY,
        lock_observation=lock(),
        observed_remote_head=SHA_A,
    )
    assert result.status is Status.WRITE_BLOCKED
    assert result.reason == Status.BLOCKED_INVALID_SNAPSHOT.value


def test_release_requires_exact_owner_and_blob_and_verifies_absence() -> None:
    allowed = classify_release(lock(), IDENTITY, SHA_B)
    assert allowed.status is Status.RELEASE_ALLOWED
    assert allowed.details["sentinel_blob_sha"] == SHA_B
    assert (
        classify_release(lock(owner="other"), IDENTITY, SHA_B).status
        is Status.BLOCKED_IDENTITY_MISMATCH
    )
    assert classify_release(lock(), IDENTITY, SHA_A).status is Status.BLOCKED_STALE_LOCK_HEAD
    assert verify_release(lock(present=False)).status is Status.RELEASED
    assert verify_release(lock()).status is Status.BLOCKED_OWNER_EXISTS


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ((True, True, True, True, True, True), Status.GC_ELIGIBLE),
        ((False, True, False, False, False, False), Status.RETAIN_CLOSED_UNMERGED),
        ((False, False, False, False, False, False), Status.RETAIN_ACTIVE),
        ((True, True, True, False, True, True), Status.RETAIN_INVALID_TARGET_SNAPSHOT),
        ((True, True, None, True, True, True), Status.RETAIN_AMBIGUOUS),
    ],
)
def test_gc_is_fail_closed(values: tuple[bool | None, ...], expected: Status) -> None:
    result = classify_gc(
        merged=values[0],
        closed=values[1],
        integration_verified=values[2],
        target_snapshot_validated=values[3],
        target_snapshot_promoted=values[4],
        target_snapshot_revalidated=values[5],
    )
    assert result.status is expected


def test_publish_manifest_batches_sorted_unique_paths(tmp_path: Path) -> None:
    root, head, _ = repository(tmp_path)
    plan = build_publication_plan(
        root,
        repository=IDENTITY.repository,
        work_unit=IDENTITY.work_unit,
        topic_branch=IDENTITY.topic_branch,
        expected_remote_head=head,
        changed_paths=["z.txt", "a.txt", "z.txt"],
    )
    assert plan.status is Status.PUBLICATION_PLAN_READY
    assert plan.details["changed_paths"] == ["a.txt", "z.txt"]
    assert "published" not in plan.details


def test_git_inspection_invokes_only_local_read_commands(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, head, _ = repository(tmp_path)
    original_run = subprocess.run
    observed: list[tuple[list[str], dict[str, str]]] = []

    def recording_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        observed.append((command, kwargs["env"]))  # type: ignore[arg-type]
        return original_run(command, **kwargs)

    monkeypatch.setenv("GIT_DIR", str(tmp_path / "redirected.git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(tmp_path / "redirected-worktree"))
    monkeypatch.setenv("GIT_ALTERNATE_OBJECT_DIRECTORIES", str(tmp_path / "objects"))
    monkeypatch.setattr(subprocess, "run", recording_run)
    plan = build_publication_plan(
        root,
        repository=IDENTITY.repository,
        work_unit=IDENTITY.work_unit,
        topic_branch=IDENTITY.topic_branch,
        expected_remote_head=head,
        changed_paths=["one.txt"],
    )
    assert plan.status is Status.PUBLICATION_PLAN_READY
    joined = [" ".join(command) for command, _ in observed]
    assert all(
        not any(word in command for word in (" fetch ", " push ", " remote ")) for command in joined
    )
    assert all(environment["GIT_NO_LAZY_FETCH"] == "1" for _, environment in observed)
    assert all("GIT_DIR" not in environment for _, environment in observed)
    assert all("GIT_WORK_TREE" not in environment for _, environment in observed)
    assert all("GIT_ALTERNATE_OBJECT_DIRECTORIES" not in environment for _, environment in observed)
    assert len(observed) == 5


def test_git_inspection_rejects_external_object_alternates(tmp_path: Path) -> None:
    root, head, _ = repository(tmp_path)
    alternates = root / ".git" / "objects" / "info" / "alternates"
    alternates.write_text(str(tmp_path / "external-objects"), encoding="utf-8")
    with pytest.raises(GitInspectionError, match="external Git object directory"):
        build_publication_plan(
            root,
            repository=IDENTITY.repository,
            work_unit=IDENTITY.work_unit,
            topic_branch=IDENTITY.topic_branch,
            expected_remote_head=head,
            changed_paths=["one.txt"],
        )


def test_cli_safety_block_is_structured_and_nonzero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text(
        json.dumps(
            {
                "expected_lock_head": SHA_A,
                "observed_lock_head": SHA_B,
                "sentinel_present": False,
            }
        ),
        encoding="utf-8",
    )
    assert chatgpt_workspace.main(["classify-lock", "--input", str(input_path)]) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == Status.BLOCKED_STALE_LOCK_HEAD.value
