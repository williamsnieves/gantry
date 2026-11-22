---
name: extracting-domain-model-from-legacy-code
description: Portable engineering capability `extracting-domain-model-from-legacy-code`.
  Use when the harness or a specialist agent explicitly requires this named capability.
---
# Extracting Domain Model From Legacy Code

## Purpose

Discover the business model already implied by an existing backend before moving behavior toward the target architecture.

The skill must:

- discover existing business invariants;
- separate transport and persistence logic;
- identify candidate Entities and Value Objects;
- identify candidate Domain Services and Domain errors;
- distinguish true Domain concepts from technical artifacts;
- expose contradictions and missing product decisions;
- produce a modeling proposal before refactoring.

This is a discovery and proposal skill.

It does not modify production code.

## Use When

- Business rules are spread across controllers, services, ORM hooks, jobs, database constraints, or provider adapters.
- A legacy service mixes business, persistence, transport, and integration logic.
- A brownfield refactor needs a credible Domain model first.
- Existing tables appear to represent business state but ownership is unclear.
- Several code paths implement similar decisions differently.
- State transitions are implicit in conditionals or status fields.
- The team needs to determine which concepts deserve Entity, Value Object, Domain Service, or Application ownership.
- Incidents or production behavior reveal rules missing from documentation.
- `adapting-backend-rules-to-existing-code` or `refactoring-backend-toward-hexagonal-architecture` has requested Domain extraction.

## Do Not Use When

- The Domain model is already accepted and only implementation is needed.
- The task is greenfield Domain design from requirements.
- The task is to refactor legacy code immediately.
- The only evidence available is a database schema with no behavior context.
- Product decisions are missing and the proposed model would require guessing.
- The request is only architecture or code review.
- The task is to rename ORM records as Entities.
- The user wants a complete repository-wide model in one pass.

## Inputs

- Selected legacy behavior or capability.
- Current runtime path.
- Controllers, services, jobs, consumers, and scheduled processes.
- ORM models, database constraints, migrations, queries, and stored data examples.
- Provider adapters and external contracts.
- Existing tests and fixtures.
- Public API/event contracts.
- Logs, metrics, incidents, and operational runbooks when available.
- Product documentation and domain terminology.
- Brownfield adaptation record.
- Repository-local `AGENTS.md`.
- Definitive backend standard.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the selected behavior and brownfield scope.
3. Trace every known entry point for the behavior.
4. Inspect all decision-making code in scope.
5. Inspect persistence constraints, statuses, migrations, and data examples.
6. Inspect provider semantics only to separate technical state from business meaning.
7. Inspect tests, incidents, and public contracts for observed behavior.
8. Identify contradictory implementations and terminology.
9. Record evidence source and confidence for every candidate rule.
10. Do not infer an invariant solely because a column is non-null or an enum exists.

## Outputs

- Domain discovery scope.
- Ubiquitous-language glossary.
- Behavior and decision inventory.
- State-transition inventory.
- Invariant candidates with evidence and confidence.
- Candidate Entities.
- Candidate Value Objects.
- Candidate Domain Services.
- Candidate Domain errors and semantic outcomes.
- Repository concept proposal.
- Technical and compatibility concepts explicitly excluded from Domain.
- Contradictions and unresolved product questions.
- Domain modeling proposal.
- Domain extraction record.

## Core Workflow

```text
select one legacy behavior
→ gather evidence
→ trace decisions and state transitions
→ separate technical concerns
→ identify invariant candidates
→ propose Domain concepts
→ challenge the proposal
→ record confidence and decisions required
→ hand off to focused modeling skills
```

## Unit of Discovery

Use one coherent behavior or capability.

Good:

```text
Apply, expire, and revoke a campaign promotion on a subscription
```

Too broad:

```text
Discover the entire commerce Domain
```

A capability may require several related behaviors when they share identity and lifecycle.

Do not model unrelated modules together merely because they use the same database.

## Readiness Gate

Use one:

