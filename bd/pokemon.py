import pokebase as pb

class Type:
    def __init__(self, name):
        type_ = pb.type_(name)
        self.id = type_.id
        self.name = type_.name
        all_types.add_type(self)
    
    def __str__(self):
        return self.name + " type"
    
class Ability:
    def __init__(self, name):
        ability = pb.ability(name)
        self.id = ability.id
        self.name = ability.name
        self.effect = self.get_description(ability)
        all_abilities.add_ability(self)
        
    def get_description(self, ability):
        for i in range(len(ability.flavor_text_entries)):
            if ability.flavor_text_entries[i].language.name == "en":
                return ability.flavor_text_entries[i].flavor_text
    
    def __str__(self):
        return self.name + " is an ability that " + self.effect

class Egg_group:
    def __init__(self, name):
        egg_group = pb.egg_group(name)
        self.id = egg_group.id
        self.name = egg_group.name
        all_egg_groups.add_egg_group(self)
    
    def __str__(self):
        return self.name + " egg group"

class Pokemon:
    def __init__(self, id):
        pokemon = pb.pokemon(id)
        self.id = pokemon.id
        self.name = pokemon.name
        self.types = (Type(pokemon.types[0].type.name), Type(pokemon.types[1].type.name)) if len(pokemon.types) == 2 else (Type(pokemon.types[0].type.name), None)
        self.height = pokemon.height
        self.weight = pokemon.weight
        self.base_exp = pokemon.base_experience
        self.generation = pokemon.species.generation.name.split("-")[1]
        self.growth_rate = pokemon.species.growth_rate.name
        self.stats = self.get_poke_stats(pokemon)
        self.held_items = self.get_poke_items(pokemon)
        self.abilities = self.get_poke_abilities(pokemon)
        self.moves = self.get_poke_moves(pokemon)
        self.egg_groups = []
        for i in range(len(pokemon.species.egg_groups)):
            self.egg_groups.append(Egg_group(pokemon.species.egg_groups[i].name))
        # self.evolution_chain = Evolution_chain(pokemon.species.evolution_chain.id)
        self.evolution_chain_id = pokemon.species.evolution_chain.id
        all_pokes.add_poke(self)
        
    
    def __str__(self):
        return self.name + " is a " + self.types[0] + " type Pokemon."

    def get_poke_stats(self, pokemon):
        poke_stats = {}
        for i in range(len(pokemon.stats)):
            poke_stats[pokemon.stats[i].stat.name] = pokemon.stats[i].base_stat
        return poke_stats

    def get_poke_abilities(self, pokemon):
        poke_abilities = []
        for i in range(len(pokemon.abilities)):
            poke_abilities.append(Ability(pokemon.abilities[i].ability.name))
        return poke_abilities
    
    def get_poke_items(self, pokemon):
        items = []
        if pokemon.held_items:
            for i in range(len(pokemon.held_items)):
                if pokemon.held_items[i].item.name in all_items.get_names():
                    items.append(all_items.get_by_name(pokemon.held_items[i].item.name).name)
                else:
                    items.append(Item(pokemon.held_items[i].item.name).name)
        return items
    
    def get_poke_moves(self, pokemon):
        moves = {} # method : (move, level)
        for i in range(len(pokemon.moves)):
            for j in range(len(pokemon.moves[i].version_group_details)):
                if pokemon.moves[i].version_group_details[j].version_group.name == "firered-leafgreen":
                    if pokemon.moves[i].move.name in all_moves.get_names():
                        move = all_moves.get_by_name(pokemon.moves[i].move.name)
                    else:
                        move = Move(pokemon.moves[i].move.name)
                    if pokemon.moves[i].version_group_details[j].move_learn_method.name in moves:
                        moves[pokemon.moves[i].version_group_details[j].move_learn_method.name].append((move.name, pokemon.moves[i].version_group_details[j].level_learned_at))
                    else:
                        moves[pokemon.moves[i].version_group_details[j].move_learn_method.name] = [(move.name, pokemon.moves[i].version_group_details[j].level_learned_at)]
        return moves
    

