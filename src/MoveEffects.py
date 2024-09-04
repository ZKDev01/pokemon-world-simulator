from utils import *

# como vimos los efectos de los movimientos pueden clasificarse principalmente como: 
# 1. causan daño directamente en los hp del pokemon contrario con un número de n hits
# 2. inducen a estados de efectos negativos a los pokemones contrarios
# 3. aumentan o disminuyen las estadísticas de sí mismos o del pokemon contrario respectivamente

# los movimientos pertenecen al menos a una de estas categorías, la idea es crear 3 listas, y al buscar y ejecutar
# los efectos de estos se verifica si pertenecen o no a estas listas para aplicar dicho efecto, de manera que un 
# movimiento puede tener 3 efectos, entonces en la clase Move() la propiedad effects es un array de efectos, los 
# los cuales se efectuarán todos a la hora de ejecutar dicho movimiento
# por defecto todos los movimientos tendrán como efecto causar daño directo, la propiedad category de Move determinará
# si el movimiento tiene categoría status no ejecutará dicho efecto

# los movimientos tienen accuracy lo cual define la posibilidad de fallar un ataque

def normal_attack(move, pokemon1State, pokemon2State, turn):
    damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
    pokemon2State.hp -= damage
    pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State

def increase_critical_chance(move, pokemon1State, pokemon2State, turn):   # Move(self, name:str, power:int, pp:int, accuracy:int, type:str, category:str, ailment:str, target:str, effects)
    critical_prob = 8  
    damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State, critical_prob=critical_prob)
    pokemon2State.hp -= damage
    pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State
    
def hits_2_5_times(move, pokemon1State, pokemon2State, turn):
    r = random.randint(2,5)

    for i in range(r):
        accuracy = move.accuracy
        r_ = random.randint(1,)
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        if pokemon2State.hp <= 0:
            pokemon2State.hp = 0
            break
    
def perc_to_burn_10_perc(move, pokemon1State, pokemon2State, turn):
    r = random.randint(1, 10)

    if r == 1:
        if pokemon2State.type != 'fire':
            conditionState = ConditionState(name='quemado', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.negEffects.append(conditionState)

def perc_to_freeze_10_perc(move, pokemon1State, pokemon2State, turn):
    r = random.randint(1, 10)

    if r == 1:
        if pokemon2State.type != 'ice':
            conditionState = ConditionState(name='congelado', pokemon=pokemon2State.pokemon, turn=turn)
            conditionState_1 = ConditionState(name='congelado_v', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.negEffects.append(conditionState_1)
            pokemon2State.negEffects.append(conditionState)

def perc_to_paralyze_10_perc(move, pokemon1State, pokemon2State, turn):
    r = random.randint(1, 10)

    if r == 1:
        if pokemon1State.type != 'electric':
            conditionState = ConditionState(name='paralizado', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.negEffects.append(conditionState)

def one_hit_ko(move, pokemon1State, pokemon2State, turn):
    pokemon2State.hp = 0

def raises_atk_2_stages(move, pokemon1State, pokemon2State, turn):
    pokemon2State.attack = 3/10


move_effects = {
    'Inflicts regular damage with no additional effect.':[normal_attack],
    'Has an increased chance for a critical hit.':[increase_critical_chance],
    'Hits 2-5 times in one turn.':[hits_2_5_times],
    "Scatters money on the ground worth five times the user's level.":[normal_attack],
    "Has a 10_ chance to burn the target.":[normal_attack, perc_to_burn_10_perc],
    "Has a 10_ chance to freeze the target.":[normal_attack, perc_to_freeze_10_perc],
    "Has a 10_ chance to paralyze the target.":[normal_attack, perc_to_paralyze_10_perc],
    "Causes a one-hit KO.":[one_hit_ko],
    "Requires a turn to charge before attacking.":[normal_attack],   # pendiente
    "Raises the user's Attack by two stages.":[]
}






more_one_hit_moves = [hits_2_5_times]






numero_de_hits = []

efectos_inducen_estado_neg = []

efectos_aumentan_stats = []

efectos_disminuyen_stats = []