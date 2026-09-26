"""Offline workflow interpreter, not a Deluge interpreter or Zoho integration."""
from __future__ import annotations
from copy import deepcopy

ALLOWED_EVENTS = {'deal_created', 'stage_changed', 'followup_due'}
ALLOWED_ACTIONS = {'assign_owner', 'set_stage', 'queue_followup'}


def validate_rules(rules):
    if not isinstance(rules, list):
        raise ValueError('rules must be a list')
    ids = set()
    for rule in rules:
        if not isinstance(rule, dict) or not isinstance(rule.get('id'), str) or not rule['id']:
            raise ValueError('Each rule requires an ID')
        if rule['id'] in ids:
            raise ValueError('Duplicate rule ID')
        ids.add(rule['id'])
        if rule.get('event') not in ALLOWED_EVENTS or rule.get('action') not in ALLOWED_ACTIONS:
            raise ValueError(f"Unsupported event/action for {rule['id']}")
        if not isinstance(rule.get('when', {}), dict):
            raise ValueError('when must be an object')
        if rule['action'] == 'set_stage' and (not isinstance(rule.get('value'), str) or not rule['value']):
            raise ValueError('set_stage needs value')
    return rules


def simulate(rules, record, initial_event='deal_created', max_steps=20):
    """Trace a single fictional deal, stop cycles and duplicate side effects."""
    validate_rules(rules)
    if initial_event not in ALLOWED_EVENTS or not isinstance(record, dict):
        raise ValueError('Invalid initial event or record')
    if not isinstance(max_steps, int) or max_steps < 1:
        raise ValueError('max_steps must be positive')
    state = deepcopy(record)
    pending = [initial_event]
    trace, findings = [], []
    visited = set()
    followups = set()
    steps = 0
    while pending:
        event = pending.pop(0)
        signature = (event, tuple(sorted((k, str(v)) for k, v in state.items())))
        if signature in visited:
            findings.append({'code':'cycle_detected','event':event})
            break
        visited.add(signature)
        for rule in rules:
            if rule['event'] != event or any(state.get(k) != v for k, v in rule.get('when', {}).items()):
                continue
            steps += 1
            if steps > max_steps:
                findings.append({'code':'step_limit','rule':rule['id']})
                pending.clear()
                break
            action = rule['action']
            if action == 'assign_owner':
                owner = rule.get('value')
                if not isinstance(owner, str) or not owner.strip():
                    findings.append({'code':'missing_owner','rule':rule['id']})
                    continue
                state['owner'] = owner
                trace.append({'rule':rule['id'],'action':action,'value':owner})
            elif action == 'set_stage':
                target = rule['value']
                if state.get('stage') == target:
                    findings.append({'code':'no_op_stage','rule':rule['id']})
                else:
                    state['stage'] = target
                    trace.append({'rule':rule['id'],'action':action,'value':target})
                    pending.append('stage_changed')
            else:
                token = (str(state.get('id', '')), str(rule.get('value', 'followup')))
                if token in followups:
                    findings.append({'code':'duplicate_followup','rule':rule['id']})
                else:
                    followups.add(token)
                    trace.append({'rule':rule['id'],'action':action,'value':token[1]})
    return {'mode':'simulation_only','state':state,'trace':trace,'findings':findings,'external_actions':0}
