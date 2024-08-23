import pokebase as pb
import sqlite3
from pokemon_ import *

conn = sqlite3.connect('pokedex.db')
cursor = conn.cursor()

def get_all_pokemons():
    #Get all pokes that belong to versions firered and leafgreen
    for i in range(1, 152):
        #SI el pokemon ya esta en all_pokes, no lo vuelvas a agregar
        if pb.pokemon(i).name in all_pokes.get_names():
            continue
        Pokemon(i)
        
def get_all_items():
    #Get all items in the game firered and leafgreen
    for i in range(1, 375):
        item = pb.item(i)
        if item.name in all_items.get_names():
            continue
        all_items.add_item(Item(item.name))
        
def get_all_moves():
    #Get all moves in the game firered and leafgreen
    for i in range(1, 355):
        move = pb.move(i)
        if move.name in all_moves.get_names():
            continue
        all_moves.add_move(Move(move.name))
    
def get_all_abilities():
    #Get all abilities in the game firered and leafgreen
    for i in range(1, 267):
        ability = pb.ability(i)
        if ability.name in all_abilities.get_names():
            continue
        all_abilities.add_ability(Ability(ability.name))
        
def get_all_types():
    #Get all types in the game firered and leafgreen
    for i in range(1, 19):
        type_ = pb.type_(i)
        if type_.name in all_types.get_names():
            continue
        all_types.add_type(Type(type_.name))
        
def get_all_egg_groups():
    #Get all egg groups in the game firered and leafgreen
    for i in range(1, 16):
        egg_group = pb.egg_group(i)
        if egg_group.name in all_egg_groups.get_names():
            continue
        all_egg_groups.add_egg_group(Egg_group(egg_group.name))

def fill_pokemons():
    for poke in all_pokes.get_all_pokes():
        cursor.execute('''
        INSERT INTO Pokemons(id, name, height, weight, base_experience, growth_rate, generation, hp, attack, defense, special_attack, special_defense, speed)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (poke.id, poke.name, poke.height, poke.weight, poke.base_experience, poke.growth_rate, poke.generation, poke.hp, poke.attack, poke.defense, poke.special_attack, poke.special_defense, poke.speed))
        conn.commit()

def fill_types():
    for type_ in all_types.get_all_types():
        cursor.execute('''
        INSERT INTO Types(id, name)
        VALUES(?,?)
        ''', (type_.id, type_.name))
        conn.commit()
        
def fill_pokemon_types():
    for pokemon in all_pokes:
        for type_ in pokemon.types:
            type_ = all_types.get_by_name(type_.name)
            cursor.execute('''
            INSERT INTO Pokemon_Types(pokemon_id, type_id)
            VALUES(?,?)
            ''', (pokemon.id, type_.id))
            conn.commit()
            
def fill_abilities():
    for ability in all_abilities.get_all_abilities():
        cursor.execute('''
        INSERT INTO Abilities(id, name)
        VALUES(?,?)
        ''', (ability.id, ability.name))
        conn.commit()
        
def fill_pokemon_abilities():
    for pokemon in all_pokes:
        for ability in pokemon.abilities:
            ability = all_abilities.get_by_name(ability.name)
            cursor.execute('''
            INSERT INTO Pokemon_Abilities(pokemon_id, ability_id)
            VALUES(?,?)
            ''', (pokemon.id, ability.id))
            conn.commit()
            
def fill_egg_groups():
    for egg_group in all_egg_groups.get_all_egg_groups():
        cursor.execute('''
        INSERT INTO Egg_Groups(id, name)
        VALUES(?,?)
        ''', (egg_group.id, egg_group.name))
        conn.commit()
        
def fill_pokemon_egg_groups():
    for pokemon in all_pokes:
        for egg_group in pokemon.egg_groups:
            egg_group = all_egg_groups.get_by_name(egg_group.name)
            cursor.execute('''
            INSERT INTO Pokemon_Egg_Groups(pokemon_id, egg_group_id)
            VALUES(?,?)
            ''', (pokemon.id, egg_group.id))
            conn.commit()
            
def fill_moves():
    for move in all_moves.get_all_moves():
        cursor.execute('''
        INSERT INTO Moves(id, name, type, power, accuracy, pp, description)
        VALUES(?,?,?,?,?,?,?)
        ''', (move.id, move.name, move.type, move.power, move.accuracy, move.pp, move.description))
        conn.commit()
        
def fill_pokemon_moves():
    for pokemon in all_pokes:
        for move in pokemon.moves:
            move = all_moves.get_by_name(move.name)
            cursor.execute('''
            INSERT INTO Pokemon_Moves(pokemon_id, move_id)
            VALUES(?,?)
            ''', (pokemon.id, move.id))
            conn.commit()
            
def fill_items():
    for item in all_items.get_all_items():
        cursor.execute('''
        INSERT INTO Items(id, name, cost, description)
        VALUES(?,?,?,?)
        ''', (item.id, item.name, item.cost, item.description))
        conn.commit()
        
def fill_pokemon_held_items():
    for pokemon in all_pokes:
        for item in pokemon.held_items:
            item = all_items.get_by_name(item.name)
            cursor.execute('''
            INSERT INTO Pokemon_Held_Items(pokemon_id, item_id)
            VALUES(?,?)
            ''', (pokemon.id, item.id))
            conn.commit()
 #TODO: Fill locations and areas tables and evolution tables.
        
        
