# Smells, and what removes each

Read the row for the smell you named. Refactorings are listed simplest first: take the first that removes the smell. The last column is the only case in which a design pattern is worth its indirection; if the condition is not true of the code today, do not use it.

| Smell | How to recognise it | Refactorings, simplest first | A pattern only if |
|---|---|---|---|
| Long function | It does several things; you need comments to mark its parts | Extract function; replace a temporary with a query; decompose a conditional | — |
| Long parameter list | Four or more parameters, or several that always travel together | Introduce a parameter object; preserve the whole object; remove a flag argument | **Builder**: an object needs many optional parts and call sites build it in different combinations |
| Duplicated logic | The same rule is written in two or more places and must change together | Extract function; pull the shared part up or into a module | **Template Method**: two procedures share their steps and differ in one or two of them |
| Large class or module | It changes for unrelated reasons; its fields are used in separate groups | Extract class; extract module; move function | **Facade**: callers need one simple entry to several parts that must stay separate |
| Feature envy | A function uses another object's data more than its own | Move function to the data; extract the envious part and move it | — |
| Shotgun surgery | One decision requires edits in many files | Move the scattered pieces together; inline what was split too far | — |
| Divergent change | One file is edited for many unrelated decisions | Split by reason to change; extract class | — |
| Switch on type | The same `switch` or `if` chain on a kind appears in several places | Extract the chain into one function; replace it with a lookup table | **Strategy** (or polymorphism): three or more kinds exist, each with behaviour, and new kinds are added |
| Primitive obsession | A string or number carries rules (an email, money, an id) checked in many places | Introduce a value object; replace a type code with an enum | — |
| Data clump | The same three or four values appear together in signatures and fields | Extract class or parameter object | — |
| Complex construction | Creating an object takes many steps, or callers must know which class to create | Extract a factory function | **Factory Method / Abstract Factory**: the concrete class is chosen at run time from several that exist today; **Builder**: see long parameter list |
| Tangled dependency on an external service | Business code calls a client library, HTTP or SQL directly | Extract the calls into one function or module; pass it in | **Adapter**: the outside interface does not fit what the code needs, or there is a second provider |
| Nested conditionals | Three or more levels of `if`; the main path is hard to see | Guard clauses; decompose the conditional; extract function | **State**: the conditions are the same state checked in many functions |
| Message chain | `a.b().c().d()`: the caller knows the whole structure | Hide the delegate; extract function over the chain | — |
| Speculative generality | An abstraction, parameter or hook with one use | Inline it; collapse the hierarchy; remove the parameter | — (this smell is a pattern used too early) |
| Temporal coupling | Calls must happen in an order nothing enforces | Combine them into one function; return the next step's input from the previous | **Builder** or a small state object that makes the wrong order impossible |
| Notification spread | Several parts must react when one thing changes, each called by hand | Extract the reactions into one function called once | **Observer**: the set of listeners changes at run time or belongs to other modules |
| Dead code | Nothing calls it | Delete it | — |

## Rules for choosing

1. The change that removes the smell with the least new structure wins.
2. A pattern needs at least two real cases in the code now. One case is a function.
3. Follow the project's existing conventions (`docs/conventions.md`) over any name in this table.
4. If two smells overlap, remove the one that blocks the change you came for, and stop.
