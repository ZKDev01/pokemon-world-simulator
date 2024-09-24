import bd.read_bd as read_bd
import random
from collections import deque
import random

LOCATIONS = read_bd.get_locations()
AREAS = read_bd.get_areas()  
POKEMON_ENCOUNTERS = read_bd.get_pokemon_encounters()
ENCOUNTER_METHODS = read_bd.get_encounter_methods()
AREA_ENCOUNTER_METHODS = read_bd.get_area_encounter_methods()
POKEMONES = read_bd.get_pokemons()
HABITATS = read_bd.get_habitats()

class Pokemon_encounter:
    def __init__(self, pokemon_name, area_name, encounter_method_rate, encounter_method_name, min_level, max_level, chance):
        self.pokemon_name = pokemon_name
        self.area_name = area_name
        self.encounter_method_rate = encounter_method_rate
        self.encounter_method_name = encounter_method_name
        self.min_level = min_level
        self.max_level = max_level
        self.chance = chance     

class Area:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.pokemon_encounters = self._set_pokemon_encounters()
        self.encounter_methods_rate = self._set_encounter_methods_rate()
        self.ecosystems = self._set_ecosystems()
        
    def _set_ecosystems(self):
        ecosystems = {}
        pokemon_list = self.get_pokemons()
        for pokemon in POKEMONES:
            if pokemon[1] in pokemon_list:
                ecosystem = None
                for habitat in HABITATS:
                    if habitat[0] == pokemon[13]:
                        ecosystem = habitat[1]
                        break
                if ecosystem not in ecosystems:
                    ecosystems[ecosystem] = []
                ecosystems[ecosystem].append(pokemon[1])
        return ecosystems
    
    def get_ecosystems(self):   
        return self.ecosystems
    
    def get_pokemons_by_ecosystem(self, ecosystem):
        return self.ecosystems[ecosystem]
        
    def _set_encounter_methods_rate(self):
        encounter_methods_rate = {}
        for element in AREA_ENCOUNTER_METHODS:
            if element[0] == self.id:
                encounter_method = None
                for method in ENCOUNTER_METHODS:
                    if method[0] == element[1]:
                        encounter_method = method[1]
                        break
                rate = element[2]
                encounter_methods_rate[encounter_method] = rate
        return encounter_methods_rate
    
    def _set_pokemon_encounters(self):
        pokemon_encounters = []
        for encounter in POKEMON_ENCOUNTERS:
            if encounter[1] == self.id:
                pokemon = None
                for p in POKEMONES:
                    if p[0] == encounter[0]:
                        pokemon = p[1]
                        break
                method_name = None
                for method in ENCOUNTER_METHODS:
                    if method[0] == encounter[2]:
                        method_name = method[1]
                        break
                method_rate = None
                for method in AREA_ENCOUNTER_METHODS:
                    if method[0] == self.id and method[1] == encounter[2]:
                        method_rate = method[2]
                        break
                pokemon_encounters.append(Pokemon_encounter(pokemon, self.name, method_rate, method_name, encounter[3], encounter[4], encounter[5]))      
        return pokemon_encounters
        
        
    def add_pokemon_encounter(self, encounter : Pokemon_encounter):
        self.pokemon_encounters.append(encounter)
        
    def get_pokemons(self):
        return [encounter.pokemon_name for encounter in self.pokemon_encounters]

    def use_encounter_method(self, encounter_method_name):
        '''
        Metodo que simula el uso de un metodo de encuentro en un area. Primero se determina si se encuentra un pokemon con el metodo proporcionado. Luego,
        si el encuentro es exitoso, se elige un pokemon de la lista de pokemons que se pueden encontrar en el area con el metodo de encuentro pasado como parametro.
        
        Parameters:
        encounter_method_name : str
            Nombre del metodo de encuentro a utilizar.
            
        Returns:
        tuple
            Tupla con el nombre del pokemon encontrado y el nivel del mismo.
        '''
        if encounter_method_name in self.encounter_methods_rate:
            rate = self.encounter_methods_rate[encounter_method_name]
            #rate: probabilidad de encontrar un pokemon con el metodo de encuentro encounter_method_name
            random_number = random.randint(0, 100)
            if random_number <= rate:
                rates = []
                pokemons = []
                level = 0
                for encounter in self.pokemon_encounters:
                    if encounter.encounter_method_name == encounter_method_name:
                        pokemons.append(encounter.pokemon_name)
                        rates.append(encounter.chance)
                        level = random.randint(encounter.min_level, encounter.max_level)
                        #El pokemon en el lugar i de la lista pokemons tiene la probabilidad en el lugar i de la lista rates
                return (random.choices(pokemons, rates), level)
            else:
                return None
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

