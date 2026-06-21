import random

class CombatManager:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

        self.player_ap = player.ap
        self.enemy_ap = enemy.ap

    def calculate_hit_chance(self, attacker, defender):
        base_skill = 70
        chance = base_skill + (attacker.per * 2) - defender.ac
        return max(5, min(95, chance))

    def execute_attack(self, attacker, defender):
        weapon = attacker.equipped_weapon

        chance = self.calculate_hit_chance(attacker, defender)
        roll = random.randint(1, 100)

        if roll <= chance:
            damage = random.randint(weapon.min_damage, weapon.max_damage)

            crit_roll = random.randint(1, 100)
            if crit_roll <= attacker.crit_chance:
                damage *= 2
                print("Критический удар!")
            
            print(f" {attacker.name} наносит {damage} урона по {defender.name}")
            defender.current_hp -= damage
            if defender.current_hp < 0:
                defender.current_hp = 0
        else:
            print(f"{attacker.name} промахнулся!")

    def player_turn(self):
        while self.player_ap > 0 and self.enemy.current_hp > 0:

            cost = self.player.equipped_weapon.ap

            print(f"===== Ваш ход (Очки действия: {self.player_ap}) =====")
            print(f"Враг: {self.enemy.name} (Здоровье: {self.enemy.current_hp}/{self.enemy.max_hp})")
            print(f"1. Атаковать врага ({self.player.equipped_weapon.name}) (Цена: {cost} AP) \n2. Завершить ход")

            choice = input("Введите действие: ")
            print("=========================")

            if choice == "1":
                if self.player_ap >= cost:
                    self.player_ap -= cost
                    self.execute_attack(self.player, self.enemy)
                else:
                    print("Недостаточно очков действия для атаки!")
            elif choice == "2":
                print("Вы завершаете ход")
                break
            else:
                print("Введено неизвестное значение")
    
    def enemy_turn(self):
        if self.enemy.current_hp <= 0:
            return
        
        print(f"===== Ход врага: {self.enemy.name} =====")

        cost = self.enemy.equipped_weapon.ap

        while self.enemy_ap >= cost and self.player.current_hp > 0:
            self.enemy_ap -= cost
            self.execute_attack(self.enemy, self.player)
        print("=========================")