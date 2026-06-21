from Fallout_Engine.special import Player 
from Fallout_Engine.locations import Sector
from Fallout_Engine.combat import CombatManager
from Fallout1_Game.monsters import cave_rat
from Fallout_Engine.item import Weapon

class Loop:
    def __init__(self):
        self.running = True
        self.state = "MAIN_MENU"
        self.points = 33
        self.st = 1
        self.per = 1
        self.end = 1
        self.cha = 1
        self.inte = 1
        self.agi = 1
        self.luc = 1
        self.player = None

        self.game_locations = {
            "Убежище 13": {
                "Пещера": Sector("Пещера убежища 13", "Темная и сырая пещара перед огромной Гермодверью с надписью 13")
            },
            "Убежище 15": {
                "Улица": Sector("Улица Убежища 15", "Какое-то заброшенное здание посреди пустыни, внутри явно что-то есть")
            },
            "Шэйди Сэндс": {
                "Улица": Sector("Улица Шэйди Сэндс", "Небольное поселение из песчанных кирпичей"),
                "Магазин": Sector("Магазин Шэйди Сэндс", "Торговый пост. На полках лежит довоенный товар, за прилавком хмурый торговец")
            }
        }

        self.world_map = {
            "Убежище 13": True,
            "Убежище 15": True,
            "Шэйди Сэндс": False
        }

        self.current_sector = None

    def run(self):
        while self.running:
            if self.state == "MAIN_MENU":
                print("===== Главное меню =====")
                print("1. Начать игру \n2. Загрузить игру \n3. Выйти из игры")
                choice = input("Введитие действие: ")
                print("=========================")
                if choice == "1":
                    self.state = "SPECIAL_CHOICE"
                elif choice == "2":
                    print("Пока недоступно")
                elif choice == "3":
                    self.running = False
                    break
                else:
                    print("Введено неизвестное значение")
            elif self.state == "EXPLORE":
                print(f"===== Локация: {self.current_sector.name} =====")
                if self.player is not None:
                    print(f"Ваше здоровье: {self.player.current_hp}/{self.player.max_hp}")
                print(self.current_sector.description)

                if hasattr(self.current_sector, 'enemies') and self.current_sector.enemies:
                    enemy_count = len(self.current_sector.enemies)
                    enemy_name = self.current_sector.enemies[0].name

                    print(f"Вокруг обноружены угрозы: {enemy_name} (Количество: {enemy_count})")
                    print(f"--> Доступно действие: 5. Напасть на ближайшего противника")

                if self.current_sector.name == "Улица Шэйди Сэндс":
                    print("--> 6. Войти в магазин")
                elif self.current_sector.name == "Магазин Шэйди Сэндс":
                    print("--> 6. Выйти на улицу")

                print("1. Открыть pip-boy 2000 \n2. Открыть инвентарь \n3. Глобальная карта \n4. Выйти в меню")
                choice1 = input("Введите действие: ")
                print("=========================")

                if choice1 == "1":
                    self.state = "PIP_BOY"
                elif choice1 == "2":
                    print("===== Инвентарь =====")
                    if not self.player.inventory.items:
                        print("Ваш рюкзак абсолютно пуст")
                    else:
                        print("Содержимое рюкзака:")
                        for index1, item in enumerate(self.player.inventory.items, 1):
                            print(f"{index1}. {item.name} (Вес: {item.weight} фунтов)")

                    total_w = self.player.inventory.get_total_weight()
                    print("-------------------------")
                    print(f"Общий вес: {total_w}/{self.player.max_weight} фунтов")
                    print("=========================")

                    if self.player.inventory.items:
                        print("Хотите осмотреть предмет? Введите его номер (или Enter чтобы закрыть инвентарь)")
                        choice_inv = input("> ")
                        if choice_inv.isdigit():
                            item_idx = int(choice_inv) - 1
                            if 0 <= item_idx < len(self.player.inventory.items):
                                selected_item = self.player.inventory.items[item_idx]
                                self.player.inventory.inspect_item(selected_item)
                            else:
                                print("Неверный номер")
                                
                elif choice1 == "3":
                    if hasattr(self.current_sector, 'enemies') and self.current_sector.enemies:
                        print("Вы не можете сбежать! Путь перекрыт врагами")
                    else:
                        self.state = "WORLD_MAP"
                elif choice1 == "4":
                    self.state = "MAIN_MENU"
                elif choice1 == "5" and hasattr(self.current_sector, 'enemies') and self.current_sector.enemies:
                    self.state = "COMBAT"
                    current_enemy = self.current_sector.enemies[0]
                    print(f"На вас напал {current_enemy.name}!")

                    combat = CombatManager(self.player, current_enemy)

                    while self.player.current_hp > 0 and current_enemy.current_hp > 0:
                        combat.player_turn()
                        combat.enemy_turn()

                        combat.player_ap = self.player.ap
                        combat.enemy_ap = current_enemy.ap

                    if self.player.current_hp <= 0:
                        print("Вы погибли в пустоши, вы отважно сражались, но пустошь оказалась слишком сильной для вас... Игра окончена")
                        self.state = "MAIN_MENU"
                    else:
                        print(f"Вы убили {current_enemy.name}!")
                        self.current_sector.enemies.remove(current_enemy)
                        self.state = "EXPLORE"

                elif choice1 == "6" and self.current_sector.name == "Улица Шэйди Сэндс":
                    self.current_sector = self.game_locations["Шэйди Сэндс"]["Магазин"]
                elif choice1 == "6" and self.current_sector.name == "Магазин Шэйди Сэндс":
                    self.current_sector = self.game_locations["Шэйди Сэндс"]["Улица"]
                else:
                    print("Введено неизвестное значение")

            elif self.state == "PIP_BOY":
                print("===== PIP-BOY 2000 =====")
                print("1. [STATUS] Характеристики персонажа")
                print("2. [DATA] Текстовые голодиски")
                print("3. [ALARM] Будильник и отдых")
                print("4. [CLOCK] Календарь и часы")
                print("5. [CLOSE] Назад в игру")
                choice_pip = input("Введите действие: ")
                print("=========================")
                if choice_pip == "1":
                    if self.player is not None:
                        self.player.show_stats()
                    else:
                        print("Ошибка! Персонаж еще не создан")
                elif choice_pip == "2":
                    print("Голодисков не найдено")
                elif choice_pip == "3":
                    print("В этой зоне отдых недоступен")
                elif choice_pip == "4":
                    print("Часы пока не работают")
                elif choice_pip == "5":
                    self.state = "EXPLORE"
                else:
                    print("Введено неизвестное значение")
            elif self.state == "SPECIAL_CHOICE":
                while True:
                    print("===== S.P.E.C.I.A.L =====")
                    print(f"Сила: {self.st} \nВосприятие: {self.per} \nВыносливость: {self.end} \nХаризма: {self.cha} \nИнтеллект: {self.inte} \nЛовкость: {self.agi} \nУдача: {self.luc}")
                    print(f"Осталось очков: {self.points}")
                    print("Выберите характеристику от 1 до 7. После распределения нажмите 8")
                    choice_spec = input("Введите действие: ")
                    print("=========================")
                    if choice_spec == "1":
                        print("===== S.P.E.C.I.A.L =====")
                        print("Сколько очков ходите добавить?")
                        new_val = int(input("Введите действие: "))
                        print("=========================")
                        if new_val < 1 or new_val > 10:
                            print("Ошибка! Характеристика должна быть от 1 до 10")
                            continue
                        diff = new_val - self.st
                        if diff <= self.points:
                            self.st = new_val
                            self.points -= diff
                            print(f"Сила теперь: {self.st}. Осталось очков: {self.points}")
                        else:
                            print("Ошибка! Недостаточно свободных очков")
                    elif choice_spec == "2":
                        print("===== S.P.E.C.I.A.L =====")
                        print("Сколько очков ходите добавить?")
                        new_val = int(input("Введите действие: "))
                        print("=========================")
                        if new_val < 1 or new_val > 10:
                            print("Ошибка! Характеристика должна быть от 1 до 10")
                            continue
                        diff = new_val - self.per
                        if diff <= self.points:
                            self.per = new_val
                            self.points -= diff
                            print(f"Восприятие теперь: {self.per}. Осталось очков: {self.points}")
                        else:
                            print("Ошибка! Недостаточно свободных очков")
                    elif choice_spec == "3":
                        print("===== S.P.E.C.I.A.L =====")
                        print("Сколько очков ходите добавить?")
                        new_val = int(input("Введите действие: "))
                        print("=========================")
                        if new_val < 1 or new_val > 10:
                            print("Ошибка! Характеристика должна быть от 1 до 10")
                            continue
                        diff = new_val - self.end
                        if diff <= self.points:
                            self.end = new_val
                            self.points -= diff
                            print(f"Выносливоть теперь: {self.end}. Осталось очков: {self.points}")
                        else:
                            print("Ошибка! Недостаточно свободных очков")
                    elif choice_spec == "4":
                        print("===== S.P.E.C.I.A.L =====")
                        print("Сколько очков ходите добавить?")
                        new_val = int(input("Введите действие: "))
                        print("=========================")
                        if new_val < 1 or new_val > 10:
                            print("Ошибка! Характеристика должна быть от 1 до 10")
                            continue
                        diff = new_val - self.cha
                        if diff <= self.points:
                            self.cha = new_val
                            self.points -= diff
                            print(f"Харизма теперь: {self.cha}. Осталось очков: {self.points}")
                        else:
                            print("Ошибка! Недостаточно свободных очков")
                    elif choice_spec == "5":
                        print("===== S.P.E.C.I.A.L =====")
                        print("Сколько очков ходите добавить?")
                        new_val = int(input("Введите действие: "))
                        print("=========================")
                        if new_val < 1 or new_val > 10:
                            print("Ошибка! Характеристика должна быть от 1 до 10")
                            continue
                        diff = new_val - self.inte
                        if diff <= self.points:
                            self.inte = new_val
                            self.points -= diff
                            print(f"Интеллект теперь: {self.inte}. Осталось очков: {self.points}")
                        else:
                            print("Ошибка! Недостаточно свободных очков")
                    elif choice_spec == "6":
                        print("===== S.P.E.C.I.A.L =====")
                        print("Сколько очков ходите добавить?")
                        new_val = int(input("Введите действие: "))
                        print("=========================")
                        if new_val < 1 or new_val > 10:
                            print("Ошибка! Характеристика должна быть от 1 до 10")
                            continue
                        diff = new_val - self.agi
                        if diff <= self.points:
                            self.agi = new_val
                            self.points -= diff
                            print(f"Ловкость теперь: {self.agi}. Осталось очков: {self.points}")
                        else:
                            print("Ошибка! Недостаточно свободных очков")
                    elif choice_spec == "7":
                        print("===== S.P.E.C.I.A.L =====")
                        print("Сколько очков ходите добавить?")
                        new_val = int(input("Введите действие: "))
                        print("=========================")
                        if new_val < 1 or new_val > 10:
                            print("Ошибка! Характеристика должна быть от 1 до 10")
                            continue
                        diff = new_val - self.luc
                        if diff <= self.points:
                            self.luc = new_val
                            self.points -= diff
                            print(f"Удача теперь: {self.luc}. Осталось очков: {self.points}")
                        else:
                            print("Ошибка! Недостаточно свободных очков")
                    elif choice_spec == "8":
                        if self.points == 0:
                            name = input("Введите имя вашего персонажа: ")
                            self.player = Player(name, self.st, self.per, self.end, self.cha, self.inte, self.agi, self.luc)
                            
                            self.player.equipped_weapon = Weapon("Кулаки", 0, 0, 1, 3, None, 3, "normal")

                            self.current_sector = self.game_locations["Убежище 13"]["Пещера"]

                            rat1 = cave_rat()
                            rat1.equipped_weapon = Weapon("Зубы", 0, 0, 1, 4, None, 4, "normal")
                            rat1.max_hp = 6
                            rat1.current_hp = 6

                            rat2 = cave_rat()
                            rat2.equipped_weapon = Weapon("Зубы", 0, 0, 1, 4, None, 4, "normal")
                            rat2.max_hp = 6
                            rat2.current_hp = 6

                            rat3 = cave_rat()
                            rat3.equipped_weapon = Weapon("Зубы", 0, 0, 1, 4, None, 4, "normal")
                            rat3.max_hp = 6
                            rat3.current_hp = 6

                            self.current_sector.enemies = [rat1, rat2, rat3]

                            self.state = "EXPLORE"
                            break
                        else:
                            print(f"Вы распределили не все очки! Осталось: {self.points}")
                    else:
                        print("Введено неизвестное значение")
            elif self.state == "WORLD_MAP":
                print("===== Глобальная карта =====")
                print("Доступные локации на радаре:")
                available_choices = []

                for loc_name, opened in self.world_map.items():
                    if opened:
                        available_choices.append(loc_name)

                for index, loc_name in enumerate(available_choices, 1):
                    print(f"{index}. Путешествовать в {loc_name}")

                back_button_index = len(available_choices) + 1
                print(f"{back_button_index}. Вернуться назад в текущую локацию")

                choice_map = input("Введите номер действия: ")
                print("=========================")

                if choice_map == str(back_button_index):
                    self.state = "EXPLORE"
                else:
                    chosen_location = None
                    for index, loc_name in enumerate(available_choices, 1):
                        if choice_map == str(index):
                            chosen_location = loc_name
                            break

                    if chosen_location == "Убежище 13":
                        self.current_sector = self.game_locations["Убежище 13"]["Пещера"]
                        self.state = "EXPLORE"

                    elif chosen_location == "Убежище 15":
                        if self.world_map["Шэйди Сэндс"] == False:
                            self.world_map["Шэйди Сэндс"] = True
                            print("Вы нашли новое поселение: Шэйди Сэндс")
                        
                        self.current_sector = self.game_locations["Убежище 15"]["Улица"]
                        self.state = "EXPLORE"

                    elif chosen_location == "Шэйди Сэндс":
                        self.current_sector = self.game_locations["Шэйди Сэндс"]["Улица"]
                        self.state = "EXPLORE"
                    else:
                        print("Неизвестное действие")

                
                    

                
        