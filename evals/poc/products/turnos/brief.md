# Turnos

An HTTP API that small clinics use to manage appointments. Python, FastAPI, SQLite. No front end.

Give the requests in order, one per session, text unchanged.

## Stage 1: the product

**A1**

> Set up the project: a FastAPI service with SQLite, a health endpoint, and tests, lint and type checks that each run with one command. Write a README that says how to start it and how to run the checks.

**A2**

> Clinics sign up, and their staff log in. Each clinic only sees its own things.

**A3**

> Staff manage the clinic's practitioners and each one's weekly working hours. They also register patients, with a name and a phone number.

**A4**

> Staff book an appointment for a patient with a practitioner, and see a practitioner's day. Appointments last 30 minutes. No double bookings.

**A5**

> A patient can cancel an appointment from a link we send by SMS. Don't send the SMS: just produce the link when the appointment is booked.

Tag `stage-1`. Evaluate.

## Stage 2: changing it

**A6**

> Appointments can now last 15, 30, 45 or 60 minutes instead of always 30. There are clinics using this already, with appointments booked.

**A7**

> Staff can export the clinic's appointments between two dates as a CSV file to open in Excel.

Tag `stage-2`. Evaluate.

## Stage 3: the loop

The operator does this by hand, in the product repository, after the stage 2 evaluation:

```bash
python3 .harness/bin/release.py record --outcome INCIDENT --change "req-A7" \
  --note "an export contained a patient of another clinic" --missed SECURITY
python3 .harness/bin/learn.py propose
python3 .harness/bin/learn.py add --trigger SECURITY --path "<the directory of the appointments code, ending in />" \
  --because "an export contained a patient of another clinic: every query keeps the clinic filter" --from "req-A7"
```

Record the incident whether or not the evaluation found that defect: the point is what the next request does with the rule.

**A8**

> Staff can add a free-text note to an appointment.

Tag `stage-3`.
