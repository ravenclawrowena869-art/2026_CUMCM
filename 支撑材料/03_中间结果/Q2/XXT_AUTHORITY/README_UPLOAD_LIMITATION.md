# Binary Upload Limitation

PR #4 requires the complete XXT authority ZIP plus directly readable key MD/JSON files.

The current ChatGPT GitHub connector used in this upload supports UTF-8 text file creation but does not expose a binary-file upload action. Therefore the complete ZIP bytes were **not** written to GitHub in this operation. The directly readable authority MD/JSON files and checksums were uploaded instead.

Current ZIP:

- file: `CUMCM2026_C_XXT_Q2_FORMAL_OPT_SPEC_R1_DELIVERY.zip`
- SHA256: `d22609f9ec0368888472945f948de66fb70669a3bc89877574fd0ab8834ea54c`
- approximate size: 44 KB

Historical ZIP hash recorded by PR #4:

`0d17f99f58ef469369c0958ee4795bb3e71553289c60b8bf6c3d225f52e7e561`

Because the hashes differ, the current package is not represented as the historical byte-identical archive. If the complete ZIP is later uploaded by Git CLI, GitHub Web, or another connector supporting binary file parameters, this document and `README.md` should be updated with its repository path and the verified SHA256.
