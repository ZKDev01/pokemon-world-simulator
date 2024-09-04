import random
import sqlite3
import json

from Move import *

conn = sqlite3.connect('pokedex.db')
cursor = conn.cursor()

with open('growth_rate_data.json', 'r') as file:
    growth_rate_data = json.load(file)

types_arr = ['normal','fighting','flying','poison','ground','rock','bug','ghost','steel','fire','water','grass','electric','psychic','ice','dragon','dark','fairy', 'confuso']
                                                                                                                                        # aquí agregamos en ultimo lugar confuso para evitar errores, como se afecta a si mismo no importa de que tipo sea
#         normal fighting ...
#normal
#fighting
#...

types_matrix = [
    [1   ,1   ,1   ,1   ,1   ,0.5 ,1   ,0   ,0.5 ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ],
    [2   ,1   ,0.5 ,0.5 ,1   ,2   ,0.5 ,0   ,2   ,1   ,1   ,1   ,1   ,0.5 ,2   ,1   ,2   ,0.5 ],
    [1   ,2   ,1   ,1   ,1   ,0.5 ,2   ,1   ,0.5 ,1   ,1   ,2   ,0.5 ,1   ,1   ,1   ,1   ,1   ],
    [1   ,1   ,1   ,0.5 ,0.5 ,0.5 ,1   ,0.5 ,0   ,1   ,1   ,2   ,1   ,1   ,1   ,1   ,1   ,2   ],
    [1   ,1   ,0   ,2   ,1   ,2   ,0.5 ,1   ,2   ,2   ,1   ,0.5 ,2   ,1   ,1   ,1   ,1   ,1   ],
    [1   ,0.5 ,2   ,1   ,0.5 ,1   ,2   ,1   ,0.5 ,2   ,1   ,1   ,1   ,1   ,2   ,1   ,1   ,1   ],
    [1   ,0.5 ,0.5 ,0.5 ,1   ,1   ,1   ,0.5 ,0.5 ,0.5 ,1   ,2   ,1   ,2   ,1   ,1   ,2   ,0.5 ],
    [0   ,1   ,1   ,1   ,1   ,1   ,1   ,2   ,1   ,1   ,1   ,1   ,1   ,2   ,1   ,1   ,0.5 ,1   ],
    [1   ,1   ,1   ,1   ,1   ,2   ,1   ,1   ,0.5 ,0.5 ,0.5 ,1   ,0.5 ,1   ,2   ,1   ,1   ,2   ],
    [1   ,1   ,1   ,1   ,1   ,0.5 ,2   ,1   ,2   ,0.5 ,0.5 ,2   ,1   ,1   ,2   ,0.5 ,1   ,1   ],
    [1   ,1   ,1   ,1   ,2   ,2   ,1   ,1   ,1   ,2   ,0.5 ,0.5 ,1   ,1   ,1   ,0.5 ,1   ,1   ],
    [1   ,1   ,0.5 ,0.5 ,2   ,2   ,0.5 ,1   ,0.5 ,0.5 ,2   ,0.5 ,1   ,1   ,1   ,0.5 ,1   ,1   ],
    [1   ,1   ,2   ,1   ,0   ,1   ,1   ,1   ,1   ,1   ,2   ,0.5 ,0.5 ,1   ,1   ,0.5 ,1   ,1   ],
    [1   ,2   ,1   ,2   ,1   ,1   ,1   ,1   ,0.5 ,1   ,1   ,1   ,1   ,0,5 ,1   ,1   ,0   ,1   ],
    [1   ,1   ,2   ,1   ,2   ,1   ,1   ,1   ,0.5 ,0.5 ,0.5 ,2   ,1   ,1   ,0.5 ,2   ,1   ,1   ],
    [1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,0.5 ,1   ,1   ,1   ,1   ,1   ,1   ,2   ,1   ,0   ],
    [1   ,0.5 ,1   ,1   ,1   ,1   ,1   ,2   ,1   ,1   ,1   ,1   ,1   ,2   ,1   ,1   ,0.5 ,0.5 ],
    [1   ,2   ,1   ,0.5 ,1   ,1   ,1   ,1   ,0.5 ,0.5 ,1   ,1   ,1   ,1   ,1   ,2   ,2   ,1   ],
    [1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ]
]

stats_arr = ['attack','defense','special attack','special defense','speed']

natures_arr = ['hardly','bold','modest','calm','timid','lonely','docile','mild','gentle','hastly',
           'adamant','impish','bashful','careful','jolly','naughty','lax','rash','quirky',
           'naive','brave','relaxed','quiet','sassy','serious']

