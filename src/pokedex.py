import bd.read_bd as read_bd

class Pokemon():
    def __init__(self, pokemon):
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
        self.habitat = pokemon[19] #NOTE: esto es la id del habitat. Deberia ser el nombre del habitat
        self.evolves_from = None #TODO: implementar
        self.evolves_to = None #TODO: implementar
        self.types = [] #TODO: implementar
        self.moves = None #TODO: implementar

class Move():
    pass

class Item():
    pass

class Pokedex():
    def __init__(self):
        self.pokemones = list[Pokemon]
        self.items = list[Item]
        
    def set_pokemones(self):
        pokemones = read_bd.get_pokemons()
        for pokemon in pokemones:
            self.pokemones.append(Pokemon(pokemon))