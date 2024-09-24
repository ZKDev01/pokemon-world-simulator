from utils import *
from Pokemon import *
from Item import *

#    Los entrenadores son los contenedores de los pokemones, estos son los que tomarán decisiones en las batallas,
# y los que recorreran el mapa en busca de los pokemones que estarán en el plan, los pokemones salvajes tendrán
# por defecto un entrenador fijo, que no se moverá por el mapa, solo se encargará de efectuar los movimientos en
# la batalla siguiendo alguna heurística

taskType_arr = ['subirNivel','obtainObject','obtainPokemon']





# por implementar, 

class Heuristic():
    def __init__(self, name):
        self.name = name





### Nota, cada entrenador tendrá un pequeño registro de lugares que ya ha visitado en el mapa, en el cual registrará el 
### camino hasta llegar a él, que será de la siguiente forma, empezará a crear un camino una vez que salga del lugar, y luego
### retrocederá en ese camino hasta llegar a dicho lugar, no tiene que ser a lo bruto, puede actualizar el camino que va 
### dejando, por ejemplo cuando da círculos o esa clase de situaciones etc

# action será las posibles acciones que el entrenador va a poder decidir fuera del combate, ejemplo ir hacia algun lugar 
# del mapa, 'comprar algún objeto', evolucionar a algún pokemon, darle algun objeto a un pokemon, cambiar de alineación, 
# deambular por la hierba en busca de combates, etc 


class Action():
    def __init__(self, name):
        self.name = name





### Nota: Todo entrenador se inicializa con un pokemon que escoge entre algunas opciones que se le brindarán

class Couch():
    def __init__(self, initialPokemon:Pokemon, heuristic:Heuristic, choose_team, name='salvaje'):   
        self.pokemonLider = initialPokemon   # es el pokemon que tendrá en primera posición, el pokemon que sale al encontrarse un pokemon salvaje
        self.pokemons = []
        self.deck = []
        self.name = name
        self.heuristic = heuristic
        
        self.ideal_team = choose_team()   # una función que le proporciona el equipo con el que quiere combatir el entrenador

        self.listToDo = []       # una lista de tareas por hacer


    # le pasan una situacion y dependiendo de la tarea que esté ejecutando ahora mismo el entrenador decide que movimiento hacer
    # falta como posibles movimientos huir de la pelea, cambiar de pokemon, etc

    def GetMove_at_Battle(self, myPokemonState:PokemonState, oponentPokemonState:PokemonState):

        #pendiente
        myPokemon = myPokemonState.pokemon  # de tipo Pokemon
        oponentPokemon = oponentPokemonState.pokemon

        totalMyPokemonMoves = len(myPokemon.moves)
        r = random.randint(0, totalMyPokemonMoves)

        return myPokemon.moves[r]      #por ahora devuelve un movimiento aleatorio
                                       #por implementar activar un objeto

    



# los entrenadores tendrán un conjunto de tareas para llegar a la meta(conformar el mazo propuesto


class Task():
    def __init__(self, taskType:str, lvl:int =None, pokemon:Pokemon=None, item:Item=None):

        if taskType == taskType_arr[0]:  # subir nivel, entonces estamos seguros que se proporcionó un nivel a alcanzar y un pokemon
            self.type = taskType
            self.pokemon = pokemon
            self.lvl_a_alcanzar = lvl
        elif taskType == taskType_arr[1]: # obtainObject, entonces estamos seguros de que proporcionó un objeto 
            self.type = taskType
            self.item = item
        else:
            self.type = taskType
            self.pokemon = pokemon   # obtain pokemon, entonces estamos seguros de que proporcionó un pokemon

    # por implementar, tiene relación con la clase Action
    def DoTask(self, ):
        pass
