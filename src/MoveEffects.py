from utils import *
import bd.read_bd as read_bd

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
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
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
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
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
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
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
    
def lowers_atk_onestage(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        pokemon2State.attack = pokemon2State.attack * 0.67
        return False
    return True

def put_to_sleep(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        condition = ConditionState(name='dormido', pokemon=pokemon2State.pokemon, turn=turn, turnsDuration=random.randint(1,5))
        condition1 = ConditionState(name='dormido_v', pokemon=pokemon2State.pokemon, turn=turn)
        pokemon2State.negEffects.append(condition)
        pokemon2State.negEffects.append(condition1)
        return False
    return True

def confuses_target(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        condition = ConditionState(name='confuso', pokemon=pokemon2State.pokemon, turn=turn)
        pokemon2State.negEffects.append(condition)
        return False
    return True

def inflige_20_danio(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        pokemon2State.hp -= 20
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State
        return False
    return True

def lowers_specialDefense_onestage(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        pokemon2State.specialDefense = pokemon2State.specialDefense * 0.67
        return False
    return True

def perc_to_lowers_specialDefense_onestage(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        r = random.randint(1, 10)
        if r == 1:
            lowers_specialDefense_onestage(move, pokemon1State, pokemon2State, turn)

        return False
    return True

def perc_to_confuses_10(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
    
        r = random.randint(1, 10)
        if r == 1:
            condition = ConditionState(name='confuso', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.neEffects.append(condition)

        return False
    return True

def perc_to_lowers_speed_10(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r == 1:
            pokemon2State.speed = pokemon2State.speed * 0.67

        return False
    return True

def perc_to_lowers_atk_10(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r == 1:
            pokemon2State.attack = pokemon2State.attack * 0.67

        return False
    return True

def more_damage_to_heavier_limit_120(move, pokemon1State, pokemon2State, turn):
    initial_move_power = move.power

    peso = pokemon2State.pokemon.weight
    if peso < 10:
        move.power = 20
    elif peso < 25:
        move.power = 40
    elif peso < 50:
        move.power = 60
    elif peso < 100:
        move.power = 80
    elif peso < 200:
        move.power = 100
    else:
        move.power = 120

    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        return False

    move.power = initial_move_power
    return True

def inflicts_damage_equal_to_lvl(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        lvl = pokemon1State.lvl

        pokemon2State.hp -= lvl
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        return False
    return True

def drains_half_damage(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
    
        pokemon1State.hp += damage/2
        pokemon1State.hp = pokemon1State.pokemon.hp if pokemon1State.hp >= pokemon1State.pokemon.hp else pokemon1State.hp

        return False
    return True

def seeds_to_target(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy and pokemon2State.type != 'grass':
        condition = ConditionState(name='drenado', pokemon=pokemon2State.pokemon, turn=turn)
        pokemon2State.negEffects.append(condition)

        return False
    return True

def raise_atk_onestage(move, pokemon1State, pokemon2State, turn):
    pokemon1State.attack = pokemon1State.attack * 1.5
    return False

def raise_specialAtk_onestage(move, pokemon1State, pokemon2State, turn):
    pokemon1State.specialAttack = pokemon1State.specialAttack * 1.5
    return False

def raise_dfs_onestage(move, pokemon1State, pokemon2State, turn):
    pokemon1State.defense = pokemon1State.defense * 1.5
    return False

def raise_specialDfs_onestage(move, pokemon1State, pokemon2State, turn):
    pokemon1State.specialDefense = pokemon1State.specialDefense * 1.5

def poison_target(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        condition = ConditionState(name='envenenado', pokemon=pokemon2State.pokemon, turn=turn)

def paralyze_target(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        condition = ConditionState(name='paralizado', pokemon=pokemon2State.pokemon, turn=turn)
        return False
    return True

def lowers_speed_twostage(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        pokemon2State.speed = pokemon2State.speed * 0.5
        return False
    return True

def inflicts_40_ofdamage(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp -= 40
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        return False
    return True

def badly_poisons(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        condition = ConditionState(name='gravemente envenenado', pokemon=pokemon2State.pokemon, turn=turn)
        return False
    return True

def raises_speed_two_stages(move, pokemon1State, pokemon2State, turn):
    pokemon1State.speed = pokemon1State.speed *2
    return False

def lowers_defense_twostages(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        pokemon2State.defense = pokemon2State.defense * 0.5
        return False
    return True

def heals_halfHpMax(move, pokemon1State, pokemon2State, turn):
    total_hp = pokemon1State.pokemon.hp
    pokemon1State.hp += total_hp
    pokemon1State.hp = total_hp if pokemon1State.hp >= total_hp else pokemon1State.hp
    return False

def raises_defense_onestage(move, pokemon1State, pokemon2State, turn):
    pokemon1State.defense = pokemon1State.defense * 1.5
    return False

def raises_defense_twostages(move, pokemon1State, pokemon2State, turn):
    pokemon1State.defense = pokemon1State.defense * 2
    return False

def resets_stats(move, pokemon1State, pokemon2State, turn):
    pokemon = pokemon1State.pokemon
    pokemon1State.attack = pokemon.attack
    pokemon1State.defense = pokemon.defense
    pokemon1State.specialAttack = pokemon.specialAttack
    pokemon1State.specialDefense = pokemon.specialDefense
    pokemon1State.speed = pokemon.speed

def random_move(move, pokemon1State, pokemon2State, turn):
    moves = read_bd.get_moves()
    
    r = random.randint(0, len(moves))
    move = moves[r]
    move = Move(name=move[0], power=move[1], pp=move[2], accuracy=move[3], type=move[4], category=move[5], ailment=move[6], target=move[7], effects=move_effects[move[8]])

    return move.DoMove(pokemon1State=pokemon1State, pokemon2State=pokemon2State, turn=turn)

def user_faints(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        pokemon1State.hp = 0
        return False
    return True

def perc_to_poisons_40(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 4:
            condition = ConditionState(name='envenenado', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.negEffects.append(condition)

        return False
    return True

def perc_to_target_flinchs_10(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r == 1:
            condition = ConditionState(name='flaqueado', pokemon=pokemon2State.pokemon, turn=turn)
            condition1 = ConditionState(name='flaqueado_v', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.negEffects.append(condition)
            pokemon2State.negEffects.append(condition1)
        return False
    return True

def perc_to_target_flinchs_20(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 2:
            condition = ConditionState(name='flaqueado', pokemon=pokemon2State.pokemon, turn=turn)
            condition1 = ConditionState(name='flaqueado_v', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.negEffects.append(condition)
            pokemon2State.negEffects.append(condition1)
        return False
    return True

def never_misses(move, pokemon1State, pokemon2State, turn):
    initial_acurracy = move.accuracy
    move.accuracy = 1000
    r = random.randint(1, 100)
    if r <= move.accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        move.accuracy = initial_acurracy
        return False
    move.accuracy = initial_acurracy
    return True
    
def raises_specialDfs_twostages(move, pokemon1State, pokemon2State, turn):
    pokemon1State.specialDefense = pokemon1State.specialDefense * 2
    return False

def dream_eater(move, pokemon1State, pokemon2State, turn):
    negEffects = pokemon2State.negEffects
    aplicar = False
    for i in range(len(negEffects)):
        if negEffects[i].name == 'dormido':
            aplicar = True
    if aplicar:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        pokemon1State.hp += damage/2
        pokemon1State.hp = pokemon1State.pokemon.hp if pokemon1State.hp >= pokemon1State.pokemon.hp else pokemon1State.hp

        return False
    else:
        return True
    
def perc_to_confuses_20(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 2:
            condition = ConditionState(name='confuso', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.negEffects.append(condition)
        return False
    return True

def inflicts_damage_betwen_50_150_to_lvl(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        r = random.randint(50, 150)
        perc = r/100
        damage = pokemon1State.lvl * perc
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        return False
    return True

def splash(move, pokemon1State, pokemon2State, turn):
    return False

def conversion(move, pokemon1State, pokemon2State, turn):
    initial_type = pokemon1State.type
    moves = pokemon1State.pokemon.learnedMoves
    moves_types = [moves[0].type, moves[1].type, moves[2].type, moves[3].type]

    r = random.randint(0, 3)
    pokemon1State.type = moves_types[r]
    return False

def perc_to_burn_20(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, accuracy)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State

        r = random.randint(1, 10)

        if r <= 2:
            if pokemon2State.type != 'fire' and not quemado in pokemon2State.negEffects:
                conditionState = ConditionState(name='quemado', pokemon=pokemon2State.pokemon, turn=turn)
                pokemon2State.negEffects.append(conditionState)
        return False
    else:
        return True

def perc_to_freeze_20(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, accuracy)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State

        r = random.randint(1, 10)

        if r <= 2:
            if pokemon2State.type != 'ice' and not congelado in pokemon2State.negEffects:
                conditionState = ConditionState(name='congelado', pokemon=pokemon2State.pokemon, turn=turn)
                conditionState_1 = ConditionState(name='congelado_v', pokemon=pokemon2State.pokemon, turn=turn)
                pokemon2State.negEffects.append(conditionState_1)
                pokemon2State.negEffects.append(conditionState)
        return False
    else:
        return True

def perc_to_paralyze_20(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, accuracy)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State

        r = random.randint(1, 10)

        if r <= 2:
            if pokemon1State.type != 'electric' and not paralizado in pokemon2State.negEffects:
                conditionState = ConditionState(name='paralizado', pokemon=pokemon2State.pokemon, turn=turn)
                pokemon2State.negEffects.append(conditionState)
        return False
    else:
        return True

def perc_to_burn_paralyze_freeze_20(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(2, 10)
        if r <= 2:
            r = random.randint(1, 3)
            if r == 1:
                return perc_to_burn_20(move, pokemon1State, pokemon2State, turn)
            elif r == 2:
                return perc_to_freeze_20(move, pokemon1State, pokemon2State, turn)
            else:
                return perc_to_paralyze_20(move, pokemon1State, pokemon2State, turn)
    return True

def inflicts_half_hp(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = pokemon2State.hp/2
        pokemon2State.hp -= damage
        #pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        return False
    return True





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
    "Lowers the target's Attack by one stage.":[lowers_atk_onestage],
    "Puts the target to sleep.":[put_to_sleep],
    "Confuses the target.":[confuses_target],
    "Inflicts 20 points of damage.":[inflige_20_danio],
    "Disables the target's last used move for 1-8 turns.":[],   # pendiente
    "Has a 10_ chance to lower the target's Special Defense by one stage.":[perc_to_lowers_specialDefense_onestage],
    "Protects the user's stats from being changed by enemy moves.":[], # pendiente
    "Inflicts regular damage and can hit Dive users.":[normal_attack], # pendiente la parte de Dive
    "Has a 10_ chance to confuse the target.":[perc_to_confuses_10],
    "Has a 10_ chance to lower the target's Speed by one stage.":[perc_to_lowers_speed_10],
    "Has a 10_ chance to lower the target's Attack by one stage.":[perc_to_lowers_atk_10],
    "User foregoes its next turn to recharge.":[],    # pendiente
    "Inflicts more damage to heavier targets, with a maximum of 120 power.":[more_damage_to_heavier_limit_120],
    "Inflicts twice the damage the user received from the last physical hit it took.":[],  # pendiente
    "Inflicts damage equal to the user's level.":[inflicts_damage_equal_to_lvl],
    "Drains half the damage inflicted to heal the user.":[drains_half_damage],
    "Seeds the target, stealing HP from it every turn.":[seeds_to_target],
    "Raises the user's Attack and Special Attack by one stage.":[raise_atk_onestage, raise_specialAtk_onestage],
    "Poisons the target.":[poison_target],
    "Paralyzes the target.":[paralyze_target],
    "Lowers the target's Speed by two stages.":[lowers_speed_twostage],
    "Inflicts 40 points of damage.":[inflicts_40_ofdamage],
    "Inflicts regular damage and can hit Dig users.":[normal_attack],     # pendiente lo de dig users
    "User digs underground, dodging all attacks, and hits next turn.":[],  # pendiente
    "Badly poisons the target, inflicting more damage every turn.":[badly_poisons],
    "Raises the user's Attack by one stage.":[raise_atk_onestage],
    "Raises the user's Speed by two stages.":[raises_speed_two_stages],
    "If the user is hit after using this move, its Attack rises by one stage.":[],  # pendiente usando registro de movimientos de los pokemones
    "Immediately ends wild battles.  No effect otherwise.":[],   # pendiete, se resuelve poniendo un if en clash de teleport
    "Copies the target's last used move.":[],   # pendiente, se resuelve con registro de movimientos del couch
    "Lowers the target's Defense by two stages.":[lowers_defense_twostages],
    "Raises the user's evasion by one stage.":[],  # pendiente de implementar, ojo evasion de los pokemones, evasion base 100%
    "Heals the user by half its max HP.":[heals_halfHpMax],
    "Raises the user's Defense by one stage.":[raises_defense_onestage],
    "Raises the user's evasion by two stages.":[],   # pendiente a implementar evasion de los pokemones
    "Raises user's Defense by one stage.":[raises_defense_onestage],
    "Raises the user's Defense by two stages.":[raises_defense_twostages],
    "Reduces damage from special attacks by 50_ for five turns.":[],  # pendiente efectos positivos
    "Resets all Pokémon's stats, accuracy, and evasion.":[],   # pendiente lo de la evasion y la precision
    "Reduces damage from physical attacks by half.":[], # pendiente crear efectos positivos
    "Increases the user's chance to score a critical hit.":[],  # pendiente crear efectos positivos
    "User waits for two turns, then hits back for twice the damage it took.":[], # pendiente crear efecto negativo, o efecto positivo
    "Randomly selects and uses any move in the game.":[random_move],
    "Uses the target's last used move.":[], # pendiente con los registros de movimientos de los couchs
    "User faints.":[user_faints],
    "Has a 40_ chance to poison the target.":[perc_to_poisons_40],
    "Has a 10_ chance to make the target flinch.":[perc_to_target_flinchs_10],
    "Has a 20_ chance to make the target flinch.":[perc_to_target_flinchs_20],
    "Never misses.":[never_misses],
    "Raises the user's Defense by one stage.  User charges for one turn before attacking.":[],  # pendiente estados positivos
    "Raises the user's Special Defense by two stages.":[raises_specialDfs_twostages],
    "Only works on sleeping Pokémon.  Drains half the damage inflicted to heal the user.":[dream_eater],
    "User charges for one turn before attacking.  Has a 30_ chance to make the target flinch.":[],   # pendiente estados positivos y ultimo movimiento
    "User becomes a copy of the target until it leaves battle.":[],  # transform pendiente
    "Has a 20_ chance to confuse the target.":[perc_to_confuses_20],
    "Inflicts damage between 50_ and 150_ of the user's level.":[inflicts_damage_betwen_50_150_to_lvl],
    "Does nothing.":[splash],
    "User sleeps for two turns, completely healing itself.":[], # pendiente efectos positivos
    "User's type changes to the type of one of its moves at random.":[conversion],  # pendiente efecto negativo o positivo que al final del combate se reestableza el tipo inicial del pokemon
    "Has a 20_ chance to burn, freeze, or paralyze the target.":[perc_to_burn_paralyze_freeze_20],
    "Inflicts damage equal to half the target's HP.":[inflicts_half_hp],
    "Transfers 1/4 of the user's max HP into a doll, protecting the user from further damage or status changes until it breaks.":[],  # pendiente substitute, muito complejo
    "User takes 1/4 its max HP in recoil.":[recoil_un_cuarto],
    "Permanently becomes the target's last used move.":[],   # pendiente registro de movimientos de los entrenadores
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