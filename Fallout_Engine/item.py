class Item:
    def __init__(self, name, weight, price):
        self.name = name
        self.weight = weight
        self.price = price
        self.is_quest = False

class Consumable(Item):
    def __init__(self, name, weight, price, heal, rad_resist):
        super().__init__(name, weight, price)
        self.heal = heal
        self.rad_resist = rad_resist

class Weapon(Item):
    def __init__(self, name, weight, price, min_damage, max_damage, ammo_type, ap, damage_type):
        super().__init__(name, weight, price)
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.ammo_type = ammo_type
        self.ap = ap
        self.damage_type = damage_type

class Armor(Item):
    def __init__(self, name, weight, price, ac):
        super().__init__(name, weight, price)
        self.ac = ac

        self.dt = {
            "normal": 0, "laser": 0, "plasma": 0, "explode": 0, "electrical": 0, "fire": 0
        }
        
        self.dr = {
            "normal": 0, "laser": 0, "plasma": 0, "explode": 0, "electrical": 0, "fire": 0
        }

class QuestItem(Item):
    def __init__(self, name, price):
        super().__init__(name, 0, price)
        self.is_quest = True