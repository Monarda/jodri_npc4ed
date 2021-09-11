## Note aliases listed at the bottom
species_default_playable = {"human", "dwarf", "halfling", "elf"}

species_npc_characteristics_4e = {
    "human":         {"M":4, "WS":30, "BS":30, "S":30, "T":30, "I":30, "Agi":30, "Dex":30, "Int":30, "WP":30, "Fel":30},
    "dwarf":         {"M":4, "WS":40, "BS":30, "S":30, "T":40, "I":30, "Agi":20, "Dex":40, "Int":30, "WP":50, "Fel":20},
    "halfling":      {"M":4, "WS":20, "BS":30, "S":20, "T":30, "I":30, "Agi":30, "Dex":40, "Int":30, "WP":40, "Fel":40},
    "elf":           {"M":5, "WS":40, "BS":40, "S":30, "T":30, "I":50, "Agi":40, "Dex":40, "Int":40, "WP":40, "Fel":30},
    "gnome":         {"M":3, "WS":30, "BS":20, "S":20, "T":25, "I":40, "Agi":40, "Dex":40, "Int":40, "WP":50, "Fel":25},
    "ogre":          {"M":6, "WS":30, "BS":20, "S":45, "T":45, "I":10, "Agi":25, "Dex":20, "Int":20, "WP":30, "Fel":20},
    "fimir":         {"M":6, "WS":35, "BS":20, "S":45, "T":40, "I":30, "Agi":20, "Dex":20, "Int":30, "WP":30, "Fel":15},
    "giant":         {"M":6, "WS":30, "BS":30, "S":65, "T":55, "I":30, "Agi":20, "Dex":15, "Int":25, "WP":25, "Fel":20},
    "troll":         {"M":6, "WS":30, "BS":15, "S":55, "T":45, "I":10, "Agi":15, "Dex":15, "Int":10, "WP":20, "Fel":5},
    "orc":           {"M":4, "WS":35, "BS":30, "S":35, "T":45, "I":20, "Agi":25, "Dex":20, "Int":25, "WP":35, "Fel":20},
    "goblin":        {"M":4, "WS":25, "BS":35, "S":30, "T":30, "I":20, "Agi":35, "Dex":30, "Int":30, "WP":20, "Fel":20},
    "vampire":       {"M":4, "WS":60, "BS":40, "S":50, "T":40, "I":50, "Agi":70, "Dex":40, "Int":40, "WP":60, "Fel":40},
    "gor":           {"M":4, "WS":45, "BS":30, "S":35, "T":45, "I":30, "Agi":35, "Dex":25, "Int":25, "WP":30, "Fel":25},
    "ungor":         {"M":4, "WS":35, "BS":30, "S":30, "T":35, "I":30, "Agi":35, "Dex":25, "Int":25, "WP":35, "Fel":25},
    "minotaur":      {"M":6, "WS":45, "BS":25, "S":44, "T":45, "I":20, "Agi":35, "Dex":25, "Int":20, "WP":30, "Fel":15},
    "bray-shaman":   {"M":4, "WS":40, "BS":30, "S":30, "T":45, "I":40, "Agi":35, "Dex":25, "Int":30, "WP":50, "Fel":30},
    "mutant":        {"M":4, "WS":30, "BS":30, "S":30, "T":30, "I":30, "Agi":30, "Dex":30, "Int":30, "WP":30, "Fel":30},
    "cultist":       {"M":4, "WS":30, "BS":30, "S":30, "T":30, "I":30, "Agi":30, "Dex":30, "Int":30, "WP":30, "Fel":30},
    "chaos warrior": {"M":4, "WS":55, "BS":30, "S":45, "T":45, "I":45, "Agi":55, "Dex":30, "Int":35, "WP":55, "Fel":25},
    "clanrat":       {"M":5, "WS":30, "BS":30, "S":30, "T":30, "I":40, "Agi":35, "Dex":30, "Int":30, "WP":20, "Fel":30},
    "stormvermin":   {"M":5, "WS":45, "BS":35, "S":35, "T":35, "I":55, "Agi":50, "Dex":30, "Int":30, "WP":25, "Fel":20},
    "rat ogre":      {"M":5, "WS":35, "BS":10, "S":55, "T":45, "I":35, "Agi":45, "Dex":25, "Int":10, "WP":25, "Fel":15},
}

