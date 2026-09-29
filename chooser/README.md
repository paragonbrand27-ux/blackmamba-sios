# Chooser prototype

This package provides a small, dependency-free starting point for the BlackMamba SIOS chooser. Its scoring approach mirrors common recommender-system patterns used in the Microsoft Recommenders ecosystem:

- content-based similarity using tag overlap;
- a bounded popularity signal;
- an optional history signal;
- maximal-marginal-relevance-style diversity re-ranking;
- explicit, inspectable explanations for every result.

## Important boundaries

- **No covert censorship:** no global blocklist or hidden ranking rule exists.
- **User control:** callers can block items and choose the diversity value.
- **Policy transparency:** an optional policy callback is visible in the application code. If an item is rejected, production code should record the policy reason in a tamper-evident audit log.
- **Safety and rights:** “uncensored” must not mean “unaccountable.” Keep consent, privacy, lawful-use, anti-abuse, and child-safety controls explicit and reviewable.
- **Security:** this module is not an OS permission boundary and must not receive secrets or execute untrusted code.

For a production integration, replace the simple similarity function with a tested model from the Microsoft Recommenders toolkit, version and pin dependencies, evaluate offline, and run bias, privacy, and security audits before deployment.
