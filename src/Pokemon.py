from utils import *


        

class PokemonState():
    def __init__(self, pokemon, type, lvl, hp, attack, defense, specialAttack, specialDefense, speed):    #aqui negEffect(Paralisis, etc) posEffect(Pociones, etc)
        self.pokemon = pokemon
        self.type = type
        self.lvl = lvl
        self.negEffects = []   # serán del tipo ConditionState
        self.posEffects = []
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
                                                                    #comienza en hp y continúa con la lista de stats de arriba
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
        #generalmente son 0. Los valores individuales varían entre cada tipo de pokemon de 0 hasta 31)
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

        #aquí no se tendrá en cuenta los efforts values, que se obtienen al derrotar otros pokemones
        #ya que los que al inicializar un pokemon estos son salvajes

        self.SubirNivel(self.lvl)

        # inicializamos el estado actual del pokemon
        self.actualState = PokemonState(self, self.type, self.lvl, self.hp, 
                                        self.attack, self.defense, self.special_attack, self.special_defense, self.speed)  #pendiente a arreglar


    # Se efectúa al inicializar el pokemon y cada vez que este sube de nivel,
    # actualiza los stats

    def SubirNivel(self, lvl):
        
        self.hp = ((2*self.b_hp + self.i_hp + self.ev_hp/4)/100)*lvl + lvl + 10
        self.attack = ((2*self.b_attack + self.i_hp + self.ev_attack/4)/100)*lvl + 5
        self.defense = ((2*self.b_defense + self.i_defense + self.ev_defense/4)/100)*lvl + 5
        self.special_attack = ((2*self.b_special_attack + self.i_specialAttack + self.ev_specialAttack/4)/100)*lvl + 5
        self.special_defense = ((2*self.b_special_defense + self.i_specialDefense + self.ev_specialDefense/4)/100)*lvl + 5
        self.speed = ((2*self.b_speed + self.i_speed + self.ev_speed/4)/100)*lvl + 5

        #aplicamos el porciento de la característica nature del pokemon
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
            # pendiente si llega a un nivel en que puede aprender un movimiento nuevo o si puede evolucionar
        self.ev_hp += ev_hp
        self.ev_attack += ev_attack
        self.ev_defense += ev_defense
        self.ev_specialAttack += ev_specialAttack
        self.ev_specialDefense += ev_specialDefense
        self.ev_speed += ev_speed



# Actualiza el estado del pokemon para el combate, ejemplo se actualiza cada cierto tiempo, 
# cada cierto tiempo el pokemon se cura, o cuando se le proporciona una poción curativa o algo parecido

    # Por implemetar

    def UpdatePokemonState(self, pokemon, updateType, pokemonState:PokemonState=None, hp=0, potion=None, posEffects=None, negEffects=None): # pokemon es de Tipo Pokemon

            updateTypeArr = ['attack', 'home', 'potion', 'positive effects', 'negative effects']

            if (updateType == updateType[0]):   # si es de tipo ataque entonces hay seguridad de que se proporcionó un estado de pokemon, un hp que sería el daño ocasionado
                pokemonState.hp -= hp
                if pokemonState.hp <= 0:
                    pokemonState.hp = 0

            
            elif (updateType == updateTypeArr[1]):
                pokemonState.hp = pokemon.hp
                pokemonState.attack = pokemon.attack
                pokemonState.defense = pokemon.defense
                pokemonState.specialAttack = pokemon.special_attack
                pokemonState.specialDefense = pokemon.special_defense
                pokemonState.speed = pokemon.speed
                pokemonState.negEffect = None    #por ahora, es como si no tuviera efectos negativos, verificar luego en la base de datos
                pokemonState.posEffect = None    #igual que efectos negativos

                
            elif (updateType == updateTypeArr[2]):
                pass           # entonces estamos seguros de que se proporcionó una potion

            elif (updateType == updateTypeArr[3]):   # entonces estamos seguros de que se proporcionó un conjunto de estados positivos
                for i in range(len(posEffects)):
                    pokemon.actualState.posEffects.append(posEffects[i])

            elif (updateType == updateTypeArr[4]):   # entonces estamos seguros de que se proporcionó un conjunto de estados negativos
                for i in range(len(negEffects)):
                    pokemon.actualState.negEffects.append(negEffects[i])
            
