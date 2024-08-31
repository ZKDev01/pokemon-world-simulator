import random
import sqlite3
import json
#from move import *

conn = sqlite3.connect('pokedex.db')
cursor = conn.cursor()

with open('growth_rate_data.json', 'r') as file:
    growth_rate_data = json.load(file)

types_arr = ['normal','fighting','flying','poison','ground','rock','bug','ghost','steel','fire','water','grass','electric','psychic','ice','dragon','dark','fairy']

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
    [1   ,2   ,1   ,0.5 ,1   ,1   ,1   ,1   ,0.5 ,0.5 ,1   ,1   ,1   ,1   ,1   ,2   ,2   ,1   ]
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


def OrderByLearnedAtLvl(pokemon_moves_at_lvl:list):
    result = []

    while(len(pokemon_moves_at_lvl) != 0):
        min_move = 100
        min_index = 0

        for i in range(len(pokemon_moves_at_lvl)):
            move_lvl = pokemon_moves_at_lvl[i][2]
            if move_lvl < min_move:
                min_index = i
                min_move = move_lvl

        result.append(pokemon_moves_at_lvl[min_index])
        pokemon_moves_at_lvl.remove(pokemon_moves_at_lvl[min_index])
    
    if len(result) <= 4:
        return result
    else:
        return result[-4:]
    

# fórmula para calcular el daño ocasionado por un ataque basándose en los stats de los pokemones

def GetDamage(move, attacker_pokemon_state, attacked_pokemon_state):  # Tipos: (Move, PokemonState, PokemonState)
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

    r = random.randint(1, 16)
    criticat_mod = 2 if r == 1 else 1   # la probabilidad de critico es 1 en 16, aplica el doble de daño en rojo fuego
    
    aleatory_mod = random.uniform(0.85, 1.00)


    result = (((atker_lvl*2/5 + 2) * move_power * (atker_stat/atked_stat)) / 50 + 2) * type_mod * stab_mod * criticat_mod * aleatory_mod

    return result

# prioridad de las acciones y movimientos, se toma como other el resto de los movimientos, que luego se 
# verificara como que el movimiento no se encuentre en el diccionario, para ahorrar tiempo, ya que se trabajará
# solamente con la primera generación

prioridad_de_acciones = {
    'cambiar pokemon':2,
    'usar objeto':2,
    'huir':2,
    'quick-attack':1,
    'other':0,
    'counter':-1
}

# estados efímeros: se padecen solo estando en combate
ephemeral_states = ['confuso', 'enamorado', 'drenado', 'maldito', 'canto maldito', 'atrapado']

# estados persistentes: se padecen incluso fuera de combate
persistent_states = ['paralizado', 'quemado', 'envenenado', 'gravemente envenenado', 'dormido', 'congelado']

# tipos de efectos que hay:
# 1. afectan los stats del pokemon
# 2. afectan a si ejecuta un movimiento o no
# 3. inducen al adversario o a el mismo a un efecto negativo o positivo respectivamente
# 4. reducen o aumentan la vida del pokemon(no se incluye en los stats porque esto ocuerre al final del turno)

# 1. Afectan stats:

def confuso(pokemon):
    pass



# las condiciones de estado tendrán un tipo, que determinará cual de las funciones va a activar, dependiendo de como se 
# definan, por ejemplo parálisis determina si el pokemon se va a move cuando le toque atacar, mientras que si tiene algún
# efecto que le reduzca stats se activa otro efecto y al iniciar el turno

class ConditionState():
    def __init__(self, name, type, pokemon):
        self.name = name
        self.type = type
    
    def ActivateEffect(self, pokemon):
        pass