class Item:
    def __init__(self, name):
        item = pb.item(name)
        self.id = item.id
        self.name = item.name
        self.cost = item.cost
        self.category = item.category.name
        self.effects = [effect.short_effect for effect in item.effect_entries][0]
        # self.held_by = self.get_held_by(item)
        all_items.add_item(self)
    
    def __str__(self):
        return self.name + " is a " + self.category + " item that costs " + str(self.cost) + " and " + self.effect
        
    # def get_held_by(self, item):
    #     held_by = []
    #     for i in range(len(item.held_by_pokemon)):
    #         held_by.append(item.held_by_pokemon[i].pokemon.name)
    #     return held_by
    
class Move:
    def __init__(self, name):
        move = pb.move(name)
        self.id = move.id
        self.name = move.name
        self.type = move.type.name
        self.category = move.damage_class.name
        self.power = move.power if move.power else 0
        self.accuracy = move.accuracy if move.accuracy else 0
        self.pp = move.pp
        self.target = move.target.name
        self.effects = [effect.short_effect for effect in move.effect_entries][0]
        # self.learned_by = self.get_learned_by(move)
        self.ailment = move.meta.ailment.name
        #How this move is learned by a pokemon
        # self.learn_method =
        all_moves.add_move(self)
    
    def __str__(self):
        return self.name + " is a " + self.category + " move with " + str(self.power) + " power and " + str(self.accuracy) + " accuracy."
    
    # def get_learned_by(self, move):
    #     learned_by = []
    #     for i in range(len(move.learned_by_pokemon)):
    #         learned_by.append(move.learned_by_pokemon[i].pokemon.name)
    #     return learned_by
    
class Evolution_chain:
    def __init__(self, id):
        self.id = id
        chain = pb.evolution_chain(id)
        self.chain = Chain(chain.chain)
        all_evol.add_evolution(self)
        
    def __str__(self):
        return str(self.chain)
    
    def get_pokes(self):
        return self.chain.get_pokes()
    
    def get_evol_details(self, poke):
        return self.chain.get_evol_details(poke)

class Chain:
    def __init__(self, chain):
        self.species = chain.species.name
        self.details = self.set_details(chain)
        self.evolves_to = []
        for i in range(len(chain.evolves_to)):
            self.evolves_to.append(Chain(chain.evolves_to[i]))
        
        
    def set_details(self, chain):
        details = {}
        names = ["gender", "held_item", "item", "known_move", "known_move_type", "location", "min_affection", "min_beauty", "min_happiness", "min_level", "needs_overworld_rain", "party_species", "party_type", "relative_physical_stats", "time_of_day", "trade_species", "turn_upside_down", "trigger"]
        if chain.evolution_details:
            evol_details = chain.evolution_details[0]
            for element in names:
                if element in evol_details.__dict__:
                    details[element] = evol_details.__dict__[element]
        return details
        
    def get_pokes(self):
        pokes = [self.species]
        for i in range(len(self.evolves_to)):
            pokes += self.evolves_to[i].get_pokes()
        return pokes
    
    def get_chain_details(self):
        return self.details
            
    def get_evol_details(self, poke_name : str):
        if self.species == poke_name:
            return self.details
        for i in range(len(self.evolves_to)):
            if poke_name in self.evolves_to[i].get_pokes():
                return self.evolves_to[i].get_evol_details(poke_name)
        return None
    
class Location:
    def __init__(self, id):
        location = pb.location(id)
        self.id = location.id
        self.name = location.name
        self.areas = self.get_areas(location)
        all_locations.add_location(self)
    
    def get_areas(self, location):
        areas = []
        for i in range(len(location.areas)):
            areas.append(Area(location.areas[i].name))
        return areas

class Area:
    def __init__(self, name):
        area = pb.location_area(name)
        self.id = area.id
        self.name = area.name
        self.pokemons = self.get_pokes(area)
    
    def get_pokes(self, area):
        pokes = []
        for i in range(len(area.pokemon_encounters)):
            pokes.append(Pokemon(area.pokemon_encounters[i].pokemon.name))
        return pokes
    
