# Q4-2 Formal Dependency Gate R1

Formal execution requires all of the following before the strategy runner is called:

1. Q4 common contract status is `LOCKED_BY_XXT` and is not marked test-only.
2. Q2 upstream SHA256 is valid and exactly equals the Controller-approved final Q2 artifact SHA256.
3. Official result4-2 writer mapping is locked.
4. Dynamic-price `known_at` audit passes in `FORMAL_CAUSAL` lane.

If any item fails, Q4-2 stays `BLOCKED_BY_DEPENDENCIES` and no formal result workbook may be emitted.
