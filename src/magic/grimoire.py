import random

from ..magic4e import Magic4e

grimoire_types = [80, 'book',
                  85, 'loose papers in a bag',
                  90, 'long scroll (lengthways)',
                  95, 'long scroll (widthways)',
                  100, 'box of scrolls (1 per spell) with belt']

grimoire_total_spells = [40, 3,
                         80, 4,
                         95, 5,
                         100, 6]

grimoire_max_cn = [30, 3,
                   50, 4,
                   60, 5,
                   70, 6,
                   80, 7,
                   85, 8,
                   90, 9,
                   95, 10,
                   100, 12]

grimoire_lore = [20, 'Arcane',
                 30, 'Petty',
                 40, 'Light',
                 50, 'Metal',
                 60, 'Life',
                 70, 'Heavens',
                 80, 'Shadows',
                 85, 'Death',
                 90, 'Fire',
                 95, 'Beasts',
                 97, 'Necromancy',
                 98, 'Witchcraft',
                 100, 'Chaos']

grimoire_characteristic_one = [30, 'Includes Arcane and/or Petty spells.',
                               40, 'Poorly Written – The text is difficult to read. Increase the CN of spells by 1.',
                               50, 'Terribly Written – The text is difficult to read. Increase the CN of spells by 1 and they cost an additional 50 XP to memorise.',
                               60, 'The spell is written with elegance and clarity and is easier to cast. Reduce the CN by 1, after doubling for grimoire casting.',
                               70, 'The wizard has kept neat notes on the processes behind learning the spells. Reduce the XP to memorise the spells by 50.',
                               80, 'Contains numerous other notes — secrets, clues to treasure, or just nonsense ramblings.',
                               85, 'Coded — The spells are written in code that must be deciphered before being cast or memorised (Extended Secret Signs Test to a total of 40 SL per spell).',
                               90, 'Fake — The grimoire looks legitimate but is the work of a trickster.',
                               95, 'Incomplete — Some or all of the spells are unfinished or have key words missing. The spells can be completed with an Extended Challenging (+0) Research Test to a total of 20 SL per spell.',
                               100, 'Damaged — Only the spells are legible.'
                              ]

grimoire_characteristic_two = [20, 'Wrapped in treated leather to protect from fire, water, and other sources of damage.',
                               30, 'The grimoire is locked.',
                               40, 'The grimoire is locked and protected by a magical alarm.',
                               50, 'The cover is highly decorated with jewels, engravings, and so on.',
                               60, 'Stolen — The grimoire is being hunted by its owner.',
                               70, 'Bound in unusual material such as skin or hide from an unusual creature.',
                               80, 'Sheets made of material other than paper. For example, vellum, metal, or skin.',
                               85, 'Renowned — The grimoire is well known, either for its content or owner.',
                               90, 'Corrupting Influence — A small amount of powdered Warpstone has been sewn into the spine.',
                               95, 'Trapped — for example, poison has been placed on small needles in the spine or pasted onto the pages. Very Hard (-30) Perception Test to spot before the trap is triggered.',
                               100, 'Roll two more times.',
                              ]

def random_grimoire():
    type   = random.choices(grimoire_types[1::2], 
                            cum_weights=grimoire_types[0::2],k=1)[0]
    number = random.choices(grimoire_total_spells[1::2], 
                            cum_weights=grimoire_total_spells[0::2],k=1)[0]
    max_cn = random.choices(grimoire_max_cn[1::2], 
                            cum_weights=grimoire_max_cn[0::2],k=1)[0]

    lore   = random.choices(grimoire_lore[1::2], 
                            cum_weights=grimoire_lore[0::2],k=1)[0]
    m4 = Magic4e()
    if lore == 'Arcane':
        arcane_lore = random.choices(['Light', 'Metal', 'Life', 'Heavens', 'Shadows', 'Death', 'Fire', 'Beasts'])[0]
        arcane_lore = m4.canonise_lore(arcane_lore)
        lore = 'arcane lore'
    if lore == 'Petty':
        lore = 'petty lore'

    lore = m4.canonise_lore(lore)

    if lore == 'arcane lore':
        lore = f'arcane lore ({arcane_lore.title()})'

    spells = ', '.join(m4.get_random_spells(lore, number, max_cn).keys())

    char1 = random.choices(grimoire_characteristic_one[1::2], 
                            cum_weights=grimoire_characteristic_one[0::2],k=1)[0]
    char2 = random.choices(grimoire_characteristic_two[1::2], 
                            cum_weights=grimoire_characteristic_two[0::2],k=1)[0]
    if char2 == 'Roll two more times.':
        char2 = random.choices(grimoire_characteristic_two[1::2][0:-1], 
                                cum_weights=grimoire_characteristic_two[0::2][0:-1],k=2)
        char2 = ' '.join(char2)

    grimoire = f'A {type} containing {number} spells, with a max CN of {max_cn}, from {lore.title()}.\nThe spells are {spells}.\n{char1}\n{char2}'

    return grimoire