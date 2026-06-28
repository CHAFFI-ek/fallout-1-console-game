from Fallout_Engine.inventory import Inventory
from Fallout_Engine.item import Weapon

class Player:
    def __init__(self, name, st, per, end, cha, inte, agi, luc, game_loop=None):
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

        self.level = 1
        self.xp = 0
        
        self.xp_next_level = int(((self.level + 1) * self.level) / 2) * 1000

        self.skill_points = 0

        self.skills = {
            "Легкое оружие": 30,
            "Скрытность": 20,
            "Воровство": 15
        }

        self.loop = game_loop

    def show_stats(self):
        print(f"===== Характеристики: {self.name.upper()} =====")
        print(f"Уровень: {self.level} | Опыт: {self.xp}/{self.xp_next_level} XP")
        print(f"Доступно очков навыков: {self.skill_points}")
        print(f"Здоровье (HP): {self.current_hp}/{self.max_hp}")
        print(f"Очки Действия (AP): {self.ap}")
        print("--------------------")
        print(f"Сила: {self.st}")
        print(f"Восприятие: {self.per}")
        print(f"Выносливость: {self.end}")
        print(f"Харизма: {self.cha}")
        print(f"Интеллект: {self.inte}")
        print(f"Ловкость: {self.agi}")
        print(f"Удача: {self.luc}")
    
    def add_xp(self, amount):
        if self.level >= 21:
            if self.loop: self.loop.add_log("Вы достигли максимального уровня (21)!")
            return
        
        self.xp += amount
        if self.loop:
            self.loop.add_log(f"Получено {amount} опыта (Текущий: {self.xp}/{self.xp_next_level} XP)")

        while self.xp >= self.xp_next_level and self.level < 21:
            self.level += 1

            added_skills = 5 + (2 * self.inte)
            self.skill_points += added_skills

            hp_gain = 3 + (self.end // 2)
            self.max_hp += hp_gain

            self.current_hp = self.max_hp

            if self.level < 21:
                self.xp_next_level = int(((self.level + 1) * self.level) / 2) * 1000
            else:
                self.xp_next_level = self.xp
            
            if self.loop:
                self.loop.add_log(f"Вы достигли {self.level} уровня!")
                self.loop.add_log(f"Максимальное здоровье увеличилось на +{hp_gain} (Теперь: {self.max_hp})")
                self.loop.add_log(f"Получено очков навыков: +{added_skills} (Всего доступно: {self.skill_points})")
                if self.level < 21:
                    self.loop.add_log(f"Следующий уровень на: {self.xp_next_level} XP")
                else:
                    self.loop.add_log("Вы достигли макс. уровня. Вы - легенда пустоши!")
