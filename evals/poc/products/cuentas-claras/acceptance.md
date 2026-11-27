# Cuentas claras: acceptance

For the evaluator only. The builder never sees this file.

Lanes are the least the request deserves: a heavier lane is noted, not failed. Check the front end in a browser at 375 px and at desktop width.

## B1: project setup

Expected lane: `DIRECT` or `SPEC`.

- said: one command starts the front end and the API; the page loads and reaches the API.
- said: tests, lint and type checks each run with one command and pass, for both sides.
- edge (INFRASTRUCTURE): the database file, `node_modules` and build output are ignored by git.
- edge (no trigger): a lockfile is committed; TypeScript runs in strict mode.

Operator: after `gantry inspect --write`, `.harness/project.yaml` lists test, lint and type commands that cover both sides. Record it if one side is left out.

## B2: groups and share links

Expected lane: `DESIGN` (the link is the only access control). Gates: Security.

- said: creating a group returns a link; opening it shows the group's name and members.
- edge (SECURITY): the link's identifier is random and long (at least 128 bits), not a counter or a short code.
- edge (SECURITY): no route lists groups, and a wrong identifier returns 404 without detail.
- edge (BEHAVIORAL): a group with no name, no members, or two members with the same name is refused, with the field named.
- edge (SECURITY): a member name with HTML in it is shown as text.
- edge (SECURITY): the API limits the size of the request body and the number of members.

## B3: expenses and balances

Expected lane: `SPEC`. Gates: backend review; QA.

- said: an expense records description, payer, amount and who shares it; the group shows totals paid and who owes whom.
- said: with one 30.00 expense paid by Ana and split between Ana, Luis and Marta, Luis and Marta each owe Ana 10.00.
- edge (DATA_INTEGRITY): amounts are stored as integer minor units, not floating point. 0.10 + 0.20 across expenses gives exactly 0.30.
- edge (DATA_INTEGRITY): 10.00 split between three people gives shares that add up to exactly 10.00 (3.34, 3.33, 3.33 or equivalent), and the balances of a group always add up to zero.
- edge (DATA_INTEGRITY): an amount that is zero, negative, not a number, or has more than two decimals is refused.
- edge (DATA_INTEGRITY): a payer or a sharer who is not a member of the group is refused; an expense split between nobody is refused.
- edge (SECURITY): an expense cannot be added to group A using a member id of group B.

## B4: the group screen

Expected lane: `SPEC`. Gates: Frontend review; QA.

- said: the screen shows expenses, balances and a form that adds an expense without reloading the page.
- said: at 375 px nothing overflows sideways and every control can be used.
- said: the form can be filled and sent with the keyboard only, in a sensible order.
- edge (BEHAVIORAL): there is a visible loading state, an empty state for a group with no expenses, and an error state when the API fails (stop the API and reload).
- edge (USER_IMPACT): every input has a label a screen reader announces; validation errors are tied to their field and announced.
- edge (BEHAVIORAL): pressing the submit button twice quickly creates one expense.
- edge (BEHAVIORAL): when saving fails, what the user typed is kept.
- edge (USER_IMPACT): focus is visible, and after adding an expense it goes somewhere deliberate.
- edge (BEHAVIORAL): amounts are shown with two decimals and the same format everywhere.

## B5: edit and delete

Expected lane: `SPEC`. Gates: backend and frontend review.

- said: an expense can be edited and deleted, and the balances change accordingly.
- edge (BEHAVIORAL): deleting asks for confirmation or can be undone.
- edge (DATA_INTEGRITY): editing validates the same as creating (every edge of B3 holds on the edit route).
- edge (SECURITY): an expense of group A cannot be edited or deleted through group B's link.
- edge (DATA_INTEGRITY): editing or deleting an expense that someone else already deleted answers 404 and the screen recovers, without a blank page.

## B6: currency per group

Expected lane: `DESIGN`. Gates: migration or data review; a `## Rollout` section.

Before giving B6, the operator creates two groups with expenses in the running product and keeps the database file.

- said: a new group has a currency; amounts are shown in it.
- said: the existing groups show euros, with the same amounts as before.
- edge (MIGRATION): a migration runs on the kept database file; no fresh database is needed.
- edge (DATA_INTEGRITY): a currency without decimals (JPY) accepts 1000 and refuses 10.50; one with two decimals behaves as before. An implementation that multiplies by 100 for every currency fails this.
- edge (BEHAVIORAL): an unknown currency code is refused; the set is a list of ISO 4217 codes, not free text.
- edge (COMPATIBILITY): the currency of a group that has expenses cannot be changed, or the specification says what happens to the amounts.
- edge (BEHAVIORAL): formatting uses the currency (symbol or code, decimals) everywhere an amount appears.

## B7: one balance calculation

Expected lane: `DIRECT`. The builder should read `refactoring-safely` and pin the tests.

- said: there is one balance function; no second copy remains in the other side of the project or in a component.
- said: every acceptance item of B3, B5 and B6 still passes.
- process: `python3 .harness/bin/refactor.py status` says `HELD` at the final gate, or the report says which pinned tests changed and why.
- process: tests for the calculation existed, or were added, before the code moved (the commit order or the pin shows it).
- edge (no trigger): no behaviour changed that a user can see; the rounding of 10.00 between three is the same as before.

Record whether `refactoring-safely` was read: it is the one build skill `harness-start` names.

## B8: settling up

Expected lane: `SPEC`. Gates: backend and frontend review; QA.

- said: a payment from one member to another can be recorded, and the balances reflect it.
- said: with Luis owing Ana 10.00, recording that Luis paid Ana 10.00 leaves both at zero.
- edge (DATA_INTEGRITY): a payment is its own record; no expense is edited or removed to represent it, and the expense list still shows the history.
- edge (DATA_INTEGRITY): a payment of zero, a negative one, or one from a member to themselves is refused.
- edge (DATA_INTEGRITY): paying more than what is owed is refused, or leaves the other person owing the difference; the balances still add up to zero.
- edge (BEHAVIORAL): pressing the button twice records one payment.
- edge (DATA_INTEGRITY): the amount follows the group's currency rules from B6.
