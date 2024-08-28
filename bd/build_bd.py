import sqlite3

#Create data base
conn = sqlite3.connect('pokedex.db')
cursor = conn.cursor()

#Create table Pokemons
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pokemons(
    id INTEGER PRIMARY KEY,
    name TEXT,
    height INTEGER,
    weight INTEGER,
    base_experience INTEGER,
    growth_rate TEXT,
    generation INTEGER,
    hp INTEGER,
    attack INTEGER,
    defense INTEGER,
    special_attack INTEGER,
    special_defense INTEGER,
    speed INTEGER
)
''')

#Create table Types
cursor.execute('''
CREATE TABLE IF NOT EXISTS Types(
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

#Create table Pokemon_Types
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pokemon_Types(
    pokemon_id INTEGER,
    type_id INTEGER,
    FOREIGN KEY(pokemon_id) REFERENCES Pokemons(id),
    FOREIGN KEY(type_id) REFERENCES Types(id)
)
''')

#Create table Abilities
cursor.execute('''
CREATE TABLE IF NOT EXISTS Abilities(
    id INTEGER PRIMARY KEY,
    name TEXT,
    effect TEXT
)
''')

#Create table Pokemon_Abilities
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pokemon_Abilities(
    pokemon_id INTEGER,
    ability_id INTEGER,
    FOREIGN KEY(pokemon_id) REFERENCES Pokemons(id),
    FOREIGN KEY(ability_id) REFERENCES Abilities(id)
)
''')

#Create table Egg_Groups
cursor.execute('''
CREATE TABLE IF NOT EXISTS Egg_Groups(
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

#Create table Pokemon_Egg_Groups
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pokemon_Egg_Groups(
    pokemon_id INTEGER,
    egg_group_id INTEGER,
    FOREIGN KEY(pokemon_id) REFERENCES Pokemons(id),
    FOREIGN KEY(egg_group_id) REFERENCES Egg_Groups(id)
)
''')

#Create table Moves
cursor.execute('''
CREATE TABLE IF NOT EXISTS Moves(
    id INTEGER PRIMARY KEY,
    name TEXT,
    power INTEGER,
    pp INTEGER,
    accuracy INTEGER,
    type_id INTEGER,
    category TEXT,
    ailment TEXT,
    target TEXT,
    effect TEXT
)
''')

#Create table Pokemon_Moves
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pokemon_Moves(
    pokemon_id INTEGER,
    move_id INTEGER,
    learned_how TEXT,
    learned_at_level INTEGER,
    FOREIGN KEY(pokemon_id) REFERENCES Pokemons(id),
    FOREIGN KEY(move_id) REFERENCES Moves(id)
)
''')

#Create table Items
cursor.execute('''
CREATE TABLE IF NOT EXISTS Items(
    id INTEGER PRIMARY KEY,
    name TEXT,
    cost INTEGER,
    category TEXT,
    effect TEXT
)
''')

#Create table Pokemon__held_Items
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pokemon_held_Items(
    pokemon_id INTEGER,
    item_id INTEGER,
    FOREIGN KEY(pokemon_id) REFERENCES Pokemons(id),
    FOREIGN KEY(item_id) REFERENCES Items(id)
)
''')

#Create table Locations
cursor.execute('''
CREATE TABLE IF NOT EXISTS Locations(
    id INTEGER PRIMARY KEY,
    name TEXT,
    region_id INTEGER
)
''')

#Create table Areas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Areas(
    id INTEGER PRIMARY KEY,
    name TEXT,
    location_id INTEGER
)
''')

#Create table Areas_in_Location
cursor.execute('''
CREATE TABLE IF NOT EXISTS Areas_in_Location(
    location_id INTEGER,
    area_id INTEGER,
    FOREIGN KEY(location_id) REFERENCES Locations(id),
    FOREIGN KEY(area_id) REFERENCES Areas(id)
)
''')

#Create table Pokemons_in_areas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pokemons_in_areas(
    pokemon_id INTEGER,
    area_id INTEGER,
    capture_method TEXT,
    capture_rate INTEGER,
    FOREIGN KEY(pokemon_id) REFERENCES Pokemons(id),
    FOREIGN KEY(area_id) REFERENCES Areas(id)
)
''')

# #Create table Regions
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Regions(
#     id INTEGER PRIMARY KEY,
#     name TEXT
# )
# ''')

#Create table Evolution
cursor.execute('''
CREATE TABLE IF NOT EXISTS Evolution(
    id INTEGER PRIMARY KEY,
    pokemon_id INTEGER,
    gender TEXT,
    held_item_id INTEGER,
    item_id INTEGER,
    known_move_id INTEGER,
    known_move_type_id INTEGER,
    location_id INTEGER,
    min_affection INTEGER,
    min_beauty INTEGER,
    min_happiness INTEGER,
    min_level,
    needs_overworld_rain TEXT,
    party_species_id INTEGER,
    party_type_id INTEGER,
    relative_physical_stats INTEGER,
    time_of_day TEXT,
    trade_species_id INTEGER,
    turn_upside_down TEXT,
    trigger TEXT,
    
    FOREIGN KEY(pokemon_id) REFERENCES Pokemons(id),
    FOREIGN KEY(held_item_id) REFERENCES Items(id),
    FOREIGN KEY(item_id) REFERENCES Items(id),
    FOREIGN KEY(known_move_id) REFERENCES Moves(id),
    FOREIGN KEY(known_move_type_id) REFERENCES Types(id),
    FOREIGN KEY(location_id) REFERENCES Locations(id),
    FOREIGN KEY(party_species_id) REFERENCES Pokemons(id),
    FOREIGN KEY(party_type_id) REFERENCES Types(id),
    FOREIGN KEY(trade_species_id) REFERENCES Pokemons(id)
)
''')
       
#Create table Pokemon_Evolution
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pokemon_Evolution(
    pokemon_id INTEGER,
    evolution_id INTEGER,
    FOREIGN KEY(pokemon_id) REFERENCES Pokemons(id),
    FOREIGN KEY(evolution_id) REFERENCES Evolution(id)
)
''') 

conn.close()

