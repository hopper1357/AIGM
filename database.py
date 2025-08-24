import sqlite3
from character import Character # Import Character class

def initialize_database():
    conn = sqlite3.connect('/home/dell/gemini_projects/AIGM/data/game.db')
    cursor = conn.cursor()

    # Create players table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            character_data TEXT,
            location TEXT
        )
    ''')

    # Create world_state table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS world_state (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    # Create items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT,
            class TEXT,
            subclass TEXT,
            rarity TEXT DEFAULT 'common',
            description TEXT,
            damage TEXT,
            damage_type TEXT,
            armor_class INTEGER,
            slot TEXT,
            weight REAL DEFAULT 0,
            value INTEGER DEFAULT 0,
            effect TEXT,
            uses INTEGER DEFAULT 1,
            duration TEXT,
            magical INTEGER DEFAULT 0,
            enchantment TEXT,
            requirements TEXT,
            material TEXT,
            quality TEXT
        )
    ''')

    conn.commit()
    conn.close()

def add_item(item_data):
    conn = sqlite3.connect('/home/dell/gemini_projects/AIGM/data/game.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO items (
            name, class, subclass, rarity, description, damage, damage_type, 
            armor_class, slot, weight, value, effect, uses, duration, magical, 
            enchantment, requirements, material, quality
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        item_data.get('name'), item_data.get('class'), item_data.get('subclass'),
        item_data.get('rarity'), item_data.get('description'), item_data.get('damage'),
        item_data.get('damage_type'), item_data.get('armor_class'), item_data.get('slot'),
        item_data.get('weight'), item_data.get('value'), item_data.get('effect'),
        item_data.get('uses'), item_data.get('duration'), item_data.get('magical'),
        item_data.get('enchantment'), item_data.get('requirements'), item_data.get('material'),
        item_data.get('quality')
    ))
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id

def save_character(character):
    conn = sqlite3.connect('/home/dell/gemini_projects/AIGM/data/game.db')
    cursor = conn.cursor()
    character_json = character.to_json()
    cursor.execute("INSERT OR REPLACE INTO players (id, name, character_data, location) VALUES (?, ?, ?, ?)",
                   (1, character.name, character_json, "tavern")) # Using a fixed ID for now
    conn.commit()
    conn.close()

def load_character(player_id):
    conn = sqlite3.connect('/home/dell/gemini_projects/AIGM/data/game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT character_data FROM players WHERE id = ?", (player_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return Character.from_json(result[0])
    return None