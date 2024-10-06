from Agente import *
from Communication_and_Tasks import *
from EventoInesperado import *

task1 = Task(pokemon=1)
task2 = Task(pokemon=2)
task3 = Task(pokemon=3)

meta = [
    task1,
    task2,
    task3,
]

#meta1 = Objetivo(pokemones=[1, 2, 3])

agente = Agente(meta=meta, creencias=None, mapa=None)

information = Afirmation(pokemon=1, coordenada=(0,1))
evento = Event(informacion=information)


agente.RecibirEventoInesperado(evento=evento)

