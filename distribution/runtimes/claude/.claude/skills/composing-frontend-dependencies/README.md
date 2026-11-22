# composing-frontend-dependencies

Creates the frontend composition boundary that selects concrete adapters, constructs Use Cases, controls lifecycle, and injects semantic dependencies into routes, screens, containers, hooks, and package consumers.

It handles safe shared clients, per-user and per-request isolation, SSR/server-client separation, explicit Factory or accepted DI-container policies, test overrides, and disposal.

It prevents Service Locators, broad dependency contexts, first-user singletons, cross-request cache leaks, and concrete Infrastructure imports from React code.
