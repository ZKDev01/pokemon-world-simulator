from Communication_and_Tasks import *
from EventoInesperado import *

'''
    Cada agente tiene una meta, que no es mas que un conjunto de objetivos
    Un objetivo es algo que se quiere lograr pero aun no se ha logrado, para lograrlo hay que cumplir
una o varias tareas
    Una Tarea es algo en especifico que para cumplirse el agente debe tomar accion directa en funcion a ello, cada
tarea tiene bien definido lo que hay que hacer para cumplirla

    La informacion se clasifica por el momento en Pokemon, Agente o Propuesta
'''

class Agente():
    def __init__(self, meta, creencias, mapa):
        self.informacion_relevante = {
            'Pokemon': [],
            'Agente': [],
            'Propuesta': [],
        }
        self.informacion_relevante_temporal = {
            'Pokemon': [],
            'Agente': [],
            'Propuesta': [],
        }
        self.meta = meta
        self.tareas = []
        for i in range(len(self.meta)):
            self.tareas.append(self.meta[i])
        self.pokemon_inventory = []
        self.creencias = creencias
        self.mapa = mapa  


    def RecibirEventoInesperado(self, evento:Event):
        if evento.type == 'agente':
            information = Afirmation(agente=evento.agente, coordenada=self.mapa.getActualCoordenate) # esta propiedad del mapa devuelve la posicion actual del agente
            self.AgregarInfoTemporal(information=information)

        elif evento.type == 'pokemon':
            information = Afirmation(pokemon=evento.pokemon, coordenada=self.mapa.getActualCoordenate)
            self.AgregarInfoTemporal(information=information)

        elif evento.type == 'information':
            self.AgregarInfoTemporal(evento.informacion)





    def AgregarInfoTemporal(self, information):
        if not self.VerificarRelevancia(information=information):
            tipos = information.type
            for i in range(len(tipos)):
                self.informacion_relevante_temporal[tipos[i]].append(information)


    # se llama cada vez que el agente recibe una informacion, aqui decide si almacenarla permanente o temporalmente
    def VerificarRelevancia(self, information):
        if  'Pokemon' in information.type:
            for item in self.tareas:
                if not item.cumplida:
                    if item.type == 'Pokemon':
                        pokemon_tarea = ObtenerPokemonDeInf(information=item.task)
                        pokemon_info = ObtenerPokemonDeInf(information=information)
                        if pokemon_tarea == pokemon_info:
                            if information not in self.informacion_relevante['Pokemon']:
                                self.informacion_relevante['Pokemon'].append(information)
                                return True   # por ahora solo se verifican las de tipo pokemon porque las tareas son de tipo 'Obtener Pokemon x'
        
        elif 'Propuesta' in information.type:
            for item in self.tareas:
                if not item.cumplida:
                    if item.type == 'Pokemon':
                        pokemon_tarea = ObtenerPokemonDeInf(information=item.task)
                        pokemon_prop = ObtenerPokemonDeInf(information=information)
                        if pokemon_tarea == pokemon_prop:
                            if information not in self.informacion_relevante['Propuesta']:
                                self.informacion_relevante['Propuesta'].append(information)

                                
        

    
def ObtenerPokemonDeInf(self, information):
    words = information.split(' ')
    for i in range(len(words)):
        if words[i] == 'Pokemon':
            return words[i+1]
    raise Exception(f'No esta la palabra "Pokemon" en la informacion {information}')
