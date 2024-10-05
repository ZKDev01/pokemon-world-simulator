from Communication_and_Tasks import *
from EventoInesperado import *

'''
    Cada agente tiene una meta, que no es mas que un conjunto de objetivos
    Un objetivo es algo que se quiere lograr pero aun no se ha logrado, para lograrlo hay que cumplir
una o varias tareas
    Una Tarea es algo en especifico que para cumplirse el agente debe tomar accion directa en funcion a ello, cada
tarea tiene bien definido lo que hay que hacer para cumplirla
'''

class Agente():
    def __init__(self, meta, creencias, mapa):
        self.informacion_relevante = []
        self.informacion_relevante_temporal = []
        self.meta = meta
        self.tareas = []
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
        self.informacion_relevante_temporal.append(information)
        #self.VerificarInformacionRelevante  #verifica que la informacion que obtuvo puede influir en la realizacion de objetivos

    