class Location:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.areas = []
        
    def get_ecosystems(self):
        '''
        Metodo que retorna un diccionario con los ecosistemas presentes en la ubicacion y los pokemones que se pueden encontrar en cada uno.
        
        Returns:
        dict
            Diccionario con los ecosistemas presentes en la ubicacion y los pokemons que se pueden encontrar en cada uno.
        '''
        ecosystems = {}
        for area in self.areas:
            for ecosystem in area.ecosystems:
                if ecosystem not in ecosystems:
                    ecosystems[ecosystem] = []
                for pokemon in area.get_pokemons_by_ecosystem(ecosystem):
                    ecosystems[ecosystem].append(pokemon)
        return ecosystems
    
    def get_areas(self):
        return self.areas
        
    def add_area(self, area : Area):
        self.areas.append(area)
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    

class Map:
    nodes = []#locations
    connections = []
    
    def __init__(self, locations=None, connections=None):
        self.nodes = []
        self.connections = []
        if locations:
            for location in locations:
                self.add_node(location)
        if connections:
            for connection in connections:
                self.add_connection(connection[0], connection[1])
    
    def get_shortest_path(self, start:str, end:str):
        if start == end:
            return [start]
        
        visited = set()
        queue = deque([(start, [start])])
        
        while queue:
            location, path = queue.popleft()
            visited.add(location)
            
            for conn in self.connections:
                if conn[0].name == location and conn[1].name not in visited:
                    new_path = path + [conn[1].name]
                    if conn[1].name == end:
                        return new_path
                    queue.append((conn[1].name, new_path))
                elif conn[1].name == location and conn[0].name not in visited:
                    new_path = path + [conn[0].name]
                    if conn[0].name == end:
                        return new_path
                    queue.append((conn[0].name, new_path))
        return None
    
    def get_next_locations(self, location):
        next_locations = []
        for conn in self.connections:
            if conn[0].name == location:
                next_locations.append(conn[1].name)
            elif conn[1].name == location:
                next_locations.append(conn[0].name)
        return next_locations
    
    def get_areas(self, location):
        for node in self.nodes:
            if node.name == location:
                return node.areas
        return None
        
    def add_node(self, location):
        self.nodes.append(location)
    
    def add_connection(self, location1:str, location2:str):
        #Find the nodes wich names are location1 and location2
        node1 = None
        node2 = None
        for node in self.nodes:
            if node.name == location1:
                node1 = node
            elif node.name == location2:
                node2 = node
        if node1 and node2:
            self.connections.append((node1, node2))
        else:
            print("Error: One or both of the locations: " + location1 + ", " + location2 + " do not exist")
            
    def generate_random_connections(self):
        n = len(self.nodes)
        total_conns = random.randint(n-1, n*(n-1)//2)
        for i in range(total_conns):
            loc1 = random.choice(self.nodes)
            loc2 = random.choice(self.nodes)
            if loc1 != loc2:
                self.add_connection(loc1.name, loc2.name)
            else:
                i -= 1
            # Check if the graph is connected
            if i == total_conns-1:
                if not self._check_graph_connectivity():
                    self.connections = []
                    i = -1
                
    def _check_graph_connectivity(self):
        if not self.nodes:
            return False
        
        visited = set()
        queue = deque([self.nodes[0]])
        visited.add(self.nodes[0])
        
        while queue:
            node = queue.popleft()
            other_node = None
            
            for neighbor in self.connections:
                if neighbor[0] == node:
                    other_node = neighbor[1]
                elif neighbor[1] == node:
                    other_node = neighbor[0]
                
                if other_node not in visited:
                    visited.add(other_node)
                    queue.append(other_node)
        
        return len(visited) == len(self.nodes)
    
    def __str__(self):
        return "Nodes: " + str([node.name for node in self.nodes]) + "\nConnections: " + str([(conn[0].name, conn[1].name) for conn in self.connections])
    
    def get_location(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def get_area(self, name):
        for node in self.nodes:
            for area in node.areas:
                if area.name == name:
                    return area
        return None
    
    def get_all_locations(self):
        return [node.name for node in self.nodes]
          



def build_random_map():
    map = Map()
    for location in LOCATIONS:#location = (id, name, region_id) --> no se usa region_id
        map.add_node(Location(location[0], location[1]))
    for area in AREAS:#area = (id, name, location_id)
        for location in map.nodes:
            if location.id == area[2]:
                location.add_area(Area(area[0], area[1], location))
                break #Se asume que cada area pertenece a un solo 'location'
    map.generate_random_connections()
    return map

def build_kanto_map():
    map = Map()
    for location in LOCATIONS:#location = (id, name, region_id) --> no se usa region_id
        map.add_node(Location(location[0], location[1]))
    for area in AREAS:#area = (id, name, location_id)
        for location in map.nodes:
            if location.id == area[2]:#area[2] = location_id
                area_ = Area(area[0], area[1]) 
                location.add_area(area_)
                break #Se asume que cada area pertenece a un solo 'location'
    kanto_map(map)
    
    # for location in map.nodes:
    #     for area in location.areas:
    #         for encounter in POKEMON_ENCOUNTERS:
    #             if encounter[1] == area.id:
    #                 pokemon = None
    #                 for p in POKEMONES:
    #                     if p[0] == encounter[0]:
    #                         pokemon = p[1]
    #                         break
    #                 method_name = None
    #                 for method in ENCOUNTER_METHODS:
    #                     if method[0] == encounter[2]:
    #                         method_name = method[1]
    #                         break
    #                 method_rate = None
    #                 for method in AREA_ENCOUNTER_METHODS:
    #                     if method[0] == area.id and method[1] == encounter[2]:
    #                         method_rate = method[2]
    #                         break
    #                 area.add_pokemon_encounter(Pokemon_encounter(pokemon, area.name, method_rate, method_name, encounter[3], encounter[4], encounter[5]))
    return map

def kanto_map(map):
    map.add_connection("pallet-town", "kanto-route-1")
    map.add_connection("kanto-route-1", "viridian-city")
    map.add_connection("viridian-city", "kanto-route-2")
    map.add_connection("kanto-route-2", "mt-moon")
    map.add_connection("mt-moon", "kanto-route-4")
    map.add_connection("kanto-route-4", "cerulean-city")
    map.add_connection("cerulean-city", "kanto-route-5")
    map.add_connection("kanto-route-5", "saffron-city")
    map.add_connection("saffron-city", "kanto-route-6")
    map.add_connection("kanto-route-6", "vermilion-city")
    map.add_connection("saffron-city", "kanto-route-7")
    map.add_connection("kanto-route-7", "celadon-city")
    map.add_connection("saffron-city", "kanto-route-8")
    map.add_connection("kanto-route-8", "lavender-town")
    map.add_connection("kanto-route-10", "power-plant")
    map.add_connection("lavender-town", "kanto-route-10")
    map.add_connection("kanto-route-10", "rock-tunnel")
    map.add_connection("rock-tunnel", "kanto-route-9")
    map.add_connection("kanto-route-9", "cerulean-city")
    map.add_connection("vermilion-city", "kanto-route-11")
    map.add_connection("kanto-route-11", "digletts-cave")
    map.add_connection("digletts-cave", "kanto-route-2")
    map.add_connection("kanto-route-11", "kanto-route-12")
    map.add_connection("lavender-town", "kanto-route-12")
    map.add_connection("kanto-route-12", "kanto-route-13")
    map.add_connection("kanto-route-13", "kanto-route-14")
    map.add_connection("kanto-route-14", "kanto-route-15")
    map.add_connection("kanto-route-15", "fuchsia-city")
    map.add_connection("fuchsia-city", "kanto-route-18")
    map.add_connection("fuchsia-city", "kanto-sea-route-19")
    map.add_connection("kanto-sea-route-19", "seafoam-islands")
    map.add_connection("seafoam-islands", "kanto-sea-route-20")
    map.add_connection("kanto-sea-route-20", "cinnabar-island")
    map.add_connection("cinnabar-island", "kanto-sea-route-21")
    map.add_connection("cerulean-city", "kanto-route-24")
    map.add_connection("kanto-route-24", "kanto-route-25")
    map.add_connection("viridian-city", "kanto-route-22")
    map.add_connection("kanto-route-22", "kanto-route-23")
    map.add_connection("kanto-route-23", "kanto-route-26")
    map.add_connection("kanto-route-26", "kanto-route-27")
    map.add_connection("kanto-route-23", "kanto-victory-road-1")
    map.add_connection("kanto-victory-road-1", "kanto-victory-road-2")
    map.add_connection("kanto-victory-road-2", "indigo-plateau")
    map.add_connection("fuchsia-city", "kanto-safari-zone")
    map.add_connection("lavender-town", "pokemon-tower")
    map.add_connection("cerulean-cave", "kanto-route-4")
    map.add_connection("cinnabar-island", "pokemon-mansion")
        
