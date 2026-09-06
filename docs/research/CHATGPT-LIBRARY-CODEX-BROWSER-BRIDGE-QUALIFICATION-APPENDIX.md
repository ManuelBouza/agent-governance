# R016 Appendix — Codex browser to ChatGPT Library bridge qualification

Research-ID: R016 (supporting appendix)  
Status: QUALIFIED / NON_NORMATIVE  
Opened: 2026-09-06  
Last-Reviewed: 2026-09-06  
Owner: ChatGPT Orchestrator  
Parent-Research: `docs/research/CHATGPT-LIBRARY-ONLY-DOCUMENT-GOVERNANCE-AND-CODEX-BRIDGE-RESEARCH.md`  
Decision-Ref: none

## Purpose

R016 identified a plausible but unqualified bridge from Codex Desktop to ChatGPT Library using Codex's browser surface: authenticated ChatGPT Library web UI -> exact file lookup -> download -> local Codex workspace -> local identity verification.

This appendix records a direct blind qualification of that bridge.

## Test fixture

The ChatGPT Orchestrator created a Library-only fixture without placing the documentary payload in GitHub:

```text
Library folder:
/r016-codex-bridge-qualification

payload:
library_codex_bridge_probe.txt

receipt:
library_codex_bridge_probe.receipt.json
```

Payload metadata independently held by the Orchestrator:

```text
probe_id: R016-CODEX-BRIDGE-20260906
size_bytes: 261
sha256: 267151f5095d1c7a303fe5dc172548e2dc2d992d12114861e403bd0374d0a95e
expected_phrase: CODEX-LIBRARY-BRIDGE-OK
github_payload_allowed: false
```

The receipt was stored separately and Codex was explicitly instructed not to open or use it.

Payload content:

```text
R016 CODEX LIBRARY BRIDGE PROBE
probe_id=R016-CODEX-BRIDGE-20260906
expected_phrase=CODEX-LIBRARY-BRIDGE-OK
purpose=Verify Codex can retrieve this exact Library-resident object through a browser/download bridge without using GitHub for the documentary payload.
```

Before the external Codex run, the Orchestrator materialized the Library object locally and independently confirmed the same 261-byte size and SHA-256 above.

## Codex procedure

A fresh Codex Desktop chat received a blind procedure requiring:

1. no GitHub;
2. no chat attachment fallback;
3. no prior-conversation information;
4. browser access to ChatGPT Library;
5. exact lookup of `library_codex_bridge_probe.txt`;
6. download of that file only;
7. no access to the `.receipt.json` file;
8. local filesystem SHA-256 and byte-size calculation;
9. local content read;
10. no modification or upload-back.

The expected SHA-256 was intentionally not disclosed to Codex.

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

Codex also returned the exact payload text shown above.

## Independent comparison

The Orchestrator compared the Codex result against the undisclosed receipt:

```text
size:
expected 261
observed 261
MATCH

sha256:
expected 267151f5095d1c7a303fe5dc172548e2dc2d992d12114861e403bd0374d0a95e
observed 267151F5095D1C7A303FE5DC172548E2DC2D992D12114861E403BD0374D0A95E
MATCH (case-insensitive hexadecimal representation)

content:
MATCH exact text

GitHub payload path:
NOT USED

receipt disclosure:
NOT USED
```

The Library fixture and receipt remained present after the test, allowing independent post-run verification.

## Qualification result

`PASS`

The previously unqualified bridge:

```text
Codex Desktop
-> browser
-> authenticated ChatGPT Library web UI
-> exact object lookup
-> download
-> local Codex filesystem
-> local SHA-256/content verification
```

is now:

`EMPIRICALLY VERIFIED / VERSION_AND_SURFACE_SENSITIVE`

for the tested account, Codex Desktop/browser surface, and ChatGPT Library web UI on 2026-09-06.

## Bounded conclusion

This test proves that Codex can consume a Library-only documentary object without the payload being present in GitHub by using browser-mediated retrieval.

It does **not** prove a native Codex filesystem mount or first-party Library source. The mechanism remains browser/UI mediated.

It also does not yet qualify the reverse path:

```text
Codex local workspace
-> browser/UI
-> create immutable Library object
-> Orchestrator discovers exact new object
-> independently verifies hash/receipt
```

That upload-back path requires its own test because Library duplicate naming, overwrite behavior, identity discovery, and promotion semantics are materially different from download.

## Updated capability delta

| Capability | Status | Evidence |
| --- | --- | --- |
| Codex reaches authenticated ChatGPT Library UI | VERIFIED | R016 bridge probe |
| exact Library file search by name | VERIFIED | probe file found |
| Library -> Codex browser download | VERIFIED | download succeeded |
| downloaded byte identity | VERIFIED | 261 bytes + exact SHA-256 |
| downloaded text identity | VERIFIED | exact content match |
| payload retrieved without GitHub | VERIFIED | Codex reported `GITHUB_USED: NO` and fixture was Library-only |
| blind verification without receipt disclosure | VERIFIED | `RECEIPT_FILE_USED: NO`; expected hash withheld |
| native Codex Library mount/source | NOT VERIFIED / NOT CLAIMED | browser-mediated path only |
| Codex -> Library immutable upload-back | NOT VERIFIED | next qualification |
| automatic Library-only multi-chat mutex | NOT QUALIFIED | parent R016 finding unchanged |

## Disposition

R016 remains:

```text
Research-State: COMPLETE
Decision-State: NOT_REQUIRED
```

This appendix adds empirical qualification evidence only. It does not itself adopt a normative Library-only adapter.