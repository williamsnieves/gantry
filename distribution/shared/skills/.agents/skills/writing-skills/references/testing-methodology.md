# Testing Methodology

## Contents

1. Baseline
2. Skill-type cases
3. Discovery
4. Procedure
5. Pressure and failure
6. Refactoring
7. Release decision

## 1. Baseline

Run a representative case without the new or revised guidance.

Record:

- the observed behavior;
- skipped steps;
- rationalizations;
- missing context;
- incorrect outputs;
- unnecessary context use.

A baseline may use an isolated agent, subagent, controlled conversation, or reproducible fixture.

## 2. Skill-Type Cases

### Technique

Test application, variation, and missing information.

### Pattern

Test recognition, application, and counterexamples.

### Reference

Test retrieval, correct application, and coverage gaps.

### Discipline-Enforcing

Test understanding and compliance under combined pressure.

## 3. Discovery

Test positive, negative, and ambiguous activation independently from full execution.

## 4. Procedure

Create one case for every meaningful decision branch. Require evidence and the declared output contract.

## 5. Pressure and Failure

Test as applicable:

- time pressure;
- sunk-cost pressure;
- user requests to skip steps;
- missing inputs;
- conflicting instructions;
- unavailable tools;
- failing validation;
- unsafe actions.

## 6. Refactoring

After passing:

- add every confirmed failure as a regression;
- close only demonstrated gaps;
- rerun the full suite;
- compare context usage before and after.

## 7. Release Decision

A skill is not production-ready when:

- critical discovery cases fail;
- a safety case fails;
- a known regression returns;
- required evidence can be skipped;
- the skill claims success after failed validation.
