# Uses cumulative probability so we can keep the order if that's ever needed
magic_miscasts_minor = [
    'Witchsign', 5, 'the next living creature born within 1 mile is mutated.',
    'Soured Milk', 10, 'All milk within 1d100 yards {rolld100} goes sour instantly.',
    'Blight', 15, 'Willpower Bonus fields within Willpower Bonus miles suffer a blight, and all crops rot overnight.',
    'Soulwax', 20, 'Your ears clog instantly with a thick wax. Gain 1 *Deafened* Condition, which is not removed until someone cleans them for you (with a successful use of the Heal Skill).',
    'Witchlight', 25, 'You glow with an eerie light related to your Lore, emitting as much light as a large bonfire, which lasts for 1d10 {rolld10} Rounds.',
    'Fell Whispers', 30, 'Pass a **Routine (+20) Willpower Test** or gain 1 Corruption point.',
    'Rupture', 35, 'Your nose, eyes, and ears bleed profusely. Gain 1d10 {rolld10} Bleeding Conditions.',
    'Soulquake', 40, 'Gain the *Prone* Condition.',
    'Unfasten', 45, 'On your person, every buckle unfastens, and every lace unties, which may cause belts to fall, pouches to open, bags to fall, and armour to slip.',
    'Wayward Garb', 50, 'your clothes seem to writhe with a mind of their own. Receive 1 *Entangled* Condition with a Strength of 1d10×5 {rolld10by5} to resist.',
    'Curse of Temperance', 55, 'All alcohol within 1d100 {rolld10} yards goes bad, tasting bitter and foul.',
    'Souldrain', 60, 'Gain 1 *Fatigued* Condition, which remains for 1d10 {rolld10} hours.',
    'Driven to Distraction', 65, 'If engaged in combat, gain the *Surprised* Condition. Otherwise, you are completely startled, your heart racing, and unable to concentrate for a few moments.',
    'Unholy Visions', 70, 'Fleeting visions of profane and unholy acts harass you. Receive a *Blinded* Condition; pass a **Challenging (+0) Cool Test** or gain another.',
    'Cloying Tongue', 75, 'All Language Tests (including Casting Tests) suffer a –10 penalty for 1d10 {rolld10} Rounds.',
    'The Horror!', 80, 'Pass a **Hard (–20) Cool Test** or gain 1 *Broken* Condition.',
    'Curse of Corruption', 85, 'Gain 1 Corruption point.',
    'Double Trouble', 90, 'The effect of the spell you cast occurs elsewhere within 1d10 {rolld10} miles. At the GM’s discretion, where possible it should have consequences.',
    'Multiplying Misfortune', 95, 'Roll twice on this table, rerolling any results between 91-00.',
    'Cascading Chaos', 100, 'Roll again on the Major Miscast Table.'
]

magic_miscasts_major = [
    'Ghostly Voices', 5, """Everyone within Willpower yards hears darkly seductive whispering of voices emanating from
the Realm of Chaos. All sentient creatures must pass an **Average (+20) Cool Test** or gain 1 Corruption point.""",
    'Hexeyes:', 10, """Your eyes turn an unnatural colour associated with your Lore for 1d10 {rolld10} hours. While your eyes are
discoloured, you have 1 *Blinded* Condition that cannot be resolved by *any* means.""",
    'Aethyric Shock:', 15, """you suffer 1d10 {rolld10} wounds, ignoring your Toughness Bonus and Armour Points. Pass an **Average
(+20) Endurance Test**, or also gain a *Stunned* Condition.""",
    'Death Walker', 20, """Your footsteps leave death in their wake. For the next 1d10 {rolld10} hours, any plant life near you withers
and dies.""",
    'Intestinal Rebellion', 25, """Your bowels move uncontrollably, and you soil yourself. Gain 1 *Fatigued* Condition,
which cannot be removed until you can change your clothes and clean yourself up.""",
    'Soulfire:', 30, """Gain an *Ablaze* Condition, as you are wreathed in unholy flames with a colour associated with your
Lore.""",
    'Speak in Tongues', 35, """You gabble unintelligibly for 1d10 {rolld10} rounds. During this time, you cannot communicate
verbally, or make any Casting Tests, although you may otherwise act normally.""",
    'Swarmed:', 40, """You are engaged by a swarm of aethyric Rats, Giant Spiders, Snakes, or similar (GM’s choice). Use
the standard profiles for the relevant creature type, adding the *Swarm* Creature Trait. After 1d10 {rolld10} rounds, if not
yet destroyed, the swarm retreats.""",
    'Ragdoll:', 45, """You are flung 1d10 {rolld10} yards through the air in a random direction, taking 1d10 {rolld10} wounds on landing,
ignoring Armour Points, and receiving the *Prone* Condition.""",
    'Limb frozen', 50, """One limb (randomly determined) is frozen in place for 1d10 {rolld10} hours. The limb is useless, as if it had
been Amputated (see page 180).""",
    'Darkling Sight', 55, """You lose the benefit of the *Second Sight* Talent for 1d10 {rolld10} hours. Channelling Tests also suffer a
penalty of –20 for the duration.""",
    'Chaotic Foresight', 60, """Gain a bonus pool of 1d10 {rolld10} Fortune points (this may take you beyond your natural limit).
Every time you spend one of these points, gain 1 Corruption point. Any of these points remaining at the end of
the session are lost.""",
    'Levitation:', 65, """You are borne aloft on the Winds of Magic, floating 1d10 {rolld10} yards above the ground for 1d10 {rolld10} minutes.
Other characters may forcibly move you, and you may move using spells, wings or similar, but will continually
return to your levitating position if otherwise left alone. Refer to the Falling rules (see page 166) for what
happens when Levitation ends.""",
    'Regurgitation:', 70, """You spew uncontrollably, throwing up far more foul-smelling vomitus than your body can
possibly contain. Gain the *Stunned* Condition, which lasts for 1d10 {rolld10} Rounds.""",
    'Chaos Quake', 75, """All creatures within 1d100 {rolld100} yards must pass an **Average (+20) Athletics Test** or gain the *Prone*
Condition.""",
    'Traitor’s Heart', 80, """The Dark Gods entice you to commit horrendous perfidy. Should you attack or otherwise
betray an ally to the full extent of your capabilities, regain all Fortune points. If you cause another character to
lose a Fate Point, gain +1 Fate Point.""",
    'Foul Enfeeblement', 85, "Gain 1 Corruption point, the *Prone* Condition, and a *Fatigued* Condition",
    'Hellish Stench', 90, """You now smell really bad! You gain the *Distracting* Creature Trait (see page 339), and probably
the enmity of anyone with a sense of smell. This lasts for 1d10 {rolld10} hours.""",
    'Power Drain', 95, """You are unable to use the Talent used to cast the spell (usually *Arcane Magic*, though it could be
*Chaos Magic*, or a similar Talent), for 1d10 {rolld10} minutes.""",
    'Aethyric Feedback', 100, """Everyone within a number of yards equal to your Willpower Bonus — friend and foe alike
— suffers 1d10 {rolld10} wounds, ignoring Toughness Bonus and Armour Points, and receives the *Prone* Condition. If
there are no targets in range, the magic has nowhere to vent, so your head explodes, killing you instantly.""",
]
for i in range(2,len(magic_miscasts_major),3):
    magic_miscasts_major[i] = magic_miscasts_major[i].replace('\n',' ')