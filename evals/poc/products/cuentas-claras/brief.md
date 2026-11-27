# Cuentas claras

A web app where a group of friends records shared expenses and sees who owes whom. TypeScript: a React front end and a Node API, SQLite.

Give the requests in order, one per session, text unchanged.

## Stage 1: the product

**B1**

> Set up the project: a React front end and a Node API in TypeScript, with SQLite. One command starts both for development. Tests, lint and type checks each run with one command. Write a README that says how.

**B2**

> Someone creates a group with a name and the names of its members, and gets a link to share. Anyone with the link can open the group. No accounts, no passwords.

**B3**

> In a group, people add expenses: what it was, who paid, how much, and who it is split between. The group shows what each person has paid and who owes whom.

**B4**

> The group screen: the list of expenses, the balances, and a form to add an expense. It has to work well on a phone, and for someone who only uses the keyboard.

**B5**

> An expense can be edited and deleted.

Tag `stage-1`. Evaluate.

## Stage 2: changing it

**B6**

> A group chooses its currency when it is created. The groups that exist today are in euros.

**B7**

> Clean up the balance calculation: one function, in one place, same behaviour. Change nothing a user can see.

**B8**

> When someone pays back what they owe, the group can record it, and the balances reflect it.

Tag `stage-2`. Evaluate.
