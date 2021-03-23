from src.npc4e import NPC4e

def print_npc(npc):
    print(f'{npc.species} ({npc.species_used}) {npc.careername}')
    print(f'{npc.career_history_unambgious}')
    print(npc.statblock)
    print(f'**Skills**: {npc.skills}')
    if npc.talents_initial: print(f'**Initial Talents: {npc.talents_initial}')
    print(f'**Suggested Talents: {npc.talents_suggested}')
    print(f'**Additional Talents: {npc.talents_additional}')
    print(f'**Traits**: {npc.traits}')
    print(f'**Trappings**: {npc.trappings}')
    print(f'**Additional Trappings**: {npc.trappings_additional}')
    print(f'**XP Spend**: {npc.xp_spend}')


def main():
    npc = NPC4e(random=False, species='Ogre', careers=[('Guard',1), ('Guard',2), ('Pedlar',2)])
    print_npc(npc)

    npc = NPC4e(random=True, species='ogre')
    print_npc(npc)

if __name__ == "__main__":
    # execute only if run as a script
    main()