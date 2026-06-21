from Fallout_Engine.special import Player

class NPC(Player):
    def __init__(self, name, st, per, end, cha, inte, agi, luc, is_hostile=True):
        super().__init__(name, st, per, end, cha, inte, agi, luc)

        self.is_hostile = is_hostile
        self.inventory = []
