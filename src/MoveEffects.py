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
# cada método devuelve True si falla el ataque, y False si aserta
def normal_attack(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, accuracy)
    if r <= accuracy:    # aqui se define si un movimiento falla o no
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State
        return False
    else:
        return True

def increase_critical_chance(move, pokemon1State, pokemon2State, turn):   # Move(self, name:str, power:int, pp:int, accuracy:int, type:str, category:str, ailment:str, target:str, effects)
    critical_prob = 8  
    accuracy = move.accuracy
    r = random.randint(1, accuracy)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State, critical_prob=critical_prob)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State
        return False
    else:
        return True
    
def hits_2_5_times(move, pokemon1State, pokemon2State, turn):
    r = random.randint(2,5)

    for i in range(r):
        accuracy = move.accuracy
        r_ = random.randint(1,accuracy)
        if r <= accuracy:
            damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
            pokemon2State.hp -= damage
            if pokemon2State.hp <= 0:
                pokemon2State.hp = 0
                break
        else:
            continue
    return False
    
def perc_to_burn_10(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, accuracy)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State

        r = random.randint(1, 10)

        if r == 1:
            if pokemon2State.type != 'fire' and not quemado in pokemon2State.negEffects:
                conditionState = ConditionState(name='quemado', pokemon=pokemon2State.pokemon, turn=turn)
                pokemon2State.negEffects.append(conditionState)
        return False
    else:
        return True
    

def perc_to_freeze_10(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, accuracy)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State

        r = random.randint(1, 10)

        if r == 1:
            if pokemon2State.type != 'ice' and not congelado in pokemon2State.negEffects:
                conditionState = ConditionState(name='congelado', pokemon=pokemon2State.pokemon, turn=turn)
                conditionState_1 = ConditionState(name='congelado_v', pokemon=pokemon2State.pokemon, turn=turn)
                pokemon2State.negEffects.append(conditionState_1)
                pokemon2State.negEffects.append(conditionState)
        return False
    else:
        return True

def perc_to_paralyze_10(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, accuracy)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State

        r = random.randint(1, 10)

        if r == 1:
            if pokemon1State.type != 'electric' and not paralizado in pokemon2State.negEffects:
                conditionState = ConditionState(name='paralizado', pokemon=pokemon2State.pokemon, turn=turn)
                pokemon2State.negEffects.append(conditionState)
        return False
    else:
        return True
    
def one_hit_ko(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, accuracy)
    if r <= accuracy:
        pokemon2State.hp = 0
        return False
    else:
        return True


def raises_atk_2_stages(move, pokemon1State, pokemon2State, turn):
    pokemon2State.attack = (3/10) * pokemon2State.attack

def has_30_perc_to_make_flinch(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, accuracy)
    if r <= accuracy:
        r = random.randint(1,10)
        if r <= 3:
            pokemon2State.hp = 0
        else:
            damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
            pokemon2State.hp -= damage
            pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        return False
    else:
        return True

def miss_then_take_halfdamage(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)

    damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
    if r <= accuracy:
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        return False
    else:
        pokemon1State.hp -= damage/2
        pokemon1State.hp = 0 if pokemon1State.hp <= 0 else pokemon1State.hp
        return True

def lowers_accuracy_onestage(move, pokemon1State, pokemon2State, turn):
    pokemon2State.negEffects.append()   # pendiente agregar efecto negativo que disminuya la puntería del pokemon contrario

