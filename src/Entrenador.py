from utils import *
from Pokemon import *
from move import *
from Item import *

#    Los entrenadores son los contenedores de los pokemones, estos son los que tomaran decisiones en las batallas,
# y los que recorreran el mapa en busca de los pokemones que estaran en el plan, los pokemones salvajes tendran
# por defecto un entrenador fijo, que no se movera por el mapa, solo se encargara de efectuar los movimientos en
# la batalla siguiendo alguna heuristica

taskType_arr = ['subirNivel','obtainObject','obtainPokemon']





# por implementar, 

class Heuristic():
    def __init__(self, name):
        self.name = name





### Nota, cada entrenador tendra un pequenio registro de lugares que ya ha visitado en el mapa, en el cualr registrara el 
### camino hasta llegar a el, que sera de la siguiente forma, empezara a crear un camino una vez que salga del lugar, y luego
### retrocedera en ese camino hasta llegar a dicho lugar, no tiene que ser a lo bruto, puede actualizar el camino que va 
### dejando, por ejemplo cuando da circulos o esa clase de situaciones etc

# action sera las posibles acciones que el entrenador va a poder decidir fuera del combate, ejemplo ir hacia algun lugar 
# del mapa, 'comprar algun objeto', evolucionar a algun pokemon, darle algun objeto a un pokemon, cambiar de alineacion, 
# deambular por la hierba en busca de combates, etc 


class Action():
    def __init__(self, name):
        self.name = name





### Nota: Todo entrenador se inicializa con un pokemon que escoge entre algunas opciones que se le brindaran

class Couch():
    def __init__(self, initialPokemon:Pokemon, heuristic:Heuristic, name='salvaje',):   
        self.pokemonLider = initialPokemon   # es el pokemon que tendra en primera posicion, el pokemon que sale al encontrarse un pokemon salvaje
        self.pokemons = []
        self.deck = []
        self.name = name
        self.heuristic = heuristic

        self.listToDo = []       # una lista de tareas por hacer


    # le pasan una situacion y dependiendo de la tarea que este ejecutando ahora mismo el entrenador decide que movimiento hacer
    # falta como posibles movimientos huir de la pelea, cambiar de pokemon, etc

    def GetMove_at_Battle(self, myPokemonState:PokemonState, oponentPokemonState:PokemonState):

        myPokemon = myPokemonState.pokemon  # de tipo Pokemon
        oponentPokemon = oponentPokemonState.pokemon

        totalMyPokemonMoves = len(myPokemon.moves)
        r = random.randint(0, totalMyPokemonMoves)

        return myPokemon.moves[r]      #por ahora devuelve un movimiento aleatorio
                                       #por implementar activar un objeto

    



# los entrenadores tendran un conjunto de tareas para llegar a la meta(conformar el mazo propuesto


class Task():
    def __init__(self, taskType:str, lvl:int =None, pokemon:Pokemon=None, item:Item=None):

        if taskType == taskType_arr[0]:  # subir nivel, entonces estamos seguros que proporcionaron un nivel a alcanzar y un pokemon
            self.type = taskType
            self.pokemon = pokemon
            self.lvl_a_alcanzar = lvl
        elif taskType == taskType_arr[1]: # obtainObject, entonces estamos seguros de que proporciono un objeto 
            self.type = taskType
            self.item = item
        else:
            self.type = taskType
            self.pokemon = pokemon   # obtain pokemon, entonces estamos seguros de que proporciono un pokemon

    # por implementar, tiene relacion con la clase Action
    def DoTask(self, ):
        pass
