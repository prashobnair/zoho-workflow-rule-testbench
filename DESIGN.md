# Rule design and rollout notes

## Business review

Before implementing actual Zoho rules, agree on stage definitions, record ownership, follow-up timing, qualification criteria, opt-in and exception queues. For every rule, capture owner, trigger, precondition, exact intended side effect, conflict/priority policy and how to disable it. A rule set should be reviewed with representative good and bad records; a simulation only approximates the intended flow.

## Good and bad examples

`examples.json` intentionally has an empty owner, two rules that queue `day-2` for the same deal, and stage rules that toggle `new` and `qualified`. The resulting trace should stop at `cycle_detected`; it never sends reminders. A clean sample can use an owner assignment, `new` → `qualified` transition and a single follow-up queue action. The unit test `test_clean_rule_advances_and_assigns` specifies it.

## Test and deployment checklist

- Tests cover broken and clean traces, duplicate rule IDs, unsupported actions, step limit and determinism.
- In a real tenant, inspect current workflow/Deluge docs and metadata; map actual fields and APIs. This simulator doesn't assert exact Zoho trigger ordering or Deluge behavior.
- Create a sandbox test matrix with source forms, stage transitions, repeated events, edits, missing owner, retries, opt-outs and role-specific access.
- Have a human review the resulting tasks/messages and workflow conflicts. Capture baseline config, change set, rollback/deactivation steps and a named owner for monitoring.
- Deploy narrowly, verify logged runs, then expand only when duplicate prevention and recovery are demonstrated.

This is not a workflow deployment tool; the `external_actions: 0` output is deliberate.
