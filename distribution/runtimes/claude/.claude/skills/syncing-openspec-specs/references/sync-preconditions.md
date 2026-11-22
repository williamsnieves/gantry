# Sync Preconditions

Do not synchronize merely because implementation appears complete.

## Required Preconditions

Confirm:

- the target change exists and is active or awaiting archival;
- its delta specs are syntactically valid;
- its behavioral intent is approved;
- material editing is complete;
- relevant tasks and verification state are understood;
- the correct main specs are available;
- no unresolved decision changes the resulting behavior.

## Return to Editing

Return to `editing-openspec-changes` when:

- requirements remain ambiguous;
- delta semantics contradict proposal or design;
- implementation feedback requires revising the change;
- task status reveals missing behavioral work;
- the change should be split or replaced.

## Implementation Evidence

Implementation evidence may confirm drift, but code does not automatically override approved specifications.

When code and specs disagree, establish the approved source of truth before synchronization.
