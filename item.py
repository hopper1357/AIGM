import sqlite3

class Item:
    def __init__(self, item_data):
        self.id = item_data[0]
        self.name = item_data[1]
        self.item_class = item_data[2]
        self.subclass = item_data[3]
        self.rarity = item_data[4]
        self.description = item_data[5]
        self.damage = item_data[6]
        self.damage_type = item_data[7]
        self.armor_class = item_data[8]
        self.slot = item_data[9]
        self.weight = item_data[10]
        self.value = item_data[11]
        self.effect = item_data[12]
        self.uses = item_data[13]
        self.duration = item_data[14]
        self.magical = item_data[15]
        self.enchantment = item_data[16]
        self.requirements = item_data[17]
        self.material = item_data[18]
        self.quality = item_data[19]

def get_item_by_id(item_id):
    conn = sqlite3.connect('/home/dell/gemini_projects/AIGM/data/game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item_data = cursor.fetchone()
    conn.close()
    if item_data:
        return Item(item_data)
    return None
