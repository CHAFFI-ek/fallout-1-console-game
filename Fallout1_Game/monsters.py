from Fallout_Engine.npc import NPC

def cave_rat():
    rat = NPC(
        name="Пещерная крыса",
        st=2, per=4, end=2, cha=1, inte=1, agi=6, luc=3,
        is_hostile=True
    )

    rat.max_hp = 6
    rat.current_hp = 6

    return rat
