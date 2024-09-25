from mapa.create_map import Map, Location
from pokedex import Pokedex, Pokemon
import random

class Heuristic:
    '''
    Clase que encapsula la estrategia que seguira un entrenador para tomar decisiones.
    '''
    
class map_orientation(Heuristic):
    '''
    Estrategia que sigue un entrenador para moverse por el mapa.
    '''
    def __init__(self, map:Map, pokemon_list:list):
        self.map = map
        self.pokemon_list = pokemon_list
        self.current_location = None
    
    def next_location(self):
        pass
    
    def route(self):
        pass
    
    def find_pokemon(self):
        pass
    
    def find_pokemon_locations(self):
        pass
    
class random_orientation(map_orientation):
    
    def next_location(self):
        locations = self.map.get_all_locations()
        next_location = random.choice(locations)
        return next_location
    
    def route(self, start:str, end:str):
        return self.map.get_shortest_path(start, end)
    
    def find_pokemon(self):
        habitats = []
        locations = self.map.get_all_locations()
        for location in locations:
            ecosystems = location.get_ecosystems()
            for pokemon in ecosystems.values():
                if pokemon in self.pokemon_list:
                    habitats.append(location)
        return habitats
    
    def find_pokemon_locations(self):
        habitats = self.find_pokemon()
        locations = []
        for habitat in habitats:
            locations.append(habitat.name())
        return locations
    
    
    
# class battle_strategy(Heuristic):

def find_habitat(map:Map, pokemones:list):
    '''
    Encuentra todos los lugares del mapa donde se puede encontrar un pokemon de la lista de pokemones.
    
    Args:
    map (Map): Mapa donde se va a buscar el habitat. Debe ser una instancia de la clase Map.
    '''
    habitats = []
    locations = map.get_all_locations()
    for location in locations:
        ecosystems = location.get_ecosystems()
        for pokemon in ecosystems.values():
            if pokemon in pokemones:
                habitats.append(location)
                
def route(map:Map, start:str, end:str):
    '''
    Encuentra la ruta más corta entre dos lugares en el mapa.
    
    Args:
    map (Map): Mapa donde se va a buscar la ruta. Debe ser una instancia de la clase Map.
    start (str): Lugar de inicio.
    end (str): Lugar de fin.
    
    Returns:
    list: Lista con los lugares que forman la ruta más corta.
    '''
    return map.get_shortest_path(start, end)

def next_location(map:Map, current_place:str, pokemon_list:list):
    '''
    Encuentra la siguiente localización a la que se va a mover el entrenador.
    
    Args:
    map (Map): Mapa donde se va a buscar la siguiente localización. Debe ser una instancia de la clase Map.
    '''
    next_locations = map.get_next_locations(current_place)
    for location in next_locations:
        ecosystems = location.get_ecosystems()
        for pokemon in ecosystems.values():
            if pokemon in pokemon_list:
                return location
    return None
    
        
    
    