import copy, json
import importlib.resources
import random

from .. import data
with importlib.resources.open_text(data,'mutations.json') as f:
#with open('C:\Development\Python\monarda_bot\data\mutations.json', 'r') as f:
    _mutations_data = json.load(f)

class Mutations4e:
    """ Class to contain all commands and related information for 4th ed mutations (Corebook, 183; 
        Enemy in Shadows Companion, Chapter 8) """

    def __init__(self):

        self._physical_mutations  = self._prep_mutation_type('physical')
        self._beast_head_mutation = self._prep_mutation_type('beast head')
        self._mental_mutations    = self._prep_mutation_type('mental')
        
        self._fixations = {'mutation':list(_mutations_data['fixations'].keys()),
                           'k':       list(_mutations_data['fixations'].values())}

    def _prep_mutation_type(self, type):
        mutations = {'any': {'mutation':[], 'k':[]}, 
                     'khorne':   {'mutation':[], 'k':[]}, 
                     'nurgle':   {'mutation':[], 'k':[]}, 
                     'slaanesh': {'mutation':[], 'k':[]}, 
                     'tzeentch': {'mutation':[], 'k':[]}
                    }

        for mutation, probs in _mutations_data[type].items():
            for k,v in probs.items():
                mutations[k.lower()]['mutation'].append(mutation)
                mutations[k.lower()]['k'].append(v)
        
        return mutations


    def physical(self, god='any'):
        """ Returns a physical mutation, randomly selected from the table in Enemy in Shadows Companion, Chapter 8.
        If the Chaos god is not specified, then 'any' will be used.
        """

        god = god.lower()

        mutation = random.choices( self._physical_mutations[god]['mutation'], self._physical_mutations[god]['k'] )[0]

        if (mutation=='Beast Head'):
            head = random.choices(self._beast_head_mutation[god]['mutation'], self._beast_head_mutation[god]['k'])[0]
            mutation = f'{mutation} ({head})'

        return mutation

    def mental(self, god='any'):
        """ Returns a mental mutation, randomly selected from the table in Enemy in Shadows Companion, Chapter 8.
        If the Chaos god is not specified, then 'any' will be used.
        """
        
        god = god.lower()

        mutation = random.choices( self._mental_mutations[god]['mutation'], self._mental_mutations[god]['k'] )[0]

        if mutation == 'Terrible Phobia':
            mutation = f'{mutation} ({self.fixation()})'

        return mutation

    def fixation(self):
        return random.choices( self._fixations['mutation'], self._fixations['k'] )[0]

    def mutation(self, species='human', god='any'):
        """ Returns a physical or mental mutation, randomly  determining the type based on the table on corebook
        p.183 and then the exact mutation selected from the table in Enemy in Shadows Companion, Chapter 8.
        If the species is not specified, then 'human' will be used (i.e. 50/50 change of physical or mental mutation)
        If the Chaos god is not specified, then 'any' will be used.
        """

                            # species: [physical, mental]
        species_prob_chart = {'elf':      [0, 100],
                              'halfling': [10, 90],
                              'human':    [50, 50],
                              'dwarf':    [ 5, 95]
                             } 
        type = random.choices( ['physical', 'mental'], species_prob_chart[species])[0]
        if type=='physical':
            return self.physical(god)
        else: 
            return self.mental(god)

def main():
    m4 = Mutations4e()

    print('Physical mutation: ', m4.physical('Tzeentch'))
    print('Mental mutation:   ',m4.mental('Slaanesh'))
    print('Fixation:          ',m4.fixation())

    print('Fully random:      ', m4.mutation())

if __name__ == "__main__":
    # execute only if run as a script
    main()