class All_locations:
    def __init__(self):
        self.all_locations = []
    
    def add_location(self, location : Location):
        if location not in self.all_locations:
            self.all_locations.append(location)
        
    def get_names(self):
        names = []
        for i in range(len(self.all_locations)):
            names.append(self.all_locations[i].name)
        return names
    
    def get_by_name(self, name):
        for i in range(len(self.all_locations)):
            if self.all_locations[i].name == name:
                return self.all_locations[i]
        return None
    
    def get_by_id(self, id):
        for i in range(len(self.all_locations)):
            if self.all_locations[i].id == id:
                return self.all_locations[i]
        return None
    
    def get_all_locations(self):
        return self.all_locations
    
    def __len__(self):
        return len(self.all_locations)
    
    def __getitem__(self, key):
        return self.all_locations[key]
    
    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current < len(self.all_locations):
            self.current += 1
            return self.all_locations[self.current - 1]
        else:
            raise StopIteration
    
class All_moves:
    def __init__(self):
        self.all_moves = []
    
    def add_move(self, move : Move):
        if move not in self.all_moves:
            self.all_moves.append(move)
        
    def get_names(self):
        names = []
        for i in range(len(self.all_moves)):
            names.append(self.all_moves[i].name)
        return names
    
    def get_by_name(self, name):
        for i in range(len(self.all_moves)):
            if self.all_moves[i].name == name:
                return self.all_moves[i]
        return None
    
    def get_by_id(self, id):
        for i in range(len(self.all_moves)):
            if self.all_moves[i].id == id:
                return self.all_moves[i]
        return None
    
    def get_all_moves(self):
        return self.all_moves
    
    def __len__(self):
        return len(self.all_moves)
    
    def __getitem__(self, key):
        return self.all_moves[key]
    
    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current < len(self.all_moves):
            self.current += 1
            return self.all_moves[self.current - 1]
        else:
            raise StopIteration
        
    
class All_items:
    def __init__(self):
        self.all_items = []
    
    def add_item(self, item : Item):
        if item not in self.all_items:
            self.all_items.append(item)
        
    def get_names(self):
        names = []
        for i in range(len(self.all_items)):
            names.append(self.all_items[i].name)
        return names
    
    def get_by_name(self, name):
        for i in range(len(self.all_items)):
            if self.all_items[i].name == name:
                return self.all_items[i]
        return None
    
    def get_by_id(self, id):
        for i in range(len(self.all_items)):
            if self.all_items[i].id == id:
                return self.all_items[i]
        return None
    
    def get_all_items(self):
        return self.all_items
    
    def __len__(self):
        return len(self.all_items)
    
    def __getitem__(self, key):
        return self.all_items[key]
    
    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current < len(self.all_items):
            self.current += 1
            return self.all_items[self.current - 1]
        else:
            raise StopIteration

class All_pokes:
    def __init__(self):
        self.all_pokes = []
    
    def add_poke(self, poke : Pokemon):
        if poke.name not in self.get_names():
            self.all_pokes.append(poke)
        
    def get_names(self):
        names = []
        for i in range(len(self.all_pokes)):
            names.append(self.all_pokes[i].name)
        return names
    
    def get_by_name(self, name):
        for i in range(len(self.all_pokes)):
            if self.all_pokes[i].name == name:
                return self.all_pokes[i]
        return None
    
    def get_by_id(self, id):
        for i in range(len(self.all_pokes)):
            if self.all_pokes[i].id == id:
                return self.all_pokes[i]
        return None
    
    def get_all_pokes(self):
        return self.all_pokes
    
    def __len__(self):
        return len(self.all_pokes)
    
    def __getitem__(self, key):
        return self.all_pokes[key]
    
    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current < len(self.all_pokes):
            self.current += 1
            return self.all_pokes[self.current - 1]
        else:
            raise StopIteration
        
