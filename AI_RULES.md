================================================================================
PROJECT PREDATOR – AI DEVELOPMENT RULES
================================================================================
Status: LOCKED
Scope: Applies to ALL AI coding assistants (Cursor, Antigravity, Copilot, etc.)

================================================================================
1. PROJECT IDENTITY
================================================================================

- PROJECT PREDATOR is a Trading Operating System, NOT a trading bot.
- This project is PLATFORM-FIRST, not strategy-first.
- The architecture is governed by:
  - /docs/constitution/MASTER.md
  - All policy documents.

Any code that violates these documents is INVALID.

================================================================================
2. ABSOLUTE PROHIBITIONS
================================================================================

AI MUST NEVER:

- Add real exchange connections unless explicitly allowed by the current phase.
- Add real trading logic unless explicitly allowed by the current phase.
- Add strategies unless explicitly allowed by the current phase.
- Bypass Risk / CRO / PolicyGuard layers.
- Merge phases (e.g., implement FAZ 2 inside FAZ 1).
- Optimize for profit, performance, or speed before stability.
- Remove logging, safety checks, or governance layers.
- Introduce "temporary hacks" or "just for now" shortcuts.

================================================================================
3. PHASE DISCIPLINE
================================================================================

- The project follows strict phases (see /docs/phases/PhasePlan.md).
- AI MUST only implement features belonging to the CURRENT PHASE.
- If a request belongs to a future phase, AI MUST:
  - Refuse
  - Or ask for confirmation.

================================================================================
4. RISK-FIRST PRINCIPLE
================================================================================

- Risk management and control layers are ALWAYS more important than features.
- Any code change that weakens control, observability, or safety is FORBIDDEN.

================================================================================
5. ARCHITECTURE RULES
================================================================================

- Platform > Engine > Strategy hierarchy MUST be preserved.
- Event-driven design is preferred.
- All components must be replaceable.
- No component may directly call an exchange.
- All actions must pass through PolicyGuard.

================================================================================
6. SIMPLICITY RULE
================================================================================

- Prefer simple, explicit, readable code.
- No premature optimization.
- No hidden magic.
- No overengineering.

================================================================================
7. AI BEHAVIOR RULE
================================================================================

When in doubt, AI MUST:

- Ask before adding features.
- Prefer less code, not more.
- Preserve architecture over functionality.

================================================================================
8. FINAL RULE
================================================================================

> PROFIT NEVER JUSTIFIES LOSS OF CONTROL.

Any code violating this principle is considered a SYSTEM FAILURE.

================================================================================
END
================================================================================