#   Ataque     Defensa  AtEspecial DefEspecial     Velocidad                (en este caso no esta el hp, luego el hp estará de primero en la lista de stats)
#hardly
#bold
#...
#serious
natures_matrix = [
    [1.0,        1.0,        1.0,        1.0,        1.0],
    [0.9,        1.1,        1.0,        1.0,        1.0],
    [0.9,        1.0,        1.1,        1.0,        1.0],
    [0.9,        1.0,        1.0,        1.1,        1.0],
    [0.9,        1.0,        1.0,        1.0,        1.1],
    
    [1.1,        0.9,        1.0,        1.0,        1.0],
    [1.0,        1.0,        1.0,        1.0,        1.0],
    [1.0,        0.9,        1.1,        1.0,        1.0],
    [1.0,        0.9,        1.0,        1.1,        1.0],
    [1.0,        0.9,        1.0,        1.0,        1.1],

    [1.1,        1.0,        0.9,        1.0,        1.0],
    [1.0,        1.1,        0.9,        1.0,        1.0],
    [1.0,        1.0,        1.0,        1.0,        1.0],
    [1.0,        1.0,        0.9,        1.1,        1.0],
    [1.0,        1.0,        0.9,        1.0,        1.1],

    [1.1,        1.0,        1.0,        0.9,        1.0],
    [1.0,        1.1,        1.0,        0.9,        1.0],
    [1.0,        1.0,        1.1,        0.9,        1.0],
    [1.0,        1.0,        1.0,        1.0,        1.0],
    [1.0,        1.0,        1.0,        0.9,        1.1],

    [1.1,        1.0,        1.0,        1.0,        0.9],
    [1.0,        1.1,        1.0,        1.0,        0.9],
    [1.0,        1.0,        1.1,        1.0,        0.9],
    [1.0,        1.0,        1.0,        1.1,        0.9],
    [1.0,        1.0,        1.0,        1.0,        1.0],
]




# aqui pokemon es de tipo Pokemon, lo que por razones de que esta la clase debajo, no se puede hacer el tipado


        

def IndexToNature(nature):
    for i in range(len(natures_arr)):
        if nature == natures_arr[i]:
            return i
    raise ValueError(f'no hay natures de tipo {nature}')

def IndexToStat(stat):
    for i in range(len(stats_arr)):
        if stat == stats_arr[i]:
            return i
    raise ValueError(f'no hay stat de tipo {stat}')

def IndexToType(type):
    for i in range(len(types_arr)):
        if type == types_arr[i]:
            return i
    raise ValueError('el type proporcionado no existe')



# fórmula para calcular el daño ocasionado por un ataque basándose en los stats de los pokemones

def GetDamage(move, attacker_pokemon_state, attacked_pokemon_state, critical_prob=24) -> int:  # Tipos: (Move, PokemonState, PokemonState)
    move_power = move.power
    atker_lvl = attacked_pokemon_state.lvl
    move_category = move.category

    atker_stat = attacker_pokemon_state.attack if move_category == 'physical' else attacker_pokemon_state.specialAttack
    atked_stat = attacked_pokemon_state.defense if move_category == 'physical' else attacked_pokemon_state.specialDefense

    move_type = move.type
    atked_pok_type = attacked_pokemon_state.type
    
    move_type_index = IndexToType(move_type)
    atked_pok_type_index = IndexToType(atked_pok_type)

    type_mod = types_matrix[move_type_index][atked_pok_type_index]   # modificador de daño con respecto al tipo de mov y el tipo de pokemon atacado

    stab_mod = 1.5 if attacker_pokemon_state.type == move_type else 1  # si el tipo del pokemon atacante coincide con el tipo de movimiento entonces se aplica bonificación

    r = random.randint(1, critical_prob)
    criticat_mod = 2 if r == 1 else 1   # la probabilidad de crítico es 1 en 24, aplica el doble de daño en rojo fuego
    
    aleatory_mod = random.uniform(0.85, 1.00)


    result = (((atker_lvl*2/5 + 2) * move_power * (atker_stat/atked_stat)) / 50 + 2) * type_mod * stab_mod * criticat_mod * aleatory_mod

    return round(result) #devuelve un entero con la cantidad de daño

# prioridad de las acciones y movimientos, se toma como other el resto de los movimientos, que luego se 
# verificará como que el movimiento no se encuentre en el diccionario, para ahorrar tiempo, ya que se trabajará
# solamente con la primera generación

prioridad_de_acciones = {
    'cambiar pokemon':2,
    'usar objeto':2,
    'huir':2,
    'quick-attack':1,
    'extreme-speed':1,
    'other':0,
    'counter':-1,
    'whirl-pool':-1,
    'roar':-1,
}

# estados efímeros: se padecen solo estando en combate
ephemeral_states = ['confuso', 'enamorado', 'drenado', 'maldito', 'canto maldito', 'atrapado, dormido']

