# Validator Decision Policy

## PASS

Return `PASS` only when:

- every applicable blocking check ran;
- every blocking check passed;
- generated and schema consistency checks pass when applicable;
- no unresolved introduced failure remains;
- no mandatory check is omitted.

## CONDITIONAL PASS

Use only when project policy explicitly permits it.

Examples may include:

- documented non-blocking platform-specific check delegated to CI;
- known pre-existing non-blocking failure with accepted ownership;
- environment-dependent check covered by an approved external gate.

Required report fields:

- policy evidence;
- missing or failing check;
- owner;
- external gate;
- residual risk.

## FAIL

Return `FAIL` when:

- any blocking check fails;
- a mandatory check cannot run;
- validation configuration was weakened;
- command discovery is incomplete;
- failure ownership cannot be established and risk is blocking;
- required generated output or schemas drift;
- the available evidence is insufficient for a completion claim.

## Rule

When uncertain between pass and fail, do not invent confidence. Return fail or incomplete validation with the exact missing evidence.
