import argparse

import random

from .src.npc.careers4 import Careers4
from .src.npc.buildNPC4 import *
from .src.utility.find_best_match import find_best_match

def main():
    ## Scroll down below the return for a better demo of how to programmatically interact with the Npc4 class

    parser = argparse.ArgumentParser(description="Generate a specified WFRP4 NPC")
    parser.add_argument("--species", help="Species of NPC to create", type=str, nargs='?',default='Human')
    parser.add_argument("--species-list", action='store_true', help="List known careers")
    parser.add_argument("--careers-list", action='store_true', help="List known species")
    parser.add_argument("--type", choices=['combat','social','utility'], help="Remove information not relevant to this type of NPC")
    parser.add_argument("careerrank", nargs='*')
    parser.parse_args()
    args = parser.parse_args()

    # These don't actually work; I can't remember how to enable this with argparse
    if args.species_list:
        print("Unknown species will be considered a type of human.")
        print("Known species: " + ', '.join(species_npc_characteristics_4e.keys()).title())
        sys.exit()

    if args.careers_list:
        careers_by_class = Careers4()._careers_by_class
        print("Known careers: ")
        for classname, careers in careers_by_class.items():
            print("\t{:9s} - {}".format(classname, ', '.join(sorted(careers))))
        sys.exit()

    # Generate the base NPC with the specified species
    npc = BuildNPC4(args.species)

    # Add careers from the command line
    lastarg = ''        # Collect words and letters till we reach a number
    firstgood = False   # The rule for the first career is slightly different to the later ones
    for item in args.careerrank:
        # Numbers and letters
        numbers = [int(s) for s in item.split() if s.isdigit()]
        letters = re.sub("\d+", "", item)

        # Add letters to any previously collected letters
        if letters:
            lastarg += f' {letters}'

        # If there's a number trigger a new career rank
        if numbers:
            career = lastarg.strip().title()
            career = find_best_match(career,Careers4().careers) # allow misspellings

            if not firstgood:
                # First time through we use the specified number as the 1:number
                npc.add_career(career,numbers[0])
                firstgood = True
            else:
                # Otherwise we just use the digits
                for rank in list(str(numbers[0])):
                    npc.add_career_rank(career,int(rank))
            
            # Reset
            lastarg = ''

    # Print
    pretty_print_npc(npc, args.type) 

    return
    
    # Hospitaller Cristina González
    npc = Npc4("Estalian", 
               characteristics={"M":4, "WS":31, "BS":37, "S":30, "T":28, "I":36, "Agi":34, "Dex":28, "Int":29, "WP":30, "Fel":32},
               starting_skills={"Consume Alcohol":5, "Haggle":5, "Language (Brettonian)":3, "Lore (Estalia)":3, "Sail (Caravel)": 5, "Swim":3},
               starting_talents={"Linguistics", "Marksman", "Resistance (Mutation)", "Rover", "Very Strong"},
               starting_trappings={'Icon of Myrmidia'})
    npc.add_career("Soldier", 2)
    npc.add_career("Riverwarden", 1)
    npc.add_career("Knight", 2)
    npc.advance_skill("Lore (Reikland)", 5)
    # npc.advance_talent("Suave")   # Not sure how to implement this yet

    # Nicely formatted and if you examine the function you see which properties to use to access the NPC data
    pretty_print_npc(npc)

    # # Doktor Helga Langstrasse (the example NPC from Enemy in Shadows, p.144)
    npc = Npc4("human", randomise=False)
    npc.add_career("Scholar", 1)
    npc.add_career_rank("Physician", 2)
    npc.add_career_rank("Physician", 3)
    pretty_print_npc(npc)

if __name__ == "__main__":
    # execute only if run as a script
    main()
