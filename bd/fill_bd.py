import pokebase as pb
import sqlite3
import tqdm
from pokemon import *

REGIONS = [1] 

conn = sqlite3.connect('pokedex.db')
cursor = conn.cursor()

#region get methods
def get_all_pokemons():
    #Get all pokes that belong to versions firered and leafgreen
    for i in tqdm.tqdm(range(1, 152)):
        if all_pokes.get_by_id(i):
            continue
        Pokemon(i)
        
def get_all_items():
    #Get all items in the game firered and leafgreen
    for i in tqdm.tqdm(range(1, 375)):
        if all_items.get_by_id(i):
            continue
        item = pb.item(i)
        all_items.add_item(Item(item.name))
        
def get_all_moves():
    #Get all moves in the game firered and leafgreen
    for i in tqdm.tqdm(range(1, 355)):
        if all_moves.get_by_id(i):
            continue
        move = pb.move(i)
        all_moves.add_move(Move(move.name))
    
def get_all_abilities():
    #Get all abilities in the game firered and leafgreen
    for i in tqdm.tqdm(range(1, 267)):
        if all_abilities.get_by_id(i):
            continue
        ability = pb.ability(i)
        for i in range(len(ability.flavor_text_entries)):
            if ability.flavor_text_entries[i].version_group == "firered-leafgreen":
                if ability.name in all_abilities.get_names():
                    continue
                all_abilities.add_ability(Ability(ability.name))
                break
        
def get_all_types():
    #Get all types in the game firered and leafgreen
    for i in tqdm.tqdm(range(1, 19)):
        if all_types.get_by_id(i):
            continue
        type_ = pb.type_(i)
        all_types.add_type(Type(type_.name))
        
def get_all_egg_groups():
    #Get all egg groups in the game firered and leafgreen
    for i in tqdm.tqdm(range(1, 16)):
        if all_egg_groups.get_by_id(i):
            continue
        egg_group = pb.egg_group(i)
        all_egg_groups.add_egg_group(Egg_group(egg_group.name))

def get_evolutions():
    for pokemon in all_pokes:
        if all_evol.get_by_id(pokemon.evolution_chain_id):
            continue
        Evolution_chain(pokemon.evolution_chain_id)

def get_locations():
    for region in REGIONS:
        for location in pb.region(region).locations:
            if all_locations.get_by_id(location.id):
                continue
            Location(location.id)
#endregion

#region fill methods
def fill_pokemons():
    for poke in all_pokes.get_all_pokes():
        cursor.execute('''
        INSERT INTO Pokemons(id, name, height, weight, base_experience, growth_rate, generation, hp, attack, defense, special_attack, special_defense, speed)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (poke.id, poke.name, poke.height, poke.weight, poke.base_exp, poke.growth_rate, poke.generation, poke.stats["hp"], poke.stats["attack"], poke.stats["defense"], poke.stats["special-attack"], poke.stats["special-defense"], poke.stats["speed"]))
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
            if type_:
                type_ = all_types.get_by_name(type_.name)
                cursor.execute('''
                INSERT INTO Pokemon_Types(pokemon_id, type_id)
                VALUES(?,?)
                ''', (pokemon.id, type_.id))
                conn.commit()
            
def fill_abilities():
    for ability in all_abilities.get_all_abilities():
        cursor.execute('''
        INSERT INTO Abilities(id, name, effect)
        VALUES(?,?,?)
        ''', (ability.id, ability.name, ability.effect))
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
        INSERT INTO Moves(id, name, power, pp, accuracy, type_id, category, ailment, target, effect)
        VALUES(?,?,?,?,?,?,?,?,?,?)
        ''', (move.id, move.name, move.power, move.pp, move.accuracy, pb.type_(move.type).id, move.category, move.ailment, move.target, move.effects))
        conn.commit()
        
def fill_pokemon_moves():
    for pokemon in all_pokes:
        for type in pokemon.moves.keys():
            for move, level in pokemon.moves[type]:
                move = all_moves.get_by_name(move)
                cursor.execute('''
                INSERT INTO Pokemon_Moves(pokemon_id, move_id, learned_how, learned_at_level)
                VALUES(?,?,?,?)
                ''', (pokemon.id, move.id, type, level))
                conn.commit()
            
def fill_items():
    for item in all_items.get_all_items():
        cursor.execute('''
        INSERT INTO Items(id, name, cost, category, effect)
        VALUES(?,?,?,?,?)
        ''', (item.id, item.name, item.cost, item.category, item.effects))
        conn.commit()
        
def fill_pokemon_held_items():
    for pokemon in all_pokes:
        for item in pokemon.held_items:
            item = all_items.get_by_name(item)
            cursor.execute('''
            INSERT INTO Pokemon_Held_Items(pokemon_id, item_id)
            VALUES(?,?)
            ''', (pokemon.id, item.id))
            conn.commit()           

