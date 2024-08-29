import random
import sqlite3
from move import *
import json

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

#   Ataque     Defensa  AtEspecial DefEspecial     Velocidad                (en este caso no esta el hp, luego el hp estara de primero en la lista de stats)
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

class Item():
    def __init__(self, id, name, cost, category, effect):
        self.id = id
        self.name = name
        self.cost = cost
        self.category = category
        self.effect = effect



# aqui pokemon es de tipo Pokemon, lo que por razones de que esta la clase debajo, no se puede hacer el tipado
class PokemonState():
    def __init__(self, pokemon, type, lvl, negEffect, posEffect, hp, attack, defense, specialAttack, specialDefense, speed):    #aqui negEffect(Paralisis, etc) posEffect(Pociones, etc)
        self.pokemon = pokemon
        self.type = type
        self.lvl = lvl
        self.negEffect = negEffect
        self.posEffect = posEffect
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.specialAttack = specialAttack
        self.specialDefense = specialDefense
        self.speed = speed


class Pokemon():   # por ahora clase lista
    def __init__(self, id, name, types, height, weight, base_experience, growth_rate, generation, # todos estos stats son de tipo int exceptuando el growth_rate, la generation y el name
                 hp, attack, defense, specialAttack, specialDefense, speed, lvl): 
                                                                               
        self.id = id
        self.name = name
        self.type = types[random.randint(0,len(types))]
        self.base_experience = base_experience
        self.height = height
        self.weight = weight
        #self.abilities = abilities
        #self.forms = forms
        #self.held_items = held_items
        #self.locations_areas = locations_areas
        #self.moves = moves
        #self.past_types = past_types
        #self.species = species
        self.growth_rate = growth_rate
        #self.stats = stats
        #self.types = types
        self.generation = generation
        self.invetory = []   #inventario de objetos

        self.lvl = lvl
        self.learnedMoves = AsignMoves(self)

        self.exp_table = growth_rate_data[self.growth_rate]['levels']    #devuelve una lista de nivel-cant_de_exp_necesaria
        
        self.exp = self.exp_table[self.lvl - 1]['experience']
        self.next_exp_level = self.exp_table[self.lvl]['experience']    

        indiv_values = [random.randint(0,31) for i in range(6)]     #los individual values son valores entre 0 y 31 que tiene cada pokemon aleatoriamente al crearse
                                                                    #comienza en hp y continua con la lista de stats de arriba
        #indiv_values es de la forma attack_defense_specialAttack_specialDefense_speed
        self.i_hp = indiv_values[0]
        self.ev_hp = 0

        self.i_attack = indiv_values[1]
        self.ev_attack = 0

        self.i_defense = indiv_values[2]
        self.ev_defense = 0

        self.i_specialAttack = indiv_values[3]
        self.ev_specialAttack = 0

        self.i_specialDefense = indiv_values[4]
        self.ev_specialDefense = 0

        self.i_speed = indiv_values[5]
        self.ev_speed = 0

        #Para determinar los stats de un pokemon salvaje encontrado hay que tener en cuenta diferentes factores como son
        #el nivel, valores individuales(IVs), naturaleza(firme por ejemplo), valores de esfuerzo(en un pokemon salvaje 
        #generalmente son 0. Los valores individuales varian entre cada tipo de pokemon de 0 hasta 31)
        # HP = ((2*Base + IV + EV/4)/100)*lvl + lvl + 10
        # others = ((2*Base + IV + EV/4)/100)*Nivel + 5 


        self.b_hp = hp           #primero para cada stat le asignamos su valor base, para luego 
        self.b_attack = attack       #actualizarlo con el valor real, es seguro ya que se crea el pokemon una sola vez
        self.b_defense = defense
        self.b_special_attack = specialAttack
        self.b_special_defense = specialDefense
        self.b_speed = speed     # b de base

        r = random.randint(0, len(natures_arr))
        self.nature = natures_arr[r]          #por ahora le asignaremos una naturaleza al encontrar el pokemon, ya sea
                                          #que este en lvl 1 o lvl 100

        #aqui no tendremos en cuenta los efforts values, que se obtienen al derrotar otros pokemones
        #ya que los que al inicializar un pokemon estos son salvajes

        self.SubirNivel(self.lvl)

        # inicializamos el estado actual del pokemon
        self.actualState = PokemonState(self, self.type, self.lvl, None, None, self.hp, 
                                        self.attack, self.defense, self.special_attack, self.special_defense, self.speed)  #pendiente a arreglar


    # Se efectua al inicializar el pokemon y cada vez que este sube de nivel,
    # actualiza los stats

    def SubirNivel(self, lvl):
        
        self.hp = ((2*self.b_hp + self.i_hp + self.ev_hp/4)/100)*lvl + lvl + 10
        self.attack = ((2*self.b_attack + self.i_hp + self.ev_attack/4)/100)*lvl + 5
        self.defense = ((2*self.b_defense + self.i_defense + self.ev_defense/4)/100)*lvl + 5
        self.special_attack = ((2*self.b_special_attack + self.i_specialAttack + self.ev_specialAttack/4)/100)*lvl + 5
        self.special_defense = ((2*self.b_special_defense + self.i_specialDefense + self.ev_specialDefense/4)/100)*lvl + 5
        self.speed = ((2*self.b_speed + self.i_speed + self.ev_speed/4)/100)*lvl + 5

        #aplicamos el porciento de la caracteristica nature del pokemon
        nature_index = IndexToNature(self.nature)

        self.attack = self.attack * natures_matrix[nature_index][0]
        self.defense = self.defense * natures_matrix[nature_index][1]
        self.special_attack = self.special_attack * natures_matrix[nature_index][2]
        self.special_defense = self.special_defense * natures_matrix[nature_index][3]
        self.speed = self.speed * natures_matrix[nature_index][4]


    # Actualiza los puntos de crecimiento del pokemon, se actualiza al terminar cada batalla

    def ObtenerExp(self, exp, ev_hp=0, ev_attack=0, ev_defense=0, ev_specialAttack=0, ev_specialDefense=0, ev_speed=0):
        self.exp += exp
        if self.exp >= self.next_exp_level:
            self.lvl += 1
            self.next_exp_level = self.exp_table[self.lvl]['experience']
            self.SubirNivel(self.lvl)
            # pendiente si llega a un nivel en que puede aprender un mivimiento nuevo o si puede evolucionar
        self.ev_hp += ev_hp
        self.ev_attack += ev_attack
        self.ev_defense += ev_defense
        self.ev_specialAttack += ev_specialAttack
        self.ev_specialDefense += ev_specialDefense
        self.ev_speed += ev_speed



