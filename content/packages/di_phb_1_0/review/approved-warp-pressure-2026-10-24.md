# PHB-RULE-037 — approved Warp Pressure arithmetic

Approved by the user in this conversation, 2026-10-24.

Warp Pressure has a minimum of 0. Any reduction uses
`max(0, currentWarpPressure - reduction)`, unless a future explicit rule overrides it.
After the Perils effect resolves, pressure becomes `floor(currentWarpPressure / 2)`.
Examples: 3 minus 6 becomes 0; 1 minus 1 becomes 0; further reductions at 0 remain 0.

This resolves the minimum-bound portion and confirms the post-Perils arithmetic for the
new psychic implementation. Historical profile snapshots remain unchanged.
