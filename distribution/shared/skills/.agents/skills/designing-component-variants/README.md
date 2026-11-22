# designing-component-variants

Designs explicit, valid component variant APIs before styling implementation.

The skill covers the exact roadmap evaluations:

```text
Button variants
size variants
compound variants
loading / disabled state
feature-specific styling mistakenly added to shared primitive
```

It keeps variant contracts semantic and implementation-neutral so they can be realized by CSS Modules, Tailwind, CSS-in-JS, or a design-system recipe layer without changing public component semantics.
