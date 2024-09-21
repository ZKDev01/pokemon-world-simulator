import bd.read_bd as read_bd

class Pokemon():
    def __init__(self, pokemon, habitats, evolutions, poke_evolutions, pokemones, poke_types, types, poke_moves, moves):
        self.id = pokemon[0]
        self.name = pokemon[1]
        self.height = pokemon[2]
        self.weight = pokemon[3]
        self.base_experience = pokemon[4]
        self.growth_rate = pokemon[5]
        self.generation = pokemon[6]
        self.stats = {}
        self.stats['hp'] = pokemon[7]
        self.stats['attack'] = pokemon[8]
        self.stats['defense'] = pokemon[9]
        self.stats['special_attack'] = pokemon[10]
        self.stats['special_defense'] = pokemon[11]
        self.stats['speed'] = pokemon[12]
        self.ev = {}
        self.ev['hp'] = pokemon[13]
        self.ev['attack'] = pokemon[14]
        self.ev['defense'] = pokemon[15]
        self.ev['special_attack'] = pokemon[16]
        self.ev['special_defense'] = pokemon[17]
        self.ev['speed'] = pokemon[18]
        self.habitat = self.set_habitat(habitats, pokemon[19])
        self.evolves_to = []
        self.evolves_from = None
        self.set_evolution(evolutions, poke_evolutions, pokemones)
        self.types = self.set_types(poke_types, types)
        self.moves = self.set_moves(poke_moves, moves)
        
    def set_moves(self, poke_moves, moves):
        selected_moves = {}
        for poke_move in poke_moves:
            if poke_move[0] == self.id:
                for move in moves:
                    if move[0] == poke_move[1]:
                        if poke_move[2] not in selected_moves:
                            selected_moves[poke_move[2]] = []
                        selected_moves[poke_move[2]].append((move[1], poke_move[3]))
                        break
        return selected_moves
        
    
    def set_types(self, poke_types, types):
        selected_types = []
        for poke_type in poke_types:
            if poke_type[0] == self.id:
                for type in types:
                    if type[0] == poke_type[1]:
                        selected_types.append(type[1])
                        break
        return selected_types

    def set_habitat(self, habitats, habitat_id):
        for habitat in habitats:
            if habitat[0] == habitat_id:
                return habitat[1]
        return None
    
    def set_evolution(self, evolutions, poke_evolutions, pokemones):
        evolves_to = []
        for poke_evol in poke_evolutions:
            if poke_evol[0] == self.id:
                for evolution in evolutions:
                    if evolution[0] == poke_evol[1]:
                        for pokemon in pokemones:
                            if pokemon[0] == evolution[1]:
                                evolves_to.append(pokemon[1])
                                break
                        break
        evolves_from = None
        for evol in evolutions:
            if evol[1] == self.id:
                for poke_evol in poke_evolutions:
                    if poke_evol[1] == evol[0]:
                        for pokemon in pokemones:
                            if pokemon[0] == poke_evol[0]:
                                evolves_from = pokemon[1]
                                break
                        break
                break
        self.evolves_to = evolves_to
        self.evolves_from = evolves_from
        
                         
            
        
class Move():
    pass

class Item():
    pass

class Pokedex():
    def __init__(self):
        self.pokemones : list[Pokemon] = []
        # self.items : list[Item] = []
        self.set_pokemones()
        
    def set_pokemones(self):
        pokemones = read_bd.get_pokemons()
        habitats = read_bd.get_habitats()
        evolutions = read_bd.get_evolutions()
        poke_evolutions = read_bd.get_pokemon_evolutions()
        poke_types = read_bd.get_pokemon_types()
        types = read_bd.get_types()
        poke_moves = read_bd.get_pokemon_moves()
        moves = read_bd.get_moves()
        for pokemon in pokemones:
            self.pokemones.append(Pokemon(pokemon, habitats, evolutions, poke_evolutions, pokemones, poke_types, types, poke_moves, moves))
            
    def get_pokemon(self, name):
        for pokemon in self.pokemones:
            if pokemon.name == name:
                return pokemon
        return None