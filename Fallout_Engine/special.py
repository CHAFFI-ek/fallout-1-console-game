from Fallout_Engine.inventory import Inventory
from Fallout_Engine.item import Weapon

class Player:
    def __init__(self, name, st, per, end, cha, inte, agi, luc):
        self.st = st
        self.per = per
        self.end = end
        self.cha = cha
        self.inte = inte
        self.agi = agi
        self.luc = luc
        self.name = name
        self.inventory = Inventory()
        self.equipped_weapon = Weapon("Кулаки", weight=0, price=0, min_damage=1, max_damage=3, ammo_type=None, ap=3, damage_type="normal")

        self.max_hp = 15 + self.st + (self.end * 2)
        self.current_hp = self.max_hp
        self.ap = 5 + (self.agi // 2)
        self.max_weight = 25 + (25 * self.st)
        self.crit_chance = self.luc
        self.sub = self.per * 2
        self.sp = 5 * (self.inte * 2)
        self.ac = self.agi

    def show_stats(self):
        print(f"Сила: {self.st}")
        print(f"Восприятие: {self.per}")
        print(f"Выносливость:{self.end}")
        print(f"Харизма: {self.cha}")
        print(f"Интеллект: {self.inte}")
        print(f"Ловкость: {self.agi}")
        print(f"Удача: {self.luc}")