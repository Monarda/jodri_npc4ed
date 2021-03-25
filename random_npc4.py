import random

from .src.npc.careers4 import Careers4
from .src.npc.buildNPC4 import *
from .src.npc.randomNPC4 import *
from .src.utility.find_best_match import find_best_match

def main():
    random.seed()

    import argparse
    parser = argparse.ArgumentParser(description="Generate a random WFRP4 NPC")
    parser.add_argument("--cl", action='store_true', help="List known species and quit.")
    parser.add_argument("--species", type=str, nargs='?',default='Human', 
                        help="""Species of NPC to create. Valid species are Human, Reiklander, Dwarf, 
                                Halfling, High Elf, Wood Elf, Gnome, Nordlander, Middenheimer, and Middenlander.
                                Default is human. Human will be randomly assigned to Reiklander, Nordlander, 
                                Middenheimer, or Middenlander.""")
    parser.add_argument("--type", choices=['combat','social','utility'], help="Remove information not relevant to this type of NPC")
    parser.add_argument("--young", help="Young NPCs have a lower probability of career ranks and changes", action='store_true')
    parser.add_argument("career", help="Final career for NPC. Multi-word arguments must be quoted.", type=str,nargs='?', default=None)
    parser.add_argument("level",help="Final career level for NPC",type=int,nargs='?',default=None)
    parser.parse_args()
    args = parser.parse_args()

    # Produce a list of valid careers, sorted by class
    if args.cl:
        careers_by_class = Careers4()._careers_by_class
        print("Known careers: ")
        for classname, careers in careers_by_class.items():
            print("\t{:9s} - {}".format(classname, ', '.join(sorted(careers))))
        sys.exit()

    # Check if we've been given a target career and level
    if args.career and args.level:
        career = find_best_match(args.career.title(),Careers4().careers)
        target = {"career":career,"rank":args.level}
    elif (args.career and not args.level) or (not args.career and args.level):
        print("Career and level must be input as a pair\n")
        parser.print_help()
        sys.exit()
    else:
        target=None

    # Generate a Wood Elf Ghost Strider
    #npc = RandomNPC4(species="Wood Elf",young=False,target={"career":"Ghost Strider","rank":2})
    
    # Generate NPC
    npc = RandomNPC4(species=args.species,young=args.young,target=target)
    pretty_print_npc(npc, args.type)


if __name__ == "__main__":
    # execute only if run as a script
    main()