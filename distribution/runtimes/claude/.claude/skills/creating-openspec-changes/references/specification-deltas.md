# Specification Deltas

## Capability Mapping

Map every behavior change to an existing or new capability.

Do not create a new capability merely because a new change exists.

## Delta Types

Use the format required by the configured OpenSpec schema for:

- added behavior;
- modified behavior;
- removed behavior;
- renamed behavior where supported.

## Requirements

Requirements should describe externally meaningful or contract-level behavior.

Scenarios should make behavior observable through:

- precondition;
- action or event;
- expected result.

## Modified Behavior

When behavior changes, preserve the complete resulting requirement context required by the project's format. Do not submit an ambiguous fragment that loses existing semantics.

## Evidence and Boundaries

Base deltas on:

- accepted input;
- exploration findings;
- current main specs;
- confirmed project behavior.

Do not encode proposed technical implementation as behavioral requirements unless it is genuinely part of the contract.
