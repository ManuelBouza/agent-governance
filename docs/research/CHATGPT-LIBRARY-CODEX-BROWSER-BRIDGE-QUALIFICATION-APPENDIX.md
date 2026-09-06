# R017 Appendix — Codex browser to ChatGPT Library bridge qualification

Research-ID: R017 (supporting appendix)  
Status: QUALIFIED / NON_NORMATIVE  
Opened: 2026-09-06  
Last-Reviewed: 2026-09-06  
Owner: ChatGPT Orchestrator  
Parent-Research: `docs/research/CHATGPT-LIBRARY-ONLY-DOCUMENT-GOVERNANCE-AND-CODEX-BRIDGE-RESEARCH.md`  
Decision-Ref: none

## Provenance note

The empirical probe was executed before the final research ID was reallocated from provisional R016 to canonical R017 because another concurrent workstream had already integrated the canonical R016 into `develop`.

Therefore historical fixture values such as:

`probe_id=R016-CODEX-BRIDGE-20260906`

are preserved exactly as executed. They are test identifiers, not the canonical research identifier.

## Purpose

Qualify the browser-mediated path:

```text
Codex Desktop
-> authenticated ChatGPT Library web UI
-> exact Library-only object lookup
-> download
-> local Codex workspace
-> local byte/hash/content verification
```

without using GitHub for the documentary payload.

## Blind fixture

Library namespace:

`/r016-codex-bridge-qualification/`

Payload:

`library_codex_bridge_probe.txt`

Receipt:

`library_codex_bridge_probe.receipt.json`

The Orchestrator retained the receipt and intentionally did not disclose its hash to Codex.

Expected identity:

```text
probe_id: R016-CODEX-BRIDGE-20260906
size_bytes: 261
sha256: 267151f5095d1c7a303fe5dc172548e2dc2d992d12114861e403bd0374d0a95e
expected_phrase: CODEX-LIBRARY-BRIDGE-OK
github_payload_allowed: false
```

Exact payload:

```text
R016 CODEX LIBRARY BRIDGE PROBE
probe_id=R016-CODEX-BRIDGE-20260906
expected_phrase=CODEX-LIBRARY-BRIDGE-OK
purpose=Verify Codex can retrieve this exact Library-resident object through a browser/download bridge without using GitHub for the documentary payload.
```

Before the Codex run, the Orchestrator independently materialized the Library object and confirmed 261 bytes and the SHA-256 above.

## Codex procedure

A fresh Codex Desktop chat was instructed to:

1. use no GitHub;
2. use no chat attachment fallback;
3. use no prior-conversation information;
4. open the browser and reach ChatGPT Library;
5. find exactly `library_codex_bridge_probe.txt`;
6. download that file only;
7. not access any `.receipt.json` file;
8. calculate local byte size and SHA-256;
9. read exact local content;
10. make no modification and perform no upload-back.

The expected SHA-256 was not included in the Codex prompt.

## Codex result

Codex reported:

```text
R016_CODEX_LIBRARY_BRIDGE: PASS
RETRIEVAL_METHOD: Navegador integrado de Codex -> ChatGPT Library -> búsqueda exacta -> descarga
LIBRARY_UI_REACHED: YES
FILE_FOUND_IN_LIBRARY: YES
DOWNLOAD_SUCCEEDED: YES
LOCAL_PATH: C:\Users\Manuel\Documents\Codex\2026-09-06\estamos-realizando-una-prueba-emp-rica\library_codex_bridge_probe.txt
SIZE_BYTES: 261
SHA256: 267151F5095D1C7A303FE5DC172548E2DC2D992D12114861E403BD0374D0A95E
GITHUB_USED: NO
RECEIPT_FILE_USED: NO
ERROR: <empty>
```

Codex returned the exact payload text.

## Independent comparison

```text
size:
expected 261
observed 261
MATCH

sha256:
expected 267151f5095d1c7a303fe5dc172548e2dc2d992d12114861e403bd0374d0a95e
observed 267151F5095D1C7A303FE5DC172548E2DC2D992D12114861E403BD0374D0A95E
MATCH

content:
MATCH exact

GitHub payload retrieval:
NO

receipt disclosure/use:
NO
```

The fixture and receipt remained in Library after the test for independent post-run verification.

## Result

`PASS`

Current status:

`EMPIRICALLY VERIFIED / VERSION_AND_SURFACE_SENSITIVE`

for the tested ChatGPT Library web UI and Codex Desktop/browser surface on 2026-09-06.

## Bounded conclusion

Codex can consume an exact Library-only documentary object without the payload residing in GitHub by using browser-mediated retrieval and then operate on the downloaded local file.

This test does **not** establish a native Codex Library filesystem mount/source.

The reverse path remains unqualified:

```text
Codex local workspace
-> authenticated Library UI
-> create new immutable uniquely named Library object
-> Orchestrator rediscovery
-> independent hash verification
```

That upload-back path requires a separate empirical test because Library duplicate naming, object identity, and overwrite semantics are materially different from download.

## Capability delta

| Capability | Status |
| --- | --- |
| Codex reaches authenticated ChatGPT Library UI | VERIFIED |
| exact Library file search by name | VERIFIED |
| Library -> Codex browser download | VERIFIED |
| downloaded byte identity | VERIFIED |
| downloaded SHA-256 identity | VERIFIED |
| downloaded text identity | VERIFIED |
| payload retrieved without GitHub | VERIFIED |
| blind verification without receipt use | VERIFIED |
| native Codex Library mount/source | NOT VERIFIED / NOT CLAIMED |
| Codex -> Library immutable upload-back | NOT VERIFIED |
| automatic Library-only multi-chat mutex | NOT QUALIFIED |

## Disposition

R017 remains:

```text
Research-State: COMPLETE
Decision-State: NOT_REQUIRED
```

This appendix adds empirical evidence only and does not adopt a normative Library-only adapter.