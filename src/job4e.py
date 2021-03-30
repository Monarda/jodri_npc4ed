import importlib.resources
import json
import random
from typing import List

from .. import data
with importlib.resources.open_text(data,'jobs.json') as f:
    _job_data = json.load(f)

class Job4e():
    """ Create a job from the 4th ed GM screen booklet random roll tables """
    def __init__(self):
        pass

    def get(self) -> List[str]:
        """ Return a list of who, what, and why strings"""
        
        who  = random.choices(_job_data["who"])[0]
        what = random.choices(_job_data["what"])[0]
        why  = random.choices(_job_data["why"])[0]

        return [who, what, why]

def main():
    print( '\n'.join(Job4e().get()) )

if __name__ == "__main__":
    # execute only if run as a script
    main()