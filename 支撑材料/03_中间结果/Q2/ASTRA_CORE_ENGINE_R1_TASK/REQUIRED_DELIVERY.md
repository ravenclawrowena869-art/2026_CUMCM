# Required Astra Delivery

Suggested delivery ZIP:

`CUMCM2026_C_Q2_ASTRA_CORE_ENGINE_R1_DELIVERY.zip`

Minimum contents:

- source code;
- configs;
- unit/integration tests;
- exact input/provenance manifest;
- solver/runtime manifest;
- canonical run command;
- canonical four-strategy slot ledger;
- daily summary;
- strategy summary;
- canonical constraint replay;
- canonical independent accounting replay;
- canonical result2 workbook;
- result2 saved-file readback evidence;
- test logs;
- runtime logs;
- implementation map: authority formula/field -> code module/function;
- `SOL_CONTINUATION_HANDOFF.md`;
- `SHA256SUMS.txt`;
- outer ZIP SHA256 and ZIP CRC result.

`SOL_CONTINUATION_HANDOFF.md` must explicitly list:

1. exact code/config revision;
2. commands to run each remaining sensitivity;
3. expected output locations;
4. any unresolved warning;
5. whether any issue requires XXT rather than FYQ;
6. which items were implemented but not fully replayed.
