#!/usr/bin/env python3

import sys

from collections import namedtuple

GameState = namedtuple('GameState', 'wizard_hp mana spent boss_hp '
                        'shield_turns poison_turns recharge_turns')

def GameState_adjust(self, **kwargs):
    for k in kwargs:
        kwargs[k] += getattr(self, k)
    return self._replace(**kwargs)

GameState._adjust = GameState_adjust

Spell = namedtuple('Spell', 'name cost turns_index')

MISSILE = Spell('Magic Missile', 53, None)
DRAIN = Spell('Drain', 73, None)
SHIELD = Spell('Shield', 113, 4)
POISON = Spell('Poison', 173, 5)
RECHARGE = Spell('Recharge', 229, 6)

SPELLS = (MISSILE, DRAIN, SHIELD, POISON, RECHARGE)

def boss_strike(state, damage):
    if state.shield_turns > 0:
        damage = max(0, damage-7)
    if damage<=0:
        return state
    return state._adjust(wizard_hp= -damage)

def can_cast(state, spell):
    if spell.cost > state.mana:
        return False
    if spell.turns_index is not None and state[spell.turns_index] > 0:
        return False
    return True

def effects(state):
    if state.poison_turns > 0:
        state = state._adjust(poison_turns=-1, boss_hp=-3)
    if state.recharge_turns > 0:
        state = state._adjust(mana=+101, recharge_turns=-1)
    if state.shield_turns > 0:
        state = state._adjust(shield_turns=-1)
    return state

def cast(state, spell):
    mana = state.mana - spell.cost
    spent = state.spent + spell.cost
    if spell==MISSILE:
        return state._replace(boss_hp=state.boss_hp-4, mana=mana, spent=spent)
    if spell==DRAIN:
        return state._replace(boss_hp=state.boss_hp-2, spent=spent,
                            wizard_hp=state.wizard_hp+2, mana=mana)
    if spell==SHIELD:
        return state._replace(shield_turns=6, mana=mana, spent=spent)
    if spell==POISON:
        return state._replace(poison_turns=6, mana=mana, spent=spent)
    if spell==RECHARGE:
        return state._replace(recharge_turns=5, mana=mana, spent=spent)

def combat(state, boss_attack, decay):
    if decay:
        state = state._adjust(wizard_hp=-decay)
    states = [state]
    seen = { state: (None, None) }
    best_mana = 1_000_000
    best_run = None
    while states:
        state = states.pop(0)
        if state.spent >= best_mana:
            continue
        for spell in SPELLS:
            # ... player turn
            if not can_cast(state, spell):
                continue
            st = cast(state, spell)
            if st.wizard_hp<=0 or st.spent >= best_mana:
                continue
            # Enemy turn
            st = effects(st)
            if st.boss_hp<=0:
                if best_mana > st.spent:
                    best_mana = st.spent
                    best_run = (spell, state)
                continue
            st = boss_strike(st, boss_attack)
            # Player turn ...
            if decay:
                st = st._adjust(wizard_hp=-decay)
            if st.wizard_hp<=0:
                continue
            st = effects(st)
            if st.boss_hp<=0:
                if best_mana > st.spent:
                    best_mana = st.spent
                    best_run = (spell, state)
                continue
            if st in seen:
                continue
            seen[st] = (spell, state)
            states.append(st)
    return best_mana

def main():
    if len(sys.argv)!=3:
        exit("Usage: %s <boss_hp> <boss_attack>"%sys.argv[0])
    boss_hp, boss_attack = map(int, sys.argv[1:])
    initial_state = GameState(50, 500, 0, boss_hp, 0, 0, 0)
    best_mana = combat(initial_state, boss_attack, 0)
    print("Best mana (normal):", best_mana)
    best_mana = combat(initial_state, boss_attack, 1)
    print("Best mana (hard):", best_mana)

if __name__ == '__main__':
    main()
