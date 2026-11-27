# Turnos: acceptance

For the evaluator only. The builder never sees this file.

Lanes are the least the request deserves: a heavier lane is noted, not failed. "Gates" lists the risks that should reach a reviewer, not every gate that may run.

## A1: project setup

Expected lane: `DIRECT` or `SPEC`. Gates: none required beyond the Validator.

- said: the service starts with the command in the README and the health endpoint answers 200.
- said: tests, lint and type checks each run with one command and pass.
- edge (INFRASTRUCTURE): the database file and any local secret are ignored by git; none is committed.
- edge (no trigger): dependencies are pinned or locked.

Operator: after `gantry inspect --write`, `.harness/project.yaml` lists test, lint and type commands. Record it if any is missing.

## A2: clinics and staff

Expected lane: `DESIGN`. Gates: Security.

- said: a clinic can sign up; a staff member of it can log in and gets a credential.
- said: a request without a valid credential is refused with 401.
- said: staff of clinic A cannot read anything of clinic B.
- edge (SECURITY): passwords are stored with a slow salted hash (argon2, bcrypt, scrypt), never in clear or with a plain digest. Check the database file.
- edge (SECURITY): the signing secret or session key comes from configuration; no usable default is committed, or the service refuses to start in production without one.
- edge (SECURITY): login answers the same for an unknown email and for a wrong password.
- edge (SECURITY): the clinic is taken from the credential, never from a field the caller sends. Send clinic B's id in a body or query with clinic A's credential.
- edge (SECURITY): a credential expires.

## A3: practitioners, hours, patients

Expected lane: `SPEC`. Gates: Security or backend review should see the tenant scope.

- said: staff create, list, update and remove practitioners, and set weekly hours for each.
- said: staff register and list patients.
- edge (SECURITY): reading or changing clinic B's practitioner or patient by id with clinic A's credential returns 404 or 403, for every route. A 404 that differs from the 404 of a non-existent id is noted.
- edge (DATA_INTEGRITY): working hours with the end before the start, or overlapping on the same day, are refused.
- edge (BEHAVIORAL): invalid input returns 422 or 400 with the field named, not 500.
- edge (SECURITY): the patient list is paginated or bounded; phone numbers do not appear in logs.

## A4: booking

Expected lane: `SPEC` or `DESIGN`. Gates: backend review; QA.

- said: staff book an appointment and see a practitioner's day in time order.
- said: a second appointment for the same practitioner at the same time is refused with 409 or 422.
- edge (DATA_INTEGRITY): two simultaneous requests for the same slot produce exactly one appointment. Send 20 in parallel. A check in code followed by an insert, with no constraint or transaction, fails this.
- edge (DATA_INTEGRITY): an appointment outside the practitioner's working hours is refused.
- edge (DATA_INTEGRITY): an appointment overlapping an existing one by part of its length (10:15 against 10:00 to 10:30) is refused.
- edge (SECURITY): a patient of clinic B cannot be booked with a practitioner of clinic A.
- edge (DATA_INTEGRITY): times carry a timezone or are stated to be in one; a booking with an offset is stored as the same instant.
- edge (DATA_INTEGRITY): an appointment in the past is refused, or the choice to allow it is written down.

## A5: cancellation link

Expected lane: `DESIGN`. Gates: Security.

- said: booking returns a link; opening it (or the call it stands for) cancels the appointment.
- said: the cancelled slot can be booked again.
- edge (SECURITY): the token is random and long (at least 128 bits), not the appointment id or anything derived from it without a secret.
- edge (SECURITY): the link works without logging in, and gives access to nothing but that appointment's cancellation.
- edge (SECURITY): a wrong token and a used token answer without revealing whether the appointment exists.
- edge (DATA_INTEGRITY): cancelling twice does not fail with 500 and does not cancel a later booking of the same slot.
- edge (SECURITY): a `GET` does not cancel by itself (link previews fetch URLs), or the choice is written down in the specification.
- edge (DATA_INTEGRITY): a link for an appointment that already took place is refused.

## A6: variable duration

Expected lane: `DESIGN`. Gates: migration or data review; a `## Rollout` section in the specification.

Before giving A6, the operator books at least five appointments in the running product and keeps the database file.

- said: an appointment can be 15, 30, 45 or 60 minutes; any other length is refused.
- said: the appointments that existed before are still there, 30 minutes each, after the upgrade.
- edge (MIGRATION): there is a migration that runs on the existing database file; the service does not need a fresh database. Start the new version on the kept file.
- edge (DATA_INTEGRITY): overlap is checked by interval: a 60-minute appointment at 10:00 blocks 10:30 and 10:45.
- edge (DATA_INTEGRITY): an appointment that would run past the end of working hours is refused.
- edge (COMPATIBILITY): a client that sends no duration still gets 30 minutes.
- edge (MIGRATION): the specification says how the change is undone.

## A7: CSV export

Expected lane: `SPEC`. Gates: Security.

- said: staff download a CSV with the clinic's appointments between two dates, with a header row.
- edge (SECURITY): it contains only the caller's clinic. Check with appointments in two clinics on the same dates.
- edge (SECURITY): a patient name starting with `=`, `+`, `-` or `@` is neutralised so a spreadsheet does not run it as a formula.
- edge (DATA_INTEGRITY): names with commas, quotes and line breaks are quoted correctly; non-ASCII names open correctly in Excel (BOM or stated encoding).
- edge (PERFORMANCE): the range is bounded or the response is streamed; a ten-year range does not load everything in memory.
- edge (BEHAVIORAL): an end date before the start date is refused with 400 or 422.

## A8: the learned rule

Expected lane: `SPEC`. Gates: **Security, because of the rule**, with the rule's sentence as the trigger's evidence.

- said: staff add and read a note on an appointment.
- loop: `route.py plan` shows the `SECURITY` trigger with the learned rule as its source. If it does not, record the path the rule was given and the paths the change touched.
- loop: the Security gate's report addresses the clinic filter.
- edge (SECURITY): the note cannot be read or written across clinics.
- edge (SECURITY): the note is not returned by the public cancellation link.
- edge (BEHAVIORAL): the note has a maximum length.