# Actualiza el estado del pokemon para el combate, ejemplo se actualiza cada cierto tiempo, 
# cada cierto tiempo el pokemon se cura, o cuando se le proporciona una pocion curativa o algo parecido

    # Por implemetar

    def UpdatePokemonState(self, pokemon, updateType, pokemonState:PokemonState=None, move=Move, potion=None): # pokemon es de Tipo Pokemon

            updateTypeArr = ['attack', 'home', 'potion', 'effects']

            if (updateType == updateTypeArr[1]):
                pass           # entonces estamos seguros de que se proporciono un movimiento y un estado de pokemon, que seria el estado del pokemon contrari
            
            elif (updateType == updateTypeArr[2]):
                pokemonState.hp = pokemon.hp
                pokemonState.attack = pokemon.attack
                pokemonState.defense = pokemon.defense
                pokemonState.specialAttack = pokemon.special_attack
                pokemonState.specialDefense = pokemon.special_defense
                pokemonState.speed = pokemon.speed
                pokemonState.negEffect = None    #por ahora, es como si no tuviera efectos negativos, verificar luego en la base de datos
                pokemonState.posEffect = None    #igual que efectos negativos
            else:
                if potion == 'curarParalisis':    #por ahora dejemoslo asi, luego seguro se creara una funcion para por cada pocion de la bd hacer el efecto indicado
                    pokemonState.negEffect = None
            


        

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

def AsignMoves(pokemon:Pokemon):
    result = [0, 0, 0, 0]

    pokemon_id = pokemon.id
    pokemon_lvl = pokemon.lvl

    cursor.execute(f'SELECT pokemon_id, move_id, learned_at_level FROM Pokemon_Moves WHERE pokemon_id = {pokemon_id}')
    pokemon_moves = cursor.fetchall()

    pokemon_moves_at_lvl = []

    for i in range(len(pokemon_moves)):
        if pokemon_moves[i][2] == 0 or pokemon_moves[i][2] > pokemon_lvl:
            continue
        else:
            pokemon_moves_at_lvl.append(pokemon_moves[i])

    # ordenamos en orden ascendente segun el lvl y nos quedamos con los 4 ultimos
    pokemon_moves_at_lvl = OrderByLearnedAtLvl(pokemon_moves_at_lvl)

    for i in range(len(pokemon_moves_at_lvl)):
        pokemon_move = pokemon_moves_at_lvl[i]
        pokemon_move_id = pokemon_move[1]

        cursor.execute(f'SELECT * FROM Moves WHERE id = {pokemon_move_id}')
        m = cursor.fetchall()[0]

        move = Move(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8]) # move(id, name, power, pp, accuracy, type_id, category, ailment, target, effect)
        result[i] = move
    
    return result




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
    

