class Event():
    def __init__(self, pokemon=None, agente=None, informacion=None):
        self.type = None
        if pokemon != None and agente == None and informacion == None:
            self.type = 'pokemon'
            self.pokemon = pokemon
        elif pokemon == None and agente != None and informacion == None:
            self.type = 'agente'
            self.agente = agente
        elif pokemon == None and agente == None and informacion != None:
            self.type = 'informacion'
            self.informacion = informacion
    
    def __str__(self) -> str:
        return self.type