# Failure Handoff

A good validator handoff enables correction without repeating the entire investigation.

## Required Fields

- check name;
- exact command;
- working directory;
- exit code;
- relevant output;
- failure classification;
- affected files or module;
- baseline evidence;
- likely correction boundary;
- checks invalidated by a future fix;
- required rerun sequence.

## Introduced Failure

Route to implementation with the smallest supported diagnosis.

## Pre-Existing Failure

Report separately. State whether repository policy treats it as blocking.

## Environmental Failure

Route to the environment owner with exact prerequisites.

## Unknown Failure

Do not assign blame. Provide evidence and the minimum next experiment needed.

## Flaky Failure

Require repeated or historical evidence. Include run count and observed variance.
