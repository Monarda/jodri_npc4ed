from .src.npc4e import NPC4e

def print_npc(npc : NPC4e):
    """ Example of pretty printing the new NPC4e class """

    print(f'{npc.species} ({npc.species_used}) {npc.careername}')
    print(f'{npc.career_history_unambgious}')
    print(npc.statblock)

    print(f'**Skills**: {npc.skills}')

    if npc.talents_initial: print(f'**Initial Talents**: {npc.talents_initial}')
    print(f'**Suggested Talents: {npc.talents_suggested}')
    print(f'**Additional Talents: {npc.talents_additional}')

    print(f'**Traits**: {npc.traits}')
    if npc.traits_optional: print(f'**Optional Traits**: {npc.traits_optional}')

    print(f'**Trappings**: {npc.trappings}')
    print(f'**Additional Trappings**: {npc.trappings_additional}')

    print(f'**XP Spend**: {npc.xp_spend}')


def main():
    # Generate completely random NPC
    npc = NPC4e()
    print_npc(npc)
    print(60*'-')

    # Generate random NPC of species Reiklander and a starting career of Guard
    npc = NPC4e(random=True, species='Reiklander', careers=[('Guard',1)])
    npc.filter = 'combat'
    print_npc(npc)

    # Generate NPC with defined career path
    npc = NPC4e(random=False, species='Skaven', careers=[('Guard',1), ('Guard',2), ('Pedlar',2)])
    print_npc(npc)
    print(60*'-')

    # Generate NPC with random career path starting from Student **but** defined starting 
    # characteristics, skills, talents and trappings
    # Note that talents that modify stats will be applied to the characteristics
    npc = NPC4e(random=True, species='Middenlander', careers=[('Scholar',1)],
                characteristics={"M":4, "WS":31, "BS":37, "S":30, "T":28, "I":36, "Agi":34, "Dex":28, "Int":29, "WP":30, "Fel":32},
                initial_skills={"Consume Alcohol":5, "Haggle":5, "Language (Brettonian)":3, "Lore (Estalia)":3, "Sail (Caravel)": 5, "Swim":3},
                initial_talents={"Linguistics", "Marksman", "Resistance (Mutation)", "Rover", "Very Strong"},
                initial_trappings={'Icon of Myrmidia'})    
    print_npc(npc)
    print(60*'-')

    # Print some additional details
    print(NPC4e.known_species())

if __name__ == "__main__":
    # execute only if run as a script
    main()