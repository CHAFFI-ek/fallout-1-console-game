from Fallout_Engine.item import Weapon, Armor, Consumable, Item

class Inventory:
    def __init__(self):
        self.items = []

    def get_total_weight(self):
        total = 0
        for item in self.items:
            total += item.weight
        return total
    
    def add_item(self, new_item, player):
        predicted_weight = self.get_total_weight() + new_item.weight

        if predicted_weight <= player.max_weight:
            self.items.append(new_item)
            print(f"Предмет '{new_item.name}' добавлен в инвентарь")
        else:
            print("Вы перегружены и не можете это поднять")

    def inspect_item(self, item):
        if isinstance(item, Weapon):
            print(f"{item.name} | Урон: {item.min_damage}-{item.max_damage} | Тип урона: {item.damage_type} | Вес: {item.weight} фунтов")
        elif isinstance(item, Armor):
            print(f"{item.name} | Защита: +{item.ac} | Вес: {item.weight} фунтов")
        else:
            print(f"{item.name} | Вес: {item.weight} фунтов")

    def drop_item(self, item):
        if item.is_quest == True:
            print("Этот предмет нельзя выбросить")
        else:
            self.items.remove(item)

    def unload_weapon(self, weapon):
        pass

    def reload_weapon(self):
        pass

    def use_item(self, item, player):
        if isinstance(item, Consumable):
            player.current_hp += item.heal

            if player.current_hp > player.max_hp:
                player.current_hp = player.max_hp
    
            self.items.remove(item)
            print(f"Вы использовали {item.name} и восстановили {item.heal}")
        


