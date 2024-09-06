import read_bd
import random
from collections import deque

class Mapa:
    nodes = []#locations
    connections = []
    
    def __init__(self):
        self.nodes = []
        self.connections = []
        
    def add_node(self, location):
        self.nodos.append(location)
    
    def add_connection(self, location1, location2):
        self.aristas.append((location1, location2))
        
    def generate_random_connections(self):
        n = len(self.nodes)
        total_conns = random.randint(n-1, n*(n-1)//2)
        for i in range(total_conns):
            loc1 = random.choice(self.nodes)
            loc2 = random.choice(self.nodes)
            if loc1 != loc2:
                self.add_connection(loc1, loc2)
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
            
            for neighbor in self.connections:
                if neighbor[0] == node:
                    other_node = neighbor[1]
                elif neighbor[1] == node:
                    other_node = neighbor[0]
                
                if other_node not in visited:
                    visited.add(other_node)
                    queue.append(other_node)
        
        return len(visited) == len(self.nodes)
            
            

locations = read_bd.get_locations()
areas = read_bd.get_areas()          
    
class Location:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.ecosystems = []
        
class Area: 
    def __init__(self, id, name, location_id):
        self.id = id
        self.name = name
        self.location_id = location_id