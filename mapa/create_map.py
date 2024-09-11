import mapa.read_bd as read_bd
import random
from collections import deque
import random

locations = read_bd.get_locations()
areas = read_bd.get_areas()  
pokemon_encounters = read_bd.get_pokemon_encounters()
encounter_methods = read_bd.get_encounter_methods()
area_x_encounter_methods = read_bd.get_area_encounter_methods()
pokemons = read_bd.get_pokemons()

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
        self.name = name      #dict(encounter_method name, list[pokemon name])
        self.pokemon_encounters : list[Pokemon_encounter] = []
        self.encounter_methods_rate = {}
        
    def set_encounter_methods_rate(self, encounter_method, rate):
        self.encounter_methods_rate[encounter_method] = rate
        
        
    def add_pokemon_encounter(self, encounter : Pokemon_encounter):
        self.pokemon_encounters.append(encounter)
        
    def get_pokemons(self):
        return [encounter.pokemon_name for encounter in self.pokemon_encounters]

    def use_encounter_method(self, encounter_method_name):
        rates = []
        pokemons = []
        for encounter in self.pokemon_encounters:
            if encounter.encounter_method_name == encounter_method_name:
                pokemons.append(encounter.pokemon_name)
                rates.append(encounter.chance)
                #El pokemon en el lugar i de la lista pokemons tiene la probabilidad en el lugar i de la lista rates
        return random.choices(pokemons, rates)
        
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

class Location:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.areas = []
        
    def add_area(self, area : Area):
        self.areas.append(area)
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    

class Map:
    nodes = []#locations
    connections = []
    
    def __init__(self, locations, connections=None):
        self.nodes = []
        self.connections = []
        if locations:
            for location in locations:
                self.add_node(location)
        if connections:
            for connection in connections:
                self.add_connection(connection[0], connection[1])
    
    def get_next_locations(self, location):
        next_locations = []
        for conn in self.connections:
            if conn[0].name == location:
                next_locations.append(conn[1].name)
            elif conn[1].name == location:
                next_locations.append(conn[0].name)
        return next_locations
        
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
                if not self.bfs_check_connected():
                    self.connections = []
                    i = -1
                
    def bfs_check_connected(self):
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
    for location in locations:#location = (id, name, region_id) --> no se usa region_id
        map.add_node(Location(location[0], location[1]))
    for area in areas:#area = (id, name, location_id)
        for location in map.nodes:
            if location.id == area[2]:
                location.add_area(Area(area[0], area[1], location))
                break #Se asume que cada area pertenece a un solo 'location'
    map.generate_random_connections()
    return map

def build_kanto_map():
    map = Map()
    for location in locations:#location = (id, name, region_id) --> no se usa region_id
        map.add_node(Location(location[0], location[1]))
    for area in areas:#area = (id, name, location_id)
        for location in map.nodes:
            if location.id == area[2]:#area[2] = location_id
                #A partir de aqui se agregan los metodos de encuentro a cada area y sus tasas.
                area_ = Area(area[0], area[1], location)
                for element in area_x_encounter_methods:
                    if element[0] == area[0]:
                        encounter_method = None
                        for method in encounter_methods:
                            if method[0] == element[1]:
                                encounter_method = method[1]
                                break
                        rate = element[2]
                area_.set_encounter_methods_rate(encounter_method, rate)
                #Hasta aqui
                
                location.add_area(area_)
                break #Se asume que cada area pertenece a un solo 'location'
    kanto_map(map)
    
    for location in map.nodes:
        for area in location.areas:
            for encounter in pokemon_encounters:
                if encounter[1] == area.id:
                    pokemon = None
                    for p in pokemons:
                        if p[0] == encounter[0]:
                            pokemon = p[1]
                            break
                    method_name = None
                    for method in encounter_methods:
                        if method[0] == encounter[2]:
                            method_name = method[1]
                            break
                    method_rate = None
                    for method in area_x_encounter_methods:
                        if method[0] == area.id and method[1] == encounter[2]:
                            method_rate = method[2]
                            break
                    area.add_pokemon_encounter(Pokemon_encounter(pokemon, area.name, method_rate, method_name, encounter[3], encounter[4], encounter[5]))
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
    
    # Nodos
# locations = [
#     "Pallet Town", "Viridian City", "Pewter City", "Cerulean City",
#     "Vermilion City", "Lavender Town", "Celadon City", "Fuchsia City",
#     "Cinnabar Island", "Indigo Plateau",
#     "Route 1", "Route 2", "Route 3", "Route 4", "Route 5",
#     "Route 6", "Route 7", "Route 8", "Route 9", "Route 10",
#     "Route 11", "Route 12", "Route 13", "Route 14", "Route 15",
#     "Route 16", "Route 17", "Route 18"
# ]

# # Conexiones
# connections = [
#     ("Pallet Town", "Route 1"),
#     ("Route 1", "Viridian City"),
#     ("Viridian City", "Route 2"),
#     ("Route 2", "Pewter City"),
#     ("Pewter City", "Route 3"),
#     ("Route 3", "Cerulean City"),
#     ("Cerulean City", "Route 4"),
#     ("Route 4", "Vermilion City"),
#     ("Vermilion City", "Route 11"),
#     ("Route 11", "Lavender Town"),
#     ("Lavender Town", "Route 12"),
#     ("Route 12", "Celadon City"),
#     ("Celadon City", "Route 16"),
#     ("Route 16", "Fuchsia City"),
#     ("Fuchsia City", "Route 18"),
#     ("Cinnabar Island", "Route 21"),
#     ("Indigo Plateau", "Route 22")
# ]
    
class Area: 
    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location
    
class Location:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.areas = []
        
    def add_area(self, area : Area):
        self.areas.append(area)
        
