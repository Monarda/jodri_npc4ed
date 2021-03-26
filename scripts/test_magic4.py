import argparse
import random

from ..src.magic4 import *

def main():
    random.seed()

    parser = argparse.ArgumentParser(description="Generate spells from the specified lore")
    parser.add_argument("nospells", type=int)
    parser.add_argument("lore", nargs='+')
    parser.parse_args()
    args = parser.parse_args()
 
    m4 = Magic4()
    selection = find_best_match( ' '.join(args.lore),m4.lores )
    print('Colour: {}'.format(m4.iscolour(selection)))
    print('; '.join( m4.get_random_spells(selection,args.nospells) ))
    if (m4.error): print(m4.error)

    print(m4.miscast_minor())
    print()
    print(m4.miscast_major())
    print()

if __name__ == "__main__":
    # execute only if run as a script
    main()