```text
READY_TO_EXTRACT_DOMAIN_MODEL
READY_WITH_CONDITIONS
BEHAVIOR_SCOPE_REQUIRED
CURRENT_BEHAVIOR_EVIDENCE_REQUIRED
DOMAIN_TERMINOLOGY_REQUIRED
PRODUCT_DECISION_REQUIRED
DATA_EVIDENCE_REQUIRED
BLOCKED
```

Stop when:

- the selected behavior is unclear;
- evidence sources contradict each other and no decision owner is available;
- current behavior cannot be observed;
- security or tenant behavior is unknown;
- persisted states cannot be interpreted safely;
- the only available input is implementation naming without behavioral evidence.

## Evidence Sources

Rank sources according to the question being answered.

Potential sources:

1. accepted product behavior and explicit business documentation;
2. executable tests that assert observable outcomes;
3. public API/event contracts;
4. database constraints and persisted history;
5. production-safe incidents, logs, and metrics;
6. code paths and conditionals;
7. provider contracts;
8. names, comments, and file structure.

Names are weak evidence.

A database constraint may prove an authoritative restriction but not necessarily explain its business meaning.

## Evidence Record

For every candidate rule, record:

- statement;
- source;
- exact behavior or code path;
- whether it is explicit or inferred;
- counterexamples;
- confidence;
- decision owner;
- impact if wrong.

Use confidence:

```text
HIGH
MEDIUM
LOW
```

## Behavior Inventory

Describe each behavior as:

```text
trigger
→ actor/context
→ preconditions
→ business decision
→ state transition
→ durable effect
→ external effect
→ semantic outcome
```

Example:

```text
owner requests campaign application
→ same-tenant subscription
→ campaign active and subscription eligible
→ promotion becomes pending
→ provider command issued
→ promotion becomes applied or remains pending for reconciliation
```

Do not include HTTP status or SDK response codes as the business decision.

## Decision Mining

Search for decision points in:

- `if` and `switch` branches;
- guard clauses;
- thrown errors;
- status assignments;
- database constraints;
- transaction boundaries;
- retry and duplicate handling;
- scheduled jobs;
- reconciliation logic;
- authorization checks;
- provider result mapping;
- tests and fixtures.

For each decision ask:

- What business question is being answered?
- What information is required?
- Who owns the decision?
- What state may change?
- What must remain true before and after?

## Separating Concerns

Classify discovered logic as:

```text
DOMAIN_RULE
APPLICATION_ORCHESTRATION
PERSISTENCE_MECHANIC
PROVIDER_PROTOCOL
DELIVERY_CONCERN
COMPATIBILITY_RULE
SECURITY_POLICY
UNKNOWN
```

### Domain Rule

Business meaning independent of framework, database, provider, and transport.

### Application Orchestration

Sequence, authorization coordination, repository/provider invocation, transaction and idempotency policy.

### Persistence Mechanic

ORM mapping, SQL constraints, locks, pagination, generated IDs, storage encoding.

### Provider Protocol

HTTP statuses, SDK types, provider retry headers, credential and account selection.

### Delivery Concern

Request parsing, authentication extraction, HTTP status/body/headers.

### Compatibility Rule

Legacy status, old response shape, migration mapping, version behavior.

### Security Policy

Tenant isolation and authorization may influence the Domain/Application design but must be modeled from accepted policy rather than inferred casually.

## Invariant Candidates

An invariant is a rule that must remain true for the Domain concept.

Candidate examples:

- a Promotion cannot be applied after expiry;
- an applied Promotion cannot be applied again;
- a Campaign date range must be valid;
- a subscription can have at most one Promotion for a campaign;
- a revoked Promotion cannot return to active without an accepted transition.

Validate whether the rule is:

```text
CREATION_INVARIANT
STATE_TRANSITION_INVARIANT
CROSS_ENTITY_INVARIANT
TEMPORAL_INVARIANT
UNIQUENESS_INVARIANT
AUTHORIZATION_POLICY
APPLICATION_POLICY
TECHNICAL_CONSTRAINT
```

Not every condition belongs inside an Entity.

## Invariant Versus Policy

Ask:

- Can the rule be evaluated from one Entity's state?
- Does it require another aggregate or repository lookup?
- Does it depend on actor permissions?
- Does it depend on provider or transaction state?
- Is it business meaning or technical implementation?