def fill_evolutions():
    for evol_chain in all_evol.get_all_evolutions():
        for poke in evol_chain.chain.get_pokes():
            
            chain = evol_chain.get_chain()
            details = evol_chain.chain.get_evol_details(poke)
            gender = details['gender']
            if gender == 1: gender = 'female' 
            if gender == 2: gender = 'male'
            else: gender = 'genderless'
            
            held_item = details['held_item']
            held_item = all_items.get_by_name(held_item)
            
            item = details['item']
            item = all_items.get_by_name(item)
            
            known_move = details['known_move']
            move = all_moves.get_by_name(known_move)
            
            known_move_type = details['known_move_type']
            known_move_type = all_types.get_by_name(known_move_type)
            
            location = details['location']
            min_affection = details['min_affection']
            min_beauty = details['min_beauty']
            min_happiness = details['min_happiness']
            min_level = details['min_level']
            needs_overworld_rain = details['needs_overworld_rain']
            
            party_species = details['party_species']
            party_species = all_pokes.get_by_name(party_species)
            
            party_type = details['party_type']
            party_type = all_types.get_by_name(party_type)
            
            relative_physical_stats = details['relative_physical_stats']
            time_of_day = details['time_of_day']
            
            trade_species = details['trade_species']
            trade_species = all_pokes.get_by_name(trade_species)
            
            turn_upside_down = details['turn_upside_down']
            trigger = details['trigger']
            
            cursor.execute('''
            INSERT INTO Evolutions(id, pokemon_id, gender, held_item_id, known_move_id, known_move_type_id, location_id, min_affection, min_beauty, min_happiness, min_level, needs_overworld_rain, party_species_id, party_type_id, relative_physical_stats, time_of_day, trade_species_id, turn_upside_down, trigger)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (chain.species.id, chain.species.id, gender, held_item.id, item.id, move.id, known_move_type.id, location, min_affection, min_beauty, min_happiness, min_level, needs_overworld_rain, party_species.id, party_type.id, relative_physical_stats, time_of_day, trade_species.id, turn_upside_down, trigger))
            conn.commit()
        
def fill_pokemon_evolutions():
    for poke in all_pokes:
        evol_chain = all_evol.get_by_id(poke.evolution_chain_id)
        for evol in evol_chain.chain.get_next_evols(poke):
            if evol == None:
                continue
            else:
                cursor.execute('''
                INSERT INTO Pokemon_Evolutions(pokemon_id, evolution_id)
                VALUES(?,?)
                ''', (poke.id, evol.species.id))
                conn.commit()  

def fill_locations():
    for location in all_locations.get_all_locations():
        cursor.execute('''
        INSERT INTO Locations(id, name, region_id)
        VALUES(?,?,?)
        ''', (location.id, location.name, location.region))
        conn.commit()
        
def fill_areas():
    for location in all_locations.get_all_locations():
        for area in location.areas:
            cursor.execute('''
            INSERT INTO Areas(location_id, area_id)
            VALUES(?,?)
            ''', (location.id, area.id))
            conn.commit()

def fill_encounter_methods():
    for method in all_enc_methods.get_all_encounter_methods():
        cursor.execute('''
        INSERT INTO Encounter_Methods(id, name)
        VALUES(?,?)
        ''', (method.id, method.name))
        conn.commit()
        
def fill_pokemon_encounters():
    for location in all_locations.get_all_locations():
        for area in location.areas:
            for encounter in area.encounters:
                cursor.execute('''
                INSERT INTO Pokemon_Encounters(pokemon_id, area_id, encounter_method_id, min_level, max_level, chance)
                VALUES(?,?,?,?,?,?)
            ''', (encounter.pokemon.id, area.id, encounter.method.id, encounter.min_level, encounter.max_level, encounter.chance))
            conn.commit()

def fill_area_x_encounter():
    for location in all_locations.get_all_locations():
        for area in location.areas:
            for method in area.encounter_methods.keys():
                encounter = all_enc_methods.get_by_name(method)
                cursor.execute('''
                INSERT INTO AreaXEncounter_Method(area_id, encounter_method_id, rate)
                VALUES(?,?,?)
                ''', (area.id, encounter.id, area.encounter_methods[method.name]))#ERROR: 'str' object has no attribute 'name'
                conn.commit()
#endregion

def get_all():
    get_all_pokemons()
    get_all_types()
    get_all_abilities()
    get_all_egg_groups()
    get_all_moves()
    get_all_items()
    get_evolutions()
    get_locations()
          
def fill_all():
    fill_pokemons()
    fill_types()
    fill_pokemon_types()
    fill_abilities()
    fill_pokemon_abilities()
    fill_egg_groups()
    fill_pokemon_egg_groups()
    fill_moves()
    fill_pokemon_moves()
    fill_items()
    fill_pokemon_held_items()
    fill_evolutions()
    fill_pokemon_evolutions()
    fill_locations()
    fill_areas()
    fill_encounter_methods()
    fill_pokemon_encounters()
    fill_area_x_encounter()