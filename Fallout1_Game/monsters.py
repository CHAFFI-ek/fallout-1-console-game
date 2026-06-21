from Fallout_Engine.npc import NPC
from Fallout_Engine.item import Weapon

def cave_rat():
    rat = NPC(
        name="Пещерная крыса",
        st=2, per=4, end=2, cha=1, inte=1, agi=6, luc=3,
        is_hostile=True
    )

    rat.max_hp = 6
    rat.current_hp = 6
    rat.equipped_weapon = Weapon("Зубы", weight=0, price=0, min_damage=1, max_damage=4, ammo_type=None, ap=4, damage_type="normal")

    return rat
