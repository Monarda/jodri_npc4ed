__all__ = ["NPC4e", "Magic4e", "Job4e"]

from .src.magic4e import Magic4e
from .src.npc4e import NPC4e
from .src.job4e import Job4e
from .src.mutations4e import Mutations4e

## Backward compatibility
from .src.npc.buildNPC4 import BuildNPC4 as Npc4
from .src.npc.randomNPC4 import RandomNPC4