Typical placement:

```text
one Entity state
→ Entity behavior

small pure cross-object calculation
→ Domain Service

repository/provider coordination
→ Application Use Case

database uniqueness enforcement
→ repository adapter + Domain semantic

actor/tenant authorization
→ Application policy unless Domain explicitly owns it
```

## Candidate Entities

Propose an Entity when evidence shows:

- stable business identity;
- lifecycle over time;
- state transitions;
- behavior protected by invariants;
- continuity despite attribute changes.

Record:

- candidate name;
- identity;
- lifecycle states;
- creation behavior;
- public behaviors;
- invariants;
- mutable state;
- related Value Objects;
- evidence;
- uncertainty.

Do not create an Entity merely because a database table has an ID.

## Entity Boundaries

Assess:

- what changes together;
- what must be consistent immediately;
- what can be referenced by ID;
- what has independent lifecycle;
- what is loaded and saved atomically;
- what is currently coupled only by schema convenience.

Avoid speculative aggregates.

The standard does not require aggregate terminology unless it clarifies a real consistency boundary.

## Candidate Value Objects

Propose a Value Object when evidence shows:

- no independent identity;
- equality by value;
- immutable semantic value;
- validation or normalization;
- recurring primitive obsession;
- behavior attached to the value.

Examples:

- CampaignId;
- SubscriptionId;
- IdempotencyKey;
- PromotionValidityPeriod;
- Money;
- Percentage;
- TenantId when it carries accepted semantics.

Do not wrap every primitive.

A single unvalidated string used once may remain a primitive.

## Value Object Evidence

Record:

- primitive shape;
- accepted values;
- normalization;
- equality;
- invalid cases;
- serialization;
- whether it is Domain, Application, or technical.

A provider request ID may remain an external reference rather than become a Domain Value Object unless the business uses it semantically.

## Candidate Domain Services

Propose a Domain Service only when:

- the operation is business-significant;
- it does not naturally belong to one Entity or Value Object;
- it is pure;
- it uses Domain concepts;
- it does not orchestrate repositories/providers.

Examples:

- eligibility policy involving Campaign and Subscription facts;
- pure allocation calculation;
- pure conflict resolution.

Do not call a legacy service a Domain Service because its name ends with `Service`.

## Domain Service Versus Use Case

Domain Service:

```text
pure business decision
no I/O
no transaction
no repository/provider
```

Use Case:

```text
load state
authorize
invoke Domain
persist
call external port
map semantic outcome
```

If the candidate needs I/O, it is not a pure Domain Service.

## Candidate Domain Errors

Identify semantic failures:

- invalid creation;
- illegal transition;
- expired;
- already applied;
- ineligible;
- invalid date range.

Exclude:

- HTTP 404/422;
- SQLSTATE;
- SDK timeout exception;
- provider error enum;
- authentication middleware error.

Record whether the outcome is:

```text
DOMAIN_ERROR
APPLICATION_ERROR
TECHNICAL_FAILURE
PUBLIC_COMPATIBILITY_ERROR
```

## State Transition Discovery

Build a transition table:

| Current state | Trigger | Preconditions | Next state | Rejection |
|---|---|---|---|---|

Inspect all writers, not only the primary service.

Include:

- API commands;
- jobs;
- webhooks;
- reconciliation;
- migrations;
- manual repair tools.

A status enum is not sufficient evidence for every possible transition.

## Temporal Rules

Search for:

- start/end timestamps;
- expiration;
- cooldown;
- retry deadlines;
- reconciliation windows;
- timezone assumptions;
- clock reads.

Separate:

- business time;
- provider timestamps;
- database timestamps;
- operational deadlines.

Use a Clock abstraction in Application/Domain tests only when behavior depends on time.

Do not model every timestamp as Domain state.

## Uniqueness and Concurrency

A unique database constraint may reveal a business rule.

Determine:

- business meaning;
- authoritative scope;
- tenant scope;
- lifecycle exceptions;
- soft-delete/archive behavior;
- conflict semantics.

Example:

```text
unique(subscription_id, campaign_id)
```

may support:

```text
one promotion per campaign and subscription
```

