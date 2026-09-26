# Zoho Workflow Rule Testbench

An offline rules lab for a fictional CRM deal. It traces pipeline changes, assignment and follow-up queue decisions before someone configures a real CRM. It flags cycles, duplicate follow-ups and missing owners. No Deluge code is executed and no Zoho tenant, email or task list is touched.

## Contract use-case

A [CRM automation brief](https://www.upwork.com/freelance-jobs/apply/CRM-Automation-Specialist-Zapier-Make-HubSpot-Zoho-Real-Workflow-Builds_~022038133362948951578/) asks for stages, cleanup, follow-ups and form/email/CRM connections. A [Zoho customization brief](https://www.freelancer.com/projects/crm/zoho-crm-customization-integration-39548378) includes modules and workflow rules. This repo shows a test-first *design exercise* for a subset of that work. Neither brief is this project's client.

## Run

Python 3.10+ and standard library only. From the repository root:

```sh
python3 cli.py examples.json
python3 -m unittest discover -p 'test_*.py' -v
```

No Zoho trial or credentials needed. The fixture is entirely fictional and deliberately broken. Expected finding codes: `missing_owner`, `duplicate_followup`, `cycle_detected`; `external_actions` remains zero. `DESIGN.md` includes a clean-rule example and a deployment checklist.

## Rule contract

A rule has unique `id`, trigger `event` (`deal_created`, `stage_changed`, `followup_due`), optional exact-match `when`, and an `action`: `assign_owner`, `set_stage`, or `queue_followup`. A value is the owner ID, stage label or reminder label respectively. The interpreter queues an internal `stage_changed` event after a real stage transition and records each matched rule in a trace. It detects a repeated event plus record state as a cycle. A bounded step limit prevents runaway execution. Duplicate follow-up labels for a deal are reported, not silently scheduled twice.

## Boundaries and risk

This is a **fictional intermediate rules language**, not Zoho Deluge syntax, workflow behavior or API semantics. It is intentionally narrower than a production engine: no priorities, asynchronous execution, role permissions, delayed schedules, idempotent persistence, real notifications or safe deployment. A clean trace is not permission to activate a rule in a tenant. See `DESIGN.md` for review, tests and rollout checks. Use only synthetic records in this repository.
