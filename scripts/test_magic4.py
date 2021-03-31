import argparse
import random

from ..src.magic4e import *

def main():
    random.seed()

    parser = argparse.ArgumentParser(description="Generate spells from the specified lore")
    parser.add_argument("nospells", type=int)
    parser.add_argument("lore", nargs='+')
    parser.parse_args()
    args = parser.parse_args()
 
    m4 = Magic4e()
    selection = m4.canonise_lore( ' '.join(args.lore)).title()
    print(f'{args.nospells} spells selected randomly from {selection}:')
    print('; '.join( m4.get_random_spells(selection,args.nospells) ))
    if (m4.error): print(m4.error)

    print('\nMinor Miscast:')
    for i in range(20):
        print(m4.miscast_minor())
    print('\nMajor Miscast:')
    print(m4.miscast_major())
    print()

if __name__ == "__main__":
    # execute only if run as a script
    main()