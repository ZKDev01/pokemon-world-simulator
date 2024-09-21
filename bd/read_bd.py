import sqlite3
import json

def read_areas():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Areas')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_locations():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Locations')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_pokemon_encounters():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pokemon_Encounter')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_encounter_methods():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Encounter_Methods')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_areaxencounter_methods():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM AreaXEncounter_Method')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_pokemon():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pokemons')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_habitats():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Habitats')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_abilities():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Abilities')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_pokemon_abilities():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pokemon_Abilities')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_effects():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Effects')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_moves():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Moves')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_pokemon_moves():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pokemon_Moves')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_egg_groups():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Egg_Groups')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_pokemon_egg_groups():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pokemon_Egg_Groups')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_evolutions():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Evolution')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_pokemon_evolutions():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pokemon_Evolution')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_items():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Items')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_pokemon_held_items():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pokemon_held_Items')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_types():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Types')
    rows = cursor.fetchall()
    conn.close()
    return rows

def read_pokemon_types():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pokemon_Types')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_areas():
    return read_areas()

def get_locations():
    return read_locations()

def get_pokemon_encounters():
    return read_pokemon_encounters()

def get_encounter_methods():
    return read_encounter_methods()

def get_area_encounter_methods():
    return read_areaxencounter_methods()

def get_pokemons():
    return read_pokemon()

def get_habitats():
    return read_habitats()

def get_abilities():
    return read_abilities()

def get_pokemon_abilities():
    return read_pokemon_abilities()

def get_effects():
    return read_effects()

def get_moves():
    return read_moves()

def get_pokemon_moves():
    return read_pokemon_moves()

def get_egg_groups():
    return read_egg_groups()

def get_pokemon_egg_groups():
    return read_pokemon_egg_groups()

def get_evolutions():
    return read_evolutions()

def get_pokemon_evolutions():
    return read_pokemon_evolutions()

def get_items():
    return read_items()

def get_pokemon_held_items():
    return read_pokemon_held_items()

def get_types():
    return read_types()

def get_pokemon_types():
    return read_pokemon_types()

def get_all():
    return read_areas(), read_locations(), read_pokemon_encounters(), read_encounter_methods(), read_areaxencounter_methods(), read_pokemon(), read_habitats(), read_abilities(), read_pokemon_abilities(), read_effects(), read_moves(), read_pokemon_moves(), read_egg_groups(), read_pokemon_egg_groups(), read_evolutions(), read_pokemon_evolutions(), read_items(), read_pokemon_held_items(), read_types(), read_pokemon_types()

def get_move(id):
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM Moves WHERE id = {id}')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_pokemon_move_at_lvl(pokemon_id):
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT pokemon_id, move_id, learned_at_level FROM Pokemon_Moves WHERE pokemon_id = {pokemon_id}')
    rows = cursor.fetchall()
    conn.close()
    return rows
    
def get_growth_rate_data():
    with open('growth_rate_data.json', 'r') as file:
        growth_rate_data = json.load(file)   
    return growth_rate_data

# areas = read_areas()
# locations = read_locations()
# pokemon_encounters = read_pokemon_encounters()
# encounter_methods = read_encounter_methods()
# areaxencounter_methods = read_areaxencounter_methods()
# pokemon = read_pokemon()
