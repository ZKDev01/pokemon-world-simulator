import pokebase as pb
import sqlite3
import tqdm
from pokemon import *

REGIONS = [1]
GENERATIONS = [1] 
EXCLUDED_POKES = ['deoxys', 'happiny']

conn = sqlite3.connect('pokedex.db')
cursor = conn.cursor()

# def colect_data():
#     for gen in GENERATIONS:
#         generation = pb.generation(gen)
#         for i in tqdm.tqdm(range(len(generation.pokemon_species))):
#             Pokemon(generation.pokemon_species[i].name)#Con Pokemon tengo Abilities, EggGroups, algunos Moves, algunos Types
#         for i in tqdm.tqdm(range(len(generation.moves))):
#             if generation.moves[i].name in all_moves.get_names():
#                 continue
#             Move(generation.moves[i].name)
#         for i in tqdm.tqdm(range(len(generation.types))):
#             if generation.types[i].name in all_types.get_names():
#                 continue
#             Type(generation.types[i].name)

#region get methods
def get_all_pokemons(total = 1302):
    #Get all pokes that belong to versions firered and leafgreen
    for i in tqdm.tqdm(range(1, total)):#1302
        if all_pokes.get_by_id(i):
            continue
        try:
            poke = pb.pokemon(i)
            if poke.species.name in EXCLUDED_POKES:
                continue
            flavor_text_entries = poke.species.flavor_text_entries
            for i in range(len(flavor_text_entries)):
                if flavor_text_entries[i].version.name == "firered":
                    if poke.name in all_pokes.get_names():
                        continue
                    all_pokes.add_poke(Pokemon(poke.id))
            else:
                continue
        except: continue
        
def get_all_items(total=2180):
    #Get all items in the game firered and leafgreen
    for i in tqdm.tqdm(range(1, total)):#2180
        if all_items.get_by_id(i):
            continue
        try:
            item = pb.item(i)
            for i in range(len(item.flavor_text_entries)):
                if item.flavor_text_entries[i].version_group.name == "firered-leafgreen":
                    if item.name in all_items.get_names():
                        continue
                    Item(item.name)
                    break
        except: continue
        
def get_all_moves():
    #Get all moves in the game firered and leafgreen
    for i in tqdm.tqdm(range(1, 937)):#937
        if all_moves.get_by_id(i):
            continue
        try:
            move = pb.move(i)
            for i in range(len(move.flavor_text_entries)):
                if move.flavor_text_entries[i].version_group.name == "firered-leafgreen":
                    if move.name in all_moves.get_names():
                        continue
                    Move(move.name)
                    break
        except: continue
    
def get_all_abilities():
    #Get all abilities in the game firered and leafgreen
    for i in tqdm.tqdm(range(1, 367)):
        if all_abilities.get_by_id(i):
            continue
        try:
            ability = pb.ability(i)
            for i in range(len(ability.flavor_text_entries)):
                if ability.flavor_text_entries[i].version_group == "firered-leafgreen":
                    if ability.name in all_abilities.get_names():
                        continue
                    all_abilities.add_ability(Ability(ability.name))
                    break
        except: continue
        
