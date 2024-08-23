import pokebase as pb

def get_mapa(region_id):
    region = pb.region(region_id)
    locations = []
    for i in range(len(region.locations)):
        location = region.locations[i]
        locations.append(location)
        
class Location:
    def __init__(self, location):
        self.name = location.name
        self.id = location.id
        self.region_id = location.region_id
        self.areas = self.get_areas(location)
        
    def get_areas(self, location):
        areas = []
        for i in range(len(location.areas)):
            area = location.areas[i]
            areas.append(area.name)
        return areas
        
        

        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    

