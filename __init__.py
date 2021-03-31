__all__ = ["npc4e", "magic4e", ]

from .src.magic4e import Magic4e
from .src.npc4e import NPC4e

## Backward compatibility
from .src.npc.buildNPC4 import BuildNPC4 as Npc4
from .src.npc.randomNPC4 import RandomNPC4