def percent_to_paralize_30(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        r = random.randint(1, 10)
        if r <= 3:
            if pokemon2State.type != 'electric' and not paralizado in pokemon2State.negEffects:
                condition = ConditionState(name='paralizado', pokemon=pokemon1State.pokemon, turn=turn)
                condition_v = ConditionState(name='paralizado_v', pokemon=pokemon1State.pokemon, turn=turn)
                pokemon2State.negEffects.append(condition_v)
                pokemon2State.negEffects.append(condition)
    else:
        return True

def recoil_un_cuarto(move, pokemon1State, pokemon2State, turn):
    if move.name != 'struggle':
        accuracy = move.accuracy
        r = random.randint(1, 100)
        if r <= accuracy:
            damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
            pokemon2State.hp -= damage
            pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State.hp

            pokemon1State.hp -= damage/4
            pokemon1State.hp = 0 if pokemon1State.hp <= 0 else pokemon1State.hp
            return False
        else:
            return True
        

    else:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        pokemon1State.hp -= damage/4
        pokemon1State.hp = 0 if pokemon1State.hp <= 0 else pokemon1State.hp
        return False

def hits_2_3_times_and_confused(move, pokemon1State, pokemon2State, turn):
    pass # pendiente

def recoil_un_tercio(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State

        pokemon1State.hp -= damage/3
        pokemon1State.hp = 0 if pokemon1State.hp <= 0 else pokemon1State.hp

        return False
    else:
        return True

def lowers_target_defense_onestage(move, pokemon1State, pokemon2State, turn):
    pokemon2State.defense = pokemon2State.defense * 0.67

def perc_to_poison_30(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 3:
            if pokemon2State.type != 'poison' and envenenado not in pokemon2State.negEffects and not gravemente_envenenado in pokemon2State.negEffects:
                condition = ConditionState(name='envenenado', pokemon=pokemon2State.pokemon, turn=turn)
                pokemon2State.negEffects.append(condition)
        return False
    else:
        return True

def hits_twice_perc_to_poison_20(move, pokemon1State, pokemon2State, turn):
    miss = True

    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 2:
            if pokemon2State.type != 'poison' and envenenado not in pokemon2State.negEffects and not gravemente_envenenado in pokemon2State.negEffects:
                condition = ConditionState(name='envenenado', pokemon=pokemon2State.pokemon, turn=turn)
                pokemon2State.negEffects.append(condition)
        miss = False
   
    r = random.randint(1, 100)
    if r <= accuracy:
        damage - GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 100)
        if r <= 2:
            if pokemon2State.type != 'poison' and envenenado not in pokemon2State.negEffects and not gravemente_envenenado in pokemon2State.negEffects:
                condition = ConditionState(name='envenenado', pokemon=pokemon2State.pokemon, turn=turn)
                pokemon2State.negEffects.append(condition)
        miss = False

    return miss
    
    




move_effects = {
    'Inflicts regular damage with no additional effect.':[normal_attack],
    'Has an increased chance for a critical hit.':[increase_critical_chance],
    'Hits 2-5 times in one turn.':[hits_2_5_times],
    "Scatters money on the ground worth five times the user's level.":[normal_attack],
    "Has a 10_ chance to burn the target.":[perc_to_burn_10],
    "Has a 10_ chance to freeze the target.":[normal_attack, perc_to_freeze_10],
    "Has a 10_ chance to paralyze the target.":[normal_attack, perc_to_paralyze_10],
    "Causes a one-hit KO.":[one_hit_ko],
    "Requires a turn to charge before attacking.":[normal_attack],   # pendiente
    "Raises the user's Attack by two stages.":[raises_atk_2_stages],
    "Inflicts regular damage and can hit Pokémon in the air.":[normal_attack], # pendiente
    "Immediately ends wild battles.  Forces trainers to switch Pokémon.":[],    # agregar efecto negativo extra que sea forzar el cambio de pokemon
    "User flies high into the air, dodging all attacks, and hits next turn.":[], # crear estado positivo donde es inmune a golpes
    "Prevents the target from fleeing and inflicts damage for 2-5 turns.":[],   # crear estado negativo en el que el pokemon atacado no pueda infligir daño durante de 2 a 5 turnos
    "Has a 30_ chance to make the target flinch.":[has_30_perc_to_make_flinch],
    "Hits twice in one turn.":[normal_attack, normal_attack],
    "If the user misses, it takes half the damage it would have inflicted in recoil.":[miss_then_take_halfdamage],
    "Lowers the target's accuracy by one stage.":[],  # pendiente
    "Has a 30_ chance to paralyze the target.":[percent_to_paralize_30],
    "User receives 1/4 the damage it inflicts in recoil.":[recoil_un_cuarto],
    "Hits every turn for 2-3 turns, then confuses the user.":[], # pendiente crear un estado positivo que se mantenga atacando durante 2 o 3 turnos consecutivos
    "User receives 1/3 the damage inflicted in recoil.":[recoil_un_tercio],
    "Lowers the target's Defense by one stage.":[lowers_target_defense_onestage],
    "Has a 30_ chance to poison the target.":[perc_to_poison_30],
    "Hits twice in the same turn.  Has a 20_ chance to poison the target.":[hits_twice_perc_to_poison_20],
}






more_one_hit_moves = [hits_2_5_times]






numero_de_hits = []

efectos_inducen_estado_neg = []

efectos_aumentan_stats = []

efectos_disminuyen_stats = []

# reducción de stats según los stages: 
# +6 -> x4     400%
# +5 -> x3.5   350%
# +4 -> x3     300%
# +3 -> x2.5   250%
# +2 -> x2     200%
# +1 -> x1.5   150%
#  0 -> x1     100%
# -1 -> x0.67    67%
# -2 -> x0.5    50%
# -3 -> x0.4    40%
# -4 -> x0.33   33%
# -5 -> x0.29   29%
# -6 -> x0.25   25%