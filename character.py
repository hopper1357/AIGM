import item # Import the item module
import json # Import the json module

class Character:
    def __init__(self, name, race, strength, dexterity, constitution, intelligence, wisdom, charisma, inventory=None):
        self.name = name
        self.race = race
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        if inventory is None:
            self.inventory = {
                "equipped": {
                    "head": None,
                    "chest": None,
                    "ring": None,
                    "main_hand": None,
                    "off_hand": None,
                },
                "carried": []
            }
        else:
            self.inventory = inventory

    def equip_item(self, item_id):
        item_obj = item.get_item_by_id(item_id)
        if item_obj and item_obj.slot:
            # Remove from carried if present
            if item_id in self.inventory["carried"]:
                self.inventory["carried"].remove(item_id)
            
            # Unequip existing item in slot if any
            if self.inventory["equipped"][item_obj.slot]:
                self.inventory["carried"].append(self.inventory["equipped"][item_obj.slot])
            
            self.inventory["equipped"][item_obj.slot] = item_id
            return True
        return False

    def unequip_item(self, slot):
        if self.inventory["equipped"][slot]:
            item_id = self.inventory["equipped"][slot]
            self.inventory["equipped"][slot] = None
            self.inventory["carried"].append(item_id)
            return True
        return False

    def add_to_carried(self, item_id):
        self.inventory["carried"].append(item_id)

    def remove_from_carried(self, item_id):
        if item_id in self.inventory["carried"]:
            self.inventory["carried"].remove(item_id)
            return True
        return False

    def to_json(self):
        return json.dumps({
            "name": self.name,
            "race": self.race,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "charisma": self.charisma,
            "inventory": self.inventory
        })

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls(
            name=data["name"],
            race=data["race"],
            strength=data["strength"],
            dexterity=data["dexterity"],
            constitution=data["constitution"],
            intelligence=data["intelligence"],
            wisdom=data["wisdom"],
            charisma=data["charisma"],
            inventory=data["inventory"]
        )
