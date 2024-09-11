import sqlite3

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

    
# areas = read_areas()
# locations = read_locations()
# pokemon_encounters = read_pokemon_encounters()
# encounter_methods = read_encounter_methods()
# areaxencounter_methods = read_areaxencounter_methods()
# pokemon = read_pokemon()
