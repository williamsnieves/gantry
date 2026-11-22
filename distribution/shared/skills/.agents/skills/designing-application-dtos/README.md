# designing-application-dtos

Designs stable Application Request and Response DTOs with:

- primitives and plain data only;
- explicit Request-to-Domain mapping;
- explicit Domain-to-Response mapping;
- field minimization;
- clear optionality, enum, date, Money, and compatibility semantics.

It prevents Entities, Value Objects, ORM rows, provider payloads, and HTTP/framework types from crossing the Application boundary.