But verify whether historical/revoked rows are allowed.

Do not infer full semantics from the constraint alone.

## Authorization and Tenant Rules

Record:

- trusted actor source;
- resource owner;
- tenant boundary;
- cross-tenant prohibition;
- role/permission rules.

Determine whether the rule is:

- Application authorization policy;
- Domain ownership concept;
- persistence scoping requirement;
- public delivery concern.

Do not move body-derived or middleware-specific identities into Domain objects automatically.

Tenant isolation is mandatory safety behavior even when the legacy code implements it inconsistently.

Contradictions require escalation.

## External Provider Concepts

Separate provider language from business language.

Provider terms:

```text
HTTP 201
ALREADY_APPLIED
operation_id
retry-after
SDK status enum
```

Possible business meanings:

```text
applied
idempotent success
pending reconciliation
temporarily unavailable
```

Do not place provider statuses, retry counters, SDK objects, or credentials inside the Domain model unless product behavior explicitly treats them as business concepts.

## Persistence Concepts

Separate:

- row status;
- nullable columns;
- join tables;
- audit fields;
- ORM relations;
- optimistic version;
- outbox records;
- migration-only states.

A legacy persistence state may be:

```text
BUSINESS_STATE
TECHNICAL_PROCESS_STATE
COMPATIBILITY_STATE
CORRUPT_OR_UNKNOWN_STATE
```

Record the classification and mapping policy.

## Legacy and Unknown Data

Inspect representative stored states when available.

For states the proposed model cannot represent, recommend one:

```text
REPAIR
QUARANTINE
REJECT
COMPATIBILITY_MAP
MIGRATE
PRODUCT_DECISION_REQUIRED
```

Do not make the proposed Entity accept invalid states merely to deserialize all legacy rows.

A compatibility mapper may remain outside Domain.

## Contradictory Rules

Legacy systems often implement the same rule differently.

Record:

- path A behavior;
- path B behavior;
- data evidence;
- tests;
- incidents;
- product documentation;
- impact;
- decision required.

Do not average contradictions into a new rule.

Use:

```text
CONTRADICTION_REQUIRES_DECISION
```

## Known Bugs

A current bug is evidence of behavior, not necessarily an invariant.

Classify:

```text
ACCEPTED_BEHAVIOR
KNOWN_BUG_TO_CORRECT
UNKNOWN_INTENT
COMPATIBILITY_QUIRK
```

A modeling proposal must not embed a known bug as a Domain rule without an accepted compatibility decision.

## Ubiquitous Language

Create a glossary from product and observed behavior.

For each term record:

- preferred term;
- synonyms;
- overloaded uses;
- technical uses to avoid;
- owning capability;
- examples.

Example:

```text
Promotion
business benefit applied to a Subscription from a Campaign

Do not use:
AcmeCampaignResponse
promotion_row
discount API payload
```

Resolve naming contradictions before final model approval when they affect meaning.

## Candidate Repository Concepts

The extraction may propose repository semantics required by Domain/Application, such as:

- find Promotion by ID;
- find existing Promotion for subscription and campaign;
- save/reconstitute Promotion;
- list pending reconciliation references.

This is not the repository adapter design.

Do not include SQL/ORM method names, table joins, or generic CRUD.

Route detailed design to:

```text
designing-domain-repositories
```

## Modeling Proposal

The proposal should include:

- capability boundary;
- glossary;
- candidate Entities;
- candidate Value Objects;
- Domain Services;
- Domain errors;
- transitions;
- invariant placement;
- repository concepts;
- excluded technical concepts;
- open questions;
- confidence.

Use labels:

```text
PROPOSED
SUPPORTED
TENTATIVE
REJECTED
DECISION_REQUIRED
```

## Challenge the Proposal

Before finalizing ask:

- Is this concept business-significant or only stored?
- Does it have identity or merely a database ID?
- Does the Value Object protect real semantics?
- Is the Domain Service actually orchestration?
- Does the model encode provider terminology?
- Does it support known accepted transitions?
- Does it accidentally preserve a bug?
- Does it require cross-aggregate consistency it cannot protect?
- Can pure unit tests prove its behavior?
- Is the model larger than the selected capability requires?