def get_all_types():
    #Get all types in the game firered and leafgreen
    for i in tqdm.tqdm(range(1, 20)):
        if all_types.get_by_id(i):
            continue
        type_ = pb.type_(i)
        Type(type_.name)
        
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
        INSERT INTO Pokemons(id, name, height, weight, base_experience, growth_rate, generation, hp, attack, defense, special_attack, special_defense, speed, habitat_id)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (poke.id, poke.name, poke.height, poke.weight, poke.base_exp, poke.growth_rate, poke.generation, poke.stats["hp"], poke.stats["attack"], poke.stats["defense"], poke.stats["special-attack"], poke.stats["special-defense"], poke.stats["speed"], poke.habitat[0]))
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
        INSERT INTO Moves(id, name, power, pp, accuracy, type_id, category, ailment, target, effect_id)
        VALUES(?,?,?,?,?,?,?,?,?,?)
        ''', (move.id, move.name, move.power, move.pp, move.accuracy, pb.type_(move.type).id, move.category, move.ailment, move.target, move.effect_id))
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
                
def fill_effects():
    for effect in all_effects.get_all_effects():
        cursor.execute('''
        INSERT INTO Effects(id, effect)
        VALUES(?,?)
        ''', (effect[0], effect[1]))
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
    saved_pokes = []
    for evol_chain in all_evol.get_all_evolutions():
        for poke in evol_chain.chain.get_pokes():
            
            try:
                if all_pokes.get_by_name(poke).id in saved_pokes:
                    continue
            except: continue
            
            chain = evol_chain.get_by_name(poke)
            details = chain.details
            gender = details['gender']
            
            # if gender == 1: gender = 'female' 
            # if gender == 2: gender = 'male'
            # else: gender = 'genderless'
            
            held_item = details['held_item']
            if held_item == None: held_item = ''
            else: held_item = all_items.get_by_name(held_item.name).name
            
            
            item = details['item']
            if item == None: item = ''
            elif item.name not in all_items.get_names(): item = ''
            else: item = all_items.get_by_name(item.name).name
            
            move = details['known_move']
            if move == None: move = ''
            else: move = all_moves.get_by_name(move.name).name
            
            
            known_move_type = details['known_move_type']
            if known_move_type == None: known_move_type = ''
            else:
                known_move_type = all_types.get_by_name(known_move_type.name).name
            
            location = details['location']
            if location == None: location = ''
            else: location = location.name
            min_affection = details['min_affection']
            if min_affection == None: min_affection = -1
            min_beauty = details['min_beauty']
            if min_beauty == None: min_beauty = -1
            min_happiness = details['min_happiness']
            if min_happiness == None: min_happiness = -1
            min_level = details['min_level']
            if min_level == None: min_level = -1
            needs_overworld_rain = str(details['needs_overworld_rain'])
            if needs_overworld_rain == None: needs_overworld_rain = "False"
            
            party_species = details['party_species']
            if party_species == None: party_species = ''
            else: party_species = all_pokes.get_by_name(party_species.name).name
            
            party_type = details['party_type']
            if party_type == None: party_type = ''
            else: party_type = all_types.get_by_name(party_type.name).name
            
            relative_physical_stats = details['relative_physical_stats']
            if relative_physical_stats == None: relative_physical_stats = -1
            time_of_day = details['time_of_day']
            if time_of_day == None: time_of_day = ''
            
            trade_species = details['trade_species']
            if trade_species == None: trade_species = ''
            else: trade_species = all_pokes.get_by_name(trade_species.name).name
            
            turn_upside_down = str(details['turn_upside_down'])
            if turn_upside_down == None: turn_upside_down = ''
            trigger = details['trigger']
            if trigger == None: trigger = ''
            else: trigger = trigger.name
            
            cursor.execute('''
            INSERT INTO Evolution(id, pokemon_id, gender, held_item, item, known_move, known_move_type, location, min_affection, min_beauty, min_happiness, min_level, needs_overworld_rain, party_species, party_type, relative_physical_stats, time_of_day, trade_species, turn_upside_down, trigger)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (all_pokes.get_by_name(chain.species).id, all_pokes.get_by_name(chain.species).id, gender, held_item, item, move, known_move_type, location, min_affection, min_beauty, min_happiness, min_level, needs_overworld_rain, party_species, party_type, relative_physical_stats, time_of_day, trade_species, turn_upside_down, trigger))
            conn.commit()
            
            saved_pokes.append(all_pokes.get_by_name(chain.species).id)
            
        
def fill_pokemon_evolutions():
    for poke in all_pokes:
        evol_chain = all_evol.get_by_id(poke.evolution_chain_id)
        if evol_chain.chain.get_next_evols(poke.name) == None:
            continue
        for evol in evol_chain.chain.get_next_evols(poke.name):
            if evol == None:
                continue
            else:
                cursor.execute('''
                INSERT INTO Pokemon_Evolution(pokemon_id, evolution_id)
                VALUES(?,?)
                ''', (poke.id, all_pokes.get_by_name(evol.species).id))
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
            INSERT INTO Areas(id, name, location_id)
            VALUES(?,?,?)
            ''', (area.id, area.name, location.id))
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
            for encounter in area.pokemon_encounters:
                pokemon = all_pokes.get_by_name(encounter.pokemon)
                if pokemon == None:
                    all_pokes.add_poke(Pokemon(pb.pokemon(encounter.pokemon).id))
                    pokemon = all_pokes.get_by_name(encounter.pokemon)
                cursor.execute('''
                INSERT INTO Pokemon_Encounter(pokemon_id, area_id, encounter_method_id, min_level, max_level, chance)
                VALUES(?,?,?,?,?,?)
            ''', (pokemon.id, area.id, encounter.encounter_method, encounter.min_level, encounter.max_level, encounter.rate))
            conn.commit()

def fill_area_x_encounter():
    for location in all_locations.get_all_locations():
        for area in location.areas:
            for method in area.encounter_methods.keys():
                encounter = all_enc_methods.get_by_name(method)
                cursor.execute('''
                INSERT INTO AreaXEncounter_Method(area_id, encounter_method_id, rate)
                VALUES(?,?,?)
                ''', (area.id, encounter.id, area.encounter_methods[encounter.name]))#ERROR: 'str' object has no attribute 'name'
                conn.commit()

def fill_habitats():
    for i in range(1,10):
        try:
            habitat = pb.pokemon_habitat(i)
            cursor.execute('''
            INSERT INTO Habitats(id, name)
            VALUES(?,?)
            ''', (habitat.id, habitat.name))
            conn.commit()
        except: continue
        
# def fill_pokemon_habitats():
#     for pokemon in all_pokes:
#         habitat = pokemon.habitat
#         cursor.execute('''
#         INSERT INTO Pokemon_Habitat(pokemon_id, habitat_id)
#         VALUES(?,?)
#         ''', (pokemon.id, habitat[0]))
#         conn.commit()
    
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
    fill_effects()
    fill_habitats()
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
    # fill_pokemon_habitats()