species_npc_traits_4e = {
    "human": {'Prejudice (choose one)', 'Weapon +7'},
    "dwarf" : {'Animosity (choose one)', 'Hatred (Greenskins)', 'Magic Resistance (2)', 'Night Vision', 'Prejudice (choose one)', 'Weapon +7'},
    "halfling": {'Night Vision', 'Size (Small)', 'Weapon +5'},
    "elf": {'Animosity (choose one)', 'Prejudice (choose two)', 'Night Vision', 'Weapon +7'},
    "gnome": {'Night vision', 'Size (Small)', 'Weapon +7'},
    "ogre": {'Armour 1', 'Hungry', 'Prejudice (Thin People)', 'Night Vision', 'Size (Large)', 'Weapon +8'},
    "fimir": {'Armour 2', 'Cold-blooded', 'Night Vision', 'Size (Large)', 'Swamp-strider', 'Weapon +8'},
    "giant": {'Armour 1', 'Night Vision', 'Size (Enormous)', 'Stride', 'Tough', 'Weapon +10'},
    "troll": {'Armour 2', 'Bite+8', 'Die Hard', 'Infected', 'Regenerate', 'Size (Large)', 'Stupid', 'Tough', 'Vomit', 'Weapon +9'},
    "orc": {'Animosity (Greenskins)', 'Armour 3', 'Belligerent', 'Die Hard', 'Infected', 'Night Vision', 'Weapon +8'},
    "goblin": {'Animosity (Greenskins)', 'Armour 1', 'Afraid (Elves)', 'Night Vision', 'Infected', 'Weapon +7'},
    "vampire": {'Bite+8', 'Night Vision', 'Undead', 'Vampiric', 'Weapon +9'},
    "gor": {'Arboreal', 'Armour 1', 'Fury', 'Horns +6', 'Night Vision', 'Weapon +7'},
    "ungor": {'Arboreal', 'Night Vision', 'Weapon +6'},
    "minotaur": {'Horns +9', 'Hungry', 'Night Vision', 'Size (Large)', 'Weapon +9'},
    "bray-shaman": {'Arboreal', 'Corruption (Minor)', 'Fury', 'Horns +6', 'Night Vision', 'Spellcaster (Beasts, Any Chaos, Death, or Shadow)', 'Weapon +7'},
    "mutant": {'Corruption (Minor)', 'Mutation', 'Weapon +7'},
    "cultist": {'Weapon +6'},
    "chaos warrior": {'Armoured 5', 'Champion', 'Corruption (Minor)', 'Weapon +8'},
    "clanrat": {'Armour 2', 'Infected', 'Night Vision', 'Weapon +7'},
    "stormvermin": {'Armour 4', 'Infected', 'Night Vision', 'Weapon +8'},
    "rat ogre": {'Armour 1', 'Infected', 'Night Vision', 'Size (Large)', 'Stupid', 'Weapon +9'}
}

species_npc_optional_traits_4e = {
    "human": {'Disease', 'Ranged +8 (50)', 'Spellcaster'},
    "dwarf" : {'Fury', 'Ranged +8 (50)'},
    "halfling": {'Ranged +7 (25)', 'Stealthy'},
    "elf": {'Arboreal', 'Magical', 'Magical Resistance', 'Ranged+9 (150)', 'Stealthy', 'Spellcaster (any one)', 'Tracker'},
    "gnome": {'Spellcaster (Ulgu)'},
    "ogre" : {'Belligerent', 'Infected', 'Tracker'},
    "fimir": {'Armour 1', 'Night Vision', 'Size (Enormous)', 'Stride', 'Tough', 'Weapon +10'},
    "giant": {'Bestial', 'Breath (Drunken Vomit)', 'Hungry', 'Infected', 'Infestation', 'Size (Monstrous)', 'Stupid'},
    "troll": {'Amphibious', 'Bestial', 'Frenzy', 'Hungry', 'Infestation', 'Magic Resistance', 'Mutation', 'Night Vision', 'Painless', 'Stealthy', 'Swamp-strider'},
    "orc": {'Painless', 'Ranged+8 (50)', 'Size (Large)'},
    "goblin": {'Arboreal', 'Dark Vision', 'Hatred (Dwarfs)', 'Ranged+7 (25)', 'Venom'},
    "vampire": {'Bestial', 'Champion', 'Corruption (Minor)', 'Dark Vision', 'Die Hard', 'Distracting', 'Fear', 'Flight', 'Frenzy', 'Fury', 'Hungry', 'Mental Corruption', 'Painless', 'Petrifying Gaze', 'Regeneration', 'Spellcaster (Death or Necromancy)', 'Tracker', 'Wall Crawler'},
    "gor": {'Armour 2', 'Corruption (Minor)', 'Disease (Packer’s Pox)', 'Infected', 'Infestation', 'Mutation', 'Size (Large)', 'Spellcaster (Beasts)'},
    "ungor": {'Armour 1', 'Corruption (Minor)', 'Disease (Packer’s Pox)', 'Infected', 'Infestation', 'Mutation', 'Ranged+7 (25)', 'Size (Small)'},
    "minotaur": {'Arboreal', 'Belligerent', 'Corruption (Minor)', 'Disease (Packer’s Pox)', 'Fury', 'Infected', 'Infestation', 'Mutation'},
    "bray-shaman": {'Disease (Packer’s Pox)', 'Infected', 'Infestation', 'Mutation', 'Size (Large)'},
    "mutant": {'All Creature Traits'},
    "cultist": {'Armour 1', 'Corruption (Minor)', 'Mutation', 'Spellcaster (Chaos)'},
    "chaos warrior": {'Belligerent', 'Disease', 'Distracting', 'Frenzy', 'Mental Corruption', 'Mutation', 'Spellcaster (Chaos)'},
    "clanrat": {'Disease (Ratte Fever)', 'Mutation', 'Skittish', 'Stealthy', 'Tracker'},
    "stormvermin": {'Disease (Ratte Fever)', 'Mutation', 'Tracker'},
    "rat ogre": {'Corruption (Minor)', 'Dark Vision', 'Disease (Ratte Fever)', 'Infestation', 'Mutation', 'Tail+8', 'Tracker', 'Trained (Broken, Guard, Mount, War)'}
}

# Aliases
species_npc_aliases_4e = {
    'skaven' : 'clanrat'
}