class All_evolutions:
    def __init__(self):
        self.all_evolutions = []
    
    def add_evolution(self, evolution : Evolution_chain):
        if evolution not in self.all_evolutions:
            self.all_evolutions.append(evolution)
        
    def get_all_evolutions(self):
        return self.all_evolutions
    
    def get_by_id(self, id):
        for i in range(len(self.all_evolutions)):
            if self.all_evolutions[i].id == id:
                return self.all_evolutions[i]
        return None
    
    def __len__(self):
        return len(self.all_evolutions)
    
    def __getitem__(self, key):
        return self.all_evolutions[key]
    
    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current < len(self.all_evolutions):
            self.current += 1
            return self.all_evolutions[self.current - 1]
        else:
            raise StopIteration

class All_types:
    def __init__(self):
        self.all_types = []
    
    def add_type(self, type_ : Type):
        if type_.name not in self.get_names():
            self.all_types.append(type_)
        
    def get_names(self):
        names = []
        for i in range(len(self.all_types)):
            names.append(self.all_types[i].name)
        return names
    
    def get_by_name(self, name):
        for i in range(len(self.all_types)):
            if self.all_types[i].name == name:
                return self.all_types[i]
        return None
    
    def get_by_id(self, id):
        for i in range(len(self.all_types)):
            if self.all_types[i].id == id:
                return self.all_types[i]
        return None
    
    def get_all_types(self):
        return self.all_types
    
    def __len__(self):
        return len(self.all_types)
    
    def __getitem__(self, key):
        return self.all_types[key]
    
    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current < len(self.all_types):
            self.current += 1
            return self.all_types[self.current - 1]
        else:
            raise StopIteration

class All_abilities:
    def __init__(self):
        self.all_abilities = []
    
    def add_ability(self, ability : Ability):
        if ability.name not in self.get_names():
            self.all_abilities.append(ability)
        
    def get_names(self):
        names = []
        for i in range(len(self.all_abilities)):
            names.append(self.all_abilities[i].name)
        return names
    
    def get_by_name(self, name):
        for i in range(len(self.all_abilities)):
            if self.all_abilities[i].name == name:
                return self.all_abilities[i]
        return None
    
    def get_by_id(self, id):
        for i in range(len(self.all_abilities)):
            if self.all_abilities[i].id == id:
                return self.all_abilities[i]
        return None
    
    def get_all_abilities(self):
        return self.all_abilities
    
    def __len__(self):
        return len(self.all_abilities)
    
    def __getitem__(self, key):
        return self.all_abilities[key]
    
    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current < len(self.all_abilities):
            self.current += 1
            return self.all_abilities[self.current - 1]
        else:
            raise StopIteration

class All_egg_groups:
    def __init__(self):
        self.all_egg_groups = []
    
    def add_egg_group(self, egg_group : Egg_group):
        if egg_group.name not in self.get_names():
            self.all_egg_groups.append(egg_group)
        
    def get_names(self):
        names = []
        for i in range(len(self.all_egg_groups)):
            names.append(self.all_egg_groups[i].name)
        return names
    
    def get_by_name(self, name):
        for i in range(len(self.all_egg_groups)):
            if self.all_egg_groups[i].name == name:
                return self.all_egg_groups[i]
        return None
    
    def get_by_id(self, id):
        for i in range(len(self.all_egg_groups)):
            if self.all_egg_groups[i].id == id:
                return self.all_egg_groups[i]
        return None
    
    def get_all_egg_groups(self):
        return self.all_egg_groups
    
    def __len__(self):
        return len(self.all_egg_groups)
    
    def __getitem__(self, key):
        return self.all_egg_groups[key]
    
    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current < len(self.all_egg_groups):
            self.current += 1
            return self.all_egg_groups[self.current - 1]
        else:
            raise StopIteration

all_moves = All_moves()
all_items = All_items()
all_pokes = All_pokes()
all_types = All_types()
all_abilities = All_abilities()
all_egg_groups = All_egg_groups()
all_evol = All_evolutions()