# estados persistentes: se padecen incluso fuera de combate
persistent_states = ['paralizado', 'quemado', 'envenenado', 'gravemente envenenado', 'congelado']

# tipos de efectos que hay:
# 1. afectan los stats del pokemon
# 2. afectan a si ejecuta un movimiento o no
# 3. inducen al adversario o a el mismo a un efecto negativo o positivo respectivamente
# 4. reducen o aumentan la vida del pokemon(no se incluye en los stats porque esto ocuerre al final del turno)
# 5. evitan que el pokemon pueda ser intercambiado

# 1. Afectan stats:

# 2. Afectan si ejecuta el movimiento o no:

def confuso(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):
    move = Move('movimiento confuso', 40, 100, 100, 18, 'physical', 'none', 'selected-pokemon', 'Inflicts regular damage with no additional effect.')

    r = random.randint(1, 3)

    if r == 1:
        damage = GetDamage(move, pokemon1.actualState, pokemon1.actualState)
        pokemon1.UpdatePokemonState(pokemon1, updateType='attack', hp=damage)
        return True
    
    else:
        return False

def enamorado(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):
    r = random.randint(1, 2)

    if r == 1:
        return True
    else:
        return False
    
def paralizado(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):
    pokemon1.actualState.speed = pokemon1.speed/2

    r = random.randint(1, 4)
    
    if r == 1:
        return True
    else:
        return False


def congelado(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):
    return True

def dormido(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):
    r = random.randint(1, 5)
    if r >= turn - activationTurn:
        return True
    else:
        return False
    
    
afectan_ejecucion_de_movimiento = [confuso, enamorado, paralizado, congelado, dormido]

# 4 reducen o aumentan los puntos de vida del pokemon

def maldito(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):   # pendiente ver si es de su vida maxima o de su vida actual
    state = pokemon1.actualState
    state.hp -= pokemon1.hp/4

def drenado(activationTurn, turn, turnDuration, pokemon1, pokemon2, atMap=False):
    state1 = pokemon1.actualState
    state2 = pokemon2.actualState

    totalLive = pokemon1.hp/8
    state1 -= totalLive
    state2 += totalLive

def cantoMortal(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):  # pendiente
    pass

def envenenado(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):
    state = pokemon1.actualState

    if(atMap):
        state.hp -= 1
    else:
        state.hp -= pokemon1.hp/8

def gravemente_envenenado(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):
    state = pokemon1.actualState

    if(atMap):
        state.hp -= 1
    else:
        state.hp -= pokemon1.hp * (1/16 * (turn - activationTurn + 1)) 

def quemado(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):
    pokemon1.actualState.attack = pokemon1.attack/2

    state = pokemon1.actualState

    if not atMap:
        state.hp -= pokemon1.hp/8

afectan_puntos_de_vida = [maldito, drenado, cantoMortal, envenenado, quemado]

# métodos en los que los pokemones puede salir de ciertos estados como congelación

def congelado_v(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):
    r = random.randint(1, 5)
    if r == 1:
        negEffects = pokemon1.actualState.negEffects
        for i in range(len(negEffects)):
            if negEffects[i].name == 'congelado' or negEffects[i].name == 'congelado_v':
                negEffects.remove(negEffects[i])

def paralisis_v(activationTurn, turn, turnDuration, pokemon1, pokemon2=None, atMap=False):
    r = random.randint(1, 4)
    if r == 1:
        negEffects = pokemon1.actualState.negEffects
        for i in range(len(negEffects)):
            if negEffects[i].name == 'paralisis' or negEffects[i].name == 'paralisis_v':
                negEffects.remove(negEffects[i])
        

verificar_salida_del_estado = [congelado_v, paralisis_v]



# las condiciones de estado tendrán un tipo, que determinará cual de las funciones va a activar, dependiendo de como se 
# definan, por ejemplo parálisis determina si el pokemon se va a move cuando le toque atacar, mientras que si tiene algún
# efecto que le reduzca stats se activa otro efecto y al iniciar el turno

class ConditionState():
    def __init__(self, name, pokemon, turn, turnsDuration=None):
        self.name = name
        self.effect = globals().get(name)

        if self.effect in afectan_ejecucion_de_movimiento:
            self.type = 'afectanEjecucionDeMovimiento'
        elif self.effect in afectan_puntos_de_vida:
            self.type = 'afectanPuntosDeVida'
        else:
            self.type = 'afectanCambio'
        
        self.activationTurn = turn
        self.turnDuration = turnsDuration
    
    def ActivateEffect(self, turn, pokemon1, pokemon2=None, atMap=False):
        self.effect(self.activationTurn, turn, self.turnDuration, pokemon1, pokemon2, atMap)

# se revisará a qué grupo pertenece la condición, y dependiendo de ello, se definirá la inicialización de la clase