## Avoiding Over-Modeling

Reject speculative concepts that have:

- no behavior;
- no accepted invariant;
- no lifecycle;
- no evidence beyond naming;
- only one technical consumer;
- future-only justification.

Examples:

- base Entity classes;
- universal Domain event hierarchy;
- generic Policy interface;
- aggregate root wrappers with no consistency role;
- Value Objects for every string;
- provider-specific Domain types.

## Avoiding Anemic Extraction

Do not produce only:

```text
PromotionData
getStatus()
setStatus()
```

when evidence clearly shows meaningful transitions and invariants.

Model behaviors using intent-revealing operations such as:

```text
Promotion.create(...)
promotion.markPending(...)
promotion.markApplied(...)
promotion.markExpired(...)
promotion.rejectApplication(...)
```

Exact API design belongs to focused modeling skills.

## Test Proposal

For each candidate invariant propose a pure test case:

```text
Given
When
Then
```

Include:

- simplest success;
- creation failure;
- transition rejection;
- boundary time/value;
- state preservation;
- equality for Value Objects;
- pure Domain Service cases.

Do not include database, HTTP, provider, or mock setup in Domain tests.

## Handoff

Route accepted candidates to:

```text
modeling-domain-entities
modeling-domain-value-objects
designing-domain-services
designing-domain-repositories
testing-domain-models
refactoring-backend-toward-hexagonal-architecture
```

The handoff must state which concepts are approved, tentative, or blocked.

Do not start refactoring while blocking Domain decisions remain unresolved.

## Failure Classification

Use:

```text
INSUFFICIENT_BEHAVIOR_EVIDENCE
CONTRADICTORY_RULES
UNKNOWN_DATA_SEMANTICS
PRODUCT_DECISION_REQUIRED
SECURITY_POLICY_UNRESOLVED
TECHNICAL_CONCEPT_MISCLASSIFIED
OVER_MODELING_RISK
ANEMIC_MODEL_RISK
SCOPE_TOO_BROAD
BLOCKED
```

## Final Decision

Use one:

```text
DOMAIN_MODEL_PROPOSAL_READY
DOMAIN_MODEL_PROPOSAL_READY_WITH_CONDITIONS
MORE_EVIDENCE_REQUIRED
PRODUCT_DECISIONS_REQUIRED
SCOPE_REDUCTION_REQUIRED
RETURN_TO_BROWNFIELD_PROFILING
BLOCKED
```

## Output

Use `assets/legacy-domain-model-extraction-record.md`.

## Completion Criteria

- [ ] One coherent legacy behavior or capability was selected.
- [ ] Entry points and all relevant writers were inspected.
- [ ] Product, tests, contracts, persistence, providers, and operational evidence were considered.
- [ ] Business decisions and state transitions were traced.
- [ ] Domain rules were separated from Application, persistence, provider, delivery, compatibility, and security concerns.
- [ ] Every invariant candidate includes evidence, confidence, and counterexamples.
- [ ] Candidate Entities have real identity and lifecycle evidence.
- [ ] Candidate Value Objects protect real semantics rather than every primitive.
- [ ] Candidate Domain Services are pure and not orchestration.
- [ ] Domain errors are semantic and protocol-neutral.
- [ ] Technical/provider/persistence concepts excluded from Domain are explicit.
- [ ] Legacy/unknown data receives an explicit compatibility or decision path.
- [ ] Contradictory rules and known bugs are not silently converted into invariants.
- [ ] The proposal is proportionate to the selected capability.
- [ ] Pure test cases are proposed for accepted invariants.
- [ ] Blocking product decisions are explicit.
- [ ] No production code was refactored or generated.
- [ ] Handoff to focused modeling/refactoring skills is clear.

## References

- Read `references/evidence-and-decision-mining.md` first.
- Read `references/separating-domain-from-technical-concerns.md` for classification.
- Read `references/entities-value-objects-and-services.md` for candidate selection.
- Read `references/state-transitions-data-and-contradictions.md` for legacy state.
- Read `references/modeling-proposal-and-handoff.md` before finalizing.
- Read `references/domain-extraction-audit.md` before completion.
