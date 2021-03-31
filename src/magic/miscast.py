import random

from ...data import miscasts

def _miscast_template(miscast_table):
    """ Support function for miscasts """
    miscast_names = miscast_table[0::3]
    miscast_prob  = miscast_table[1::3]
    miscast_rules = miscast_table[2::3]

    miscast_result = random.choices(miscast_names, cum_weights=miscast_prob,k=1)[0]

    d10  = random.randint(1,10)
    d100 = random.randint(1,100)
    rolld10      = f'({d10})'
    rolld10again = f'({random.randint(1,10)})'
    rolld100     = f'({d100})'
    rolld10by5   = f'({d10}×5= {d10*5})'

    idx = miscast_names.index(miscast_result)
    miscast_text = f'**{miscast_result}**: {miscast_rules[idx]}'.format(rolld10=rolld10, rolld10again=rolld10again, rolld100=rolld100, rolld10by5=rolld10by5)

    return miscast_text, miscast_result


def miscast_minor() -> str:
    """ Return text describing a randomly rolled minor miscast. 
    
        Includes rerolls and escalations to major miscasts """
    miscast_text, miscast_result = _miscast_template(miscasts.magic_miscasts_minor)

    if miscast_result == 'Multiplying Misfortune':
        miscast_text += '\n\nRolling again twice:\n'
        miscast_text += _miscast_template(miscasts.magic_miscasts_minor[:-6])[0] + '\n'
        miscast_text += _miscast_template(miscasts.magic_miscasts_minor[:-6])[0] + '\n'

    if miscast_result == 'Cascading Chaos':
        miscast_text += '\n\nResult from Major Miscast Table:\n' + _miscast_template(miscasts.magic_miscasts_major)[0] + '\n'

    return miscast_text


def miscast_major() -> str:
    """ Return text describing a randomly rolled major miscast."""
    return _miscast_template(miscasts.magic_miscasts_major)[0]