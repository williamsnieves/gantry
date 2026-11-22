# designing-frontend-dtos-and-view-data

Designs stable frontend data boundaries:

```text
Transport/provider
→ Domain
→ Application DTO/result
→ Presentation view data
→ Component props
```

It covers Application DTO value, discriminated results, nullability, partial data, dates/numbers/enums, formatting and localization ownership, server/client serialization, mapping ownership, and test boundaries.

It prevents provider and snake_case leakage, ReactNode/JSX/icons/colors/CSS in Application DTOs, giant nullable bags, localized UI formatting in the wrong layer, and speculative BaseDTO/mapper frameworks.
