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
    pokemon1State.hp += total_hp / 2
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
    cursor.execute("SELECT * FROM Moves")

    moves = cursor.fetchall()
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

def triple_kick(move, pokemon1State, pokemon2State, turn):
    initial_power = move.power
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        move.power = move.power + initial_power
    
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        move.power = move.power + initial_power

    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        move.power = move.power + initial_power

    move.power = initial_power

    return False

def prevents_leave_to_battle(move, pokemon1State, pokemon2State, turn):
    condition = ConditionState(name='dont_leave_battle')
    pokemon2State.negEffects.append(condition)
    return False

def nightmare(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        condition = ConditionState(name='pesadilla_v', pokemon=pokemon2State.pokemon, turn=turn)
        condition1 = ConditionState(name='pesadilla', pokemon=pokemon2State.pokmeon, turn=turn)

        pokemon2State.negEffects.append(condition)
        pokemon2State.negEffects.append(condition1)
        
        return False
    return True

def perc_to_flinch_30_if_is_sleeped(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        do_effect = False
        negEffects = pokemon2State.negEffects
        for i in range(len(negEffects)):
            if negEffects[i].name == 'dormido':
                do_effect = True
        if do_effect:
            r = random.randint(1, 10)
            if r <= 3:
                pokemon2State.hp = 0
        
        return False
    return True

def curse(move, pokemon1State, pokemon2State, turn):
    if pokemon1State.type == 'ghost':
        condition = ConditionState(name='maldicion', pokemon=pokemon2State.pokemon, turn=turn)
        pokemon2State.negEffects.append(condition)
    else:
        pokemon1State.speed = pokemon1State.speed *0.67
        pokemon1State.attack = pokemon1State.attack * 1.5
        pokemon1State.defense = pokemon1State.defense * 1.5
        return False

def reversal(move, pokemon1State, pokemon2State, turn):
    initial_power = move.power
    perc = pokemon1State.hp / pokemon1State.pokemon.hp

    if perc >= 0.68:
        move.power = 20
    elif perc < 0.68 and perc >= 0.35:
        move.power = 40
    elif perc < 0.35 and perc >= 0.20:
        move.power = 80
    elif perc < 0.20 and perc >= 0.10:
        move.power = 100
    elif perc < 0.10 and perc >= 0.04:
        move.power = 150
    else:
        move.power = 200

    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        move.power = initial_power
        return False
    move.power = initial_power
    return True

def conversion_2(move, pokemon1State, pokemon2State, turn):
    pass

def lowers_pp_target_by_4(move, pokemon1State, pokemon2State, turn):
    pass

def maximiza_atk_paying_half_live(move, pokemon1State, pokemon2State, turn):
    pass

def perc_to_paralyze_100(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        condition = ConditionState(name='paralizado_v', pokemon=pokemon2State.pokemon, turn=turn)
        condition1 = ConditionState(name='paralizado', pokemon=pokemon2State.name, turn=turn)

        pokemon2State.negEffects.append(condition)
        pokemon2State.negEffects.append(condition1)

        return False
    return True

def dead_then_target_dead(move, pokemon1State, pokemon2State, turn):
    condition = ConditionState(name='dead_to_dead', pokemon=pokemon1State.pokemon, turn=turn)
    pokemon1State.negEffects.append(condition)
    return False

def user_and_target_dead_in_3turns(move, pokemon1State, pokemon2State, turn):
    condition_pokemon1 = ConditionState(name='dead_at_3_turns', pokemon=pokemon1State.pokemon)
    condition_pokemon2 = ConditionState(name='dead_at_3_turns', pokemon=pokemon2State.pokemon, turn=turn)

    pokemon1State.negEffects.append(condition_pokemon1)
    pokemon2State.negEffects.append(condition_pokemon2)

    return False

def perc_to_lowers_speed_onestage_100(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        pokemon2State.speed = pokemon2State.speed * 0.5
        return False
    return True

def lowers_target_attack_by_two_stages(move, pokemon1State, pokemon2State, turn):
    pokemon2State.attack = pokemon2State.attack * 0.5
    return False

def can_not_lower_hp_below_1(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 1 if pokemon2State.hp <= 0 else pokemon2State.hp
        return False
    return True

def swagger(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        pokemon2State.attack = pokemon2State.attack * 2
        condition = ConditionState(name='confundido', pokemon=pokemon2State.pokemon, turn=turn)
        pokemon2State.negEffects.append(condition)
    return True

def perc_to_raises_user_defense_10(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State

        r = random.randint(1, 10)
        if r <= 1:
            pokemon1State.defense = pokemon1State.defense * 1.5
        return False
    return True

def enfatuatuion(move, pokemon1State, pokemon2State, turn):
    condition = ConditionState(name='enamorado', pokemon=pokemon2State.pokemon, turn=turn)
    pokemon2State.negEffects.append(condition)
    return False

def sleep_talk(move, pokemon1State, pokemon2State, turn):
    esta_dormido = False
    negEffects = pokemon1State.negEffects
    for i in range(len(negEffects)):
        if negEffects[i].name == 'dormido':
            esta_dormido = True
    
    if esta_dormido:
        pokemon1_moves = pokemon1State.pokemon.learnedMoves
        r = random.randint(1, len(pokemon1_moves))
        while(pokemon1_moves[r].name == 'sleep-talk'):
            r = random.randint(1, len(pokemon1_moves))
        
        return pokemon1_moves[r].DoMove(pokemon1State=pokemon1State, pokemon2State=pokemon2State, turn=turn)
    
    else:
        return True
    
def cures_entire_group_of_major_negEffects(move, pokemon1State, pokemon2State, turn):
    couch = pokemon1State.pokemon.couch

    pokemons_couch = couch.pokemons
    negEffects_to_remove = []
    for i in range(len(pokemons_couch)):
        negEffects = pokemons_couch[i].actualState.negEffects
        for j in negEffects:
            if negEffects[j].name == 'quemado' or negEffects[j].name == 'congelado' or negEffects[j] == 'paralizado' or negEffects[j] == 'dormido' or negEffects[j].name == 'envenenado':
                negEffects_to_remove.append(negEffects[j])

    for i in range(len(negEffects_to_remove)):
        negEffects.remove(negEffects_to_remove[i])

def present(move, pokemon1State, pokemon2State, turn):
    initial_power = move.power
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        r = random.randint(1, 100)
        if r <= 20:
            pokemon2State.hp += pokemon2State.pokemon.hp / 4
            pokemon2State.hp = 0 if pokemon2State.hp >= pokemon2State.pokemon.hp else pokemon2State.hp
            return False
        else:
            if r <= 30 and r > 20:
                move.power = 120
            elif r <= 60 and r > 30:
                move.power = 80
            else:
                move.power = 40

            damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
            pokemon2State.hp -= damage
            pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State

            move.power = initial_power
            return False
    return True

def pain_split(move, pokemon1State, pokemon2State, turn):
    hp_result = (pokemon1State.hp + pokemon2State.hp) / 2
    pokemon1State.hp = hp_result
    pokemon2State.hp = hp_result
    return False

def perc_to_burn_taget_50(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 2)
        if r <= 1:
            condition = ConditionState(name='quemado', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.negEffects.append(condition)

        return False
    return True

def random_power_10_150(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    initial_power = move.power
    r = random.randint(1, 100)
    if r <= accuracy:
        r = random.randint(10, 150)
        move.power = r

        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp  = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        return False
    return True

def perc_to_confuse_target_100(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        condition = ConditionState('confundido', pokemon=pokemon2State.pokemon, turn=turn)
        pokemon2State.negEffects.append(condition)

        return False
    return True

def rapid_spin(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    negEffects = pokemon1State.negEffects
    for i in range(len(negEffects)):
        if negEffects[i].name == '':  # pendiente condicion de espinas
            pass

    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        return False
    return True

def perc_lowers_target_defense_onestage_30(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 3:
            pokemon2State.defense = pokemon2State.defense * 0.67

        return False
    return True

def perc_raise_user_atack_onestage_10(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 1:
            pokemon1State.attack = pokemon1State.attack * 1.5
        
        return False
    return True

def hidden_power(move, pokemon1State, pokemon2State, turn):
    pokemon1 = pokemon1State.pokemon
    i_values = [pokemon1.i_hp, pokemon1.i_attack, pokemon1.i_defense, pokemon1.i_specialAttack, pokemon1.i_specialDefense, pokemon1.speed]
    tipo_index = round((((i_values[0] % 2) + 2*(i_values[1] % 2) + 4*(i_values[2] % 2) + 8*(i_values[3]) + 16*(i_values[4]) + 32*(i_values[5]))/63)*15)
    
    move.type = types_arr[tipo_index]
    initial_power = move.power
    r = random.randint(30, 70)
    move.power = r

    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        return False
    return True

def perc_lowers_target_defense_onestage_20(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 2:
            pokemon2State.defense = pokemon2State.defense * 0.67
        return False
    return True

def copy_targets_stats(move, pokemon1State, pokemon2State, turn):
    pokemon1State.hp = pokemon2State.hp
    pokemon1State.attack = pokemon2State.attack
    pokemon1State.defense = pokemon2State.defense
    pokemon1State.specialAttack = pokemon2State.specialAttack
    pokemon1State.specialDefense = pokemon2State.specialDefense
    pokemon1State.speed = pokemon2State.speed

    return False

def perc_raise_all_stats_10(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 1:
            pokemon1State.attack = pokemon1State.attack * 1.5
            pokemon1State.defense = pokemon1State.defense * 1.5
            pokemon1State.specialAttack = pokemon1State.specialAttack * 1.5
            pokemon1State.specialDefense = pokemon1State.specialDefense * 1.5
            pokemon1State.speed = pokemon1State.speed * 1.5

        return False
    return True

def perc_lower_specialDefense_onestage_20(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 2:
            pokemon2State.specialDefense = pokemon2State.specialDefense * 0.67
        
        return False
    return True

def perc_to_lowers_target_defense_onestage_50(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 2)
        if r <= 1:
            pokemon2State.defense = pokemon2State.defense * 0.67
        return False
    return True

def whirlpool(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1,100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        r = random.randint(2,5)
        condition = ConditionState(name='trap_t', pokemon=pokemon2State.pokemon, turn=turn, turnsDuration=r)
        condition1 = ConditionState(name='trap', pokemon=pokemon2State.pokemon, turn=turn)

        pokemon2State.negEffects.append(condition)
        pokemon2State.negEffects.append(condition1)

        return False
    return True

def beat_up(move, pokemon1State, pokemon2State, turn):
    couch = pokemon1State.pokemon.couch
    pokemons = couch.pokemons
    move_ = Move(name='beat_up', power=10, pp=1, accuracy=100, type='dark', category='physical', ailment='none', target='selected-pokemon', effects=[normal_attack])
    for i in range(len(pokemons)):
        pokemon = pokemons[i]
        negEffects = pokemon.actualState.negEffects
        puede_atacar = True
        for i in range(len(negEffects)):
            if negEffects[i].name == 'paralizado' or negEffects[i].name == 'envenenado' or negEffects[i].name == 'quemado' or negEffects[i].name == 'congelado' or negEffects[i].name == 'dormido' or negEffects[i].name == 'gravemente envenenado':
                puede_atacar = False
        if puede_atacar:
            accuracy = move_.accuracy
            r = random.randint(1, 100)
            if r <= accuracy:
                damage = GetDamage(move=move_, attacker_pokemon_state=pokemon.actualState, attacked_pokemon_state=pokemon2State)
                pokemon2State.hp -= damage
                pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

    return False  # por revisar

def fake_out(move, pokemon1State, pokemon2State, turn):
    if True:
        return normal_attack(move, pokemon1State, pokemon2State, turn)
    else:
        return True
    
def raises_specialAtck_confuses_target(move, pokemon1State, pokemon2State, turn):
    pokemon2State.specialAttack = pokemon2State.specialAttack * 1.5
    condition = ConditionState(name='confundido', pokemon=pokemon2State.pokemon, turn=turn)
    pokemon2State.negEffects.append(condition)

    return False

def burn_target(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        condition = ConditionState(name='quemado', pokemon=pokemon2State.pokemon, turn=turn)
        pokemon2State.negEffects.append(condition)
        return False
    return True

def lowers_specialAttack_twostages(move, pokemon1State, pokemon2State, turn):
    pokemon2State.specialAttack = pokemon2State.specialAttack * 0.5
    return False

def memento(move, pokemon1State, pokemon2State, turn):
    lowers_specialAttack_twostages(move, pokemon1State, pokemon2State, turn)
    lowers_target_attack_by_two_stages(move, pokemon1State, pokemon2State, turn)
    pokemon1State.hp = 0

    return False

def facade(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        negEffects = pokemon2State.negEffects
        for i in range(len(negEffects)):
            if negEffects[i].name == 'paralizado' or negEffects[i].name == 'quemado' or negEffects[i].name == 'envenenado':
                damage = 2 * damage
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        return False

    return True

def smellings_salts(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage_increment = False
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        negEffects = pokemon2State.negEffects
        for i in range(len(negEffects) -1, -1, -1):
            if negEffects[i].name == 'paralizado' or negEffects[i].name == 'paralizado_v':
                damage_increment = True
                negEffects.remove(negEffects[i])
        if damage_increment:
            damage = 2 * damage                

        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp
        
        return False
    return True

def taunt_(move, pokemon1State, pokemon2State, turn):
    condition1 = ConditionState(name='taunt', pokemon=pokemon2State.pokemon, turn=turn)
    condition2 = ConditionState(name='taunt_v', pokemon=pokemon2State.pokemon, turn=turn, turnsDuration=3)

    pokemon2State.negEffects.append(condition1)
    pokemon2State.negEffects.append(condition2)

    return False

def swap_items(move, pokemon1State, pokemon2State, turn):
    pokemon1_items = pokemon1State.pokemon.inventory   # suponiendo que solo se puede tener un objeto en el inventario
    pokemon2_items = pokemon2State.pokemon.inventory

    if len(pokemon1_items) == 0 and len(pokemon2_items) == 0:
        return 
    
    elif len(pokemon1_items) != 0 and len(pokemon2_items) == 0:
        pokemon2_items.append(pokemon1_items[0])
        pokemon1_items.remove(pokemon1_items[0])

        return
    elif len(pokemon1_items) == 0 and len(pokemon2_items) != 0:
        pokemon1_items.append(pokemon2_items[0])
        pokemon2_items.remove(pokemon2_items[0])
    else:
        item1 = pokemon1_items[0]
        pokemon1_items.remove(pokemon1_items[0])
        pokemon1_items.append(pokemon2_items[0])

        pokemon2_items.remove(pokemon2_items[0])
        pokemon2_items.append(item1)

        return
    
def random_trained_pok_moves(move, pokemon1State, pokemon2State, turn):
    pokemons = pokemon1State.pokemon.couch.pokemons

    moves = []

    for i in range(len(pokemons)):
        if pokemons[i].name == pokemon1State.pokemon.name:
            continue
        else:
            learned_moves = pokemons[i].learnedMoves
            for j in range(len(learned_moves)):
                moves.append(learned_moves[j])
    
    r = random.randint(0, len(moves))
    move_ = moves[r]

    return move_.DoMove(pokemon1State, pokemon2State, turn)
        
def ingrain(move, pokemon1State, pokemon2State, turn):
    condition1 = ConditionState(name='dont_leave_battle', pokemon=pokemon2State.pokemon, turn=turn)
    condition2 = ConditionState(name='trap', pokemon=pokemon2State.pokemon, turn=turn)

    pokemon2State.negEffects.append(condition1)
    pokemon2State.negEffects.append(condition2)

    return False

def superpower(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(0, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        pokemon1State.attack = pokemon1State.attack * 0.67
        pokemon1State.defense = pokemon1State.defense * 0.67

        return False
    return True

def yawn(move, pokemon1State, pokemon2State, turn):
    condition = ConditionState(name='sleep_end_off_nextTurn', pokemon=pokemon2State.pokemon, turn=turn, turnsDuration=1)
    pokemon2State.negEffects.append(condition)
    return False

def lowers_hp_equal_user_is(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(0, 100)
    if r <= accuracy:
        pokemon2State.hp = pokemon1State.hp if pokemon2State.hp >= pokemon1State.hp else pokemon2State.hp

        return False
    return True

def eruption(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        actual_hp = pokemon2State.hp
        total_hp = pokemon2State.pokemon.hp
        
        initial_power = move.power
        move.power = 150 * (actual_hp/total_hp)
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        move.power = initial_power

        return False
    return True

def clear_user_burn_paralysis_poison(move, pokemon1State, pokemon2State, turn):
    negEffects = pokemon1State.negEffects

    for i in range(len(negEffects)-1, -1, -1):
        if negEffects[i].name == 'quemado' or negEffects[i].name == 'paralizado' or negEffects[i].name == 'paralizado_v' or negEffects[i].name == 'envenenado':
            negEffects.remove(negEffects[i])

    return False

def raises_user_specialAttack_threestages(move, pokemon1State, pokemon2State, turn):
    pokemon1State.specialAttack = pokemon1State.specialAttack * 2.5
    return False

def luster_purge(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 2)
        if r <= 1:
            pokemon2State.specialDefense = pokemon2State.specialDefense * 0.67

        return False
    return True

def mist_ball(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 2)
        if r <= 1:
            pokemon2State.specialAttack = pokemon2State.specialAttack * 0.67

        return False
    return True

def blaze_kick(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        critical_prob = 8
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State, critical_prob=critical_prob)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 1:
            condition = ConditionState(name='quemado', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.negEffects.append(condition)
        
        return False
    return True

def perc_badly_poison_50(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State.hp

        r = random.randint(1, 2)
        if r <= 1:
            condition = ConditionState(name='gravemente_envenenado', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.negEffects.append(condition)
        return False
    return True

def perc_raise_user_attack_onestage_20(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 2:
            pokemon1State.attack = pokemon1State.attack * 1.5
        return False
    return True

def lower_target_specialDefense_twostages(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        pokemon2State.specialDefense = pokemon2State.specialDefense * 0.5
        return False
    return True

def lower_user_specialAttack_twostages_after_damage(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State.hp

        pokemon1State.specialAttack = pokemon1State.specialAttack * 0.5

        return False
    return True

def poison_tail(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        critical_prob = 8
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State, critical_prob=critical_prob)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        r = random.randint(1, 10)
        if r <= 1:
            condition = ConditionState(name='envenenado', pokemon=pokemon2State.pokemon, turn=turn)

def volt_tackle(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State <= 0 else pokemon2State.hp

        pokemon1State.hp -= damage/3
        pokemon1State.hp = 0 if pokemon1State.hp <= 0 else pokemon1State.hp

        r = random.randint(1, 10)
        if r <= 1:
            condition1 = ConditionState(name='paralizado_v', pokemon=pokemon2State.pokemon, turn=turn)
            condition2 = ConditionState(name='paralizado', pokemon=pokemon2State.pokemon, turn=turn)
            pokemon2State.negEffects.append(condition1)
            pokemon2State.negEffects.append(condition2)
        
        return False
    return True

def raise_speed_onestage(move, pokemon1State, pokemon2State, turn):
    pokemon1State.speed = pokemon1State.speed * 1.5
    return False

def fly(move, pokemon1State, pokemon2State, turn):
    condition = ConditionState(name='volar_v', pokemon=pokemon1State.pokemon, turn=turn, turnsDuration=1, pokemon2=pokemon2State.pokemon)
    condition1 = ConditionState(name='inmune_fisico', pokemon=pokemon1State.pokemon, turn=turn)
    condition2 = ConditionState(name='carga', pokemon=pokemon1State.pokemon, turn=turn)
    pokemon1State.posEffects.append(condition)
    pokemon1State.posEffects.append(condition1)
    pokemon1State.posEffects.append(condition2)

    return False

def prevent_fleeing_and_inflicts_damage(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        condition1 = ConditionState(name='trap', pokemon=pokemon2State.pokemon, turn=turn, turnsDuration=random.randint(2, 5))
        condition2 = ConditionState(name='trap_v', pokemon=pokemon2State.pokemon, turn=turn)

        pokemon2State.negEffects.append(condition1)
        pokemon2State.negEffects.append(condition2)

        return False
    return True

def cargar_oneTurn(move, pokemon1State, pokemon2State, turn):
    condition = ConditionState(name='carga', pokemon=pokemon1State.pokemon, turn=turn)
    condition1 = ConditionState(name='carga_v', pokemon=pokemon1State.pokemon, turn=turn, turnsDuration=1)
    pokemon1State.posEffects.append(condition)
    pokemon1State.posEffects.append(condition1)

    pokemon1State.effMovCargado = normal_attack
    pokemon1State.effMovCargadoParams = (move, pokemon1State, pokemon2State, turn)

    return False

def keep_attacking_2_3_turns(move, pokemon1State, pokemon2State, turn):
    condition = ConditionState(name='keep_attacking', pokemon=pokemon1State.pokemon, turn=turn, turnsDuration=random.randint(2,3))
    pokemon1State.posEffects.append(condition)

    pokemon1State.effMovCargado = normal_attack
    pokemon1State.effMovCargadoParams = (move, pokemon1State, pokemon2State, turn)

def confuses_user(move, pokemon1State, pokemon2State, turn):
    accuracy = move.accuracy
    r = random.randint(1, 100)
    if r <= accuracy:
        damage = GetDamage(move=move, attacker_pokemon_state=pokemon1State, attacked_pokemon_state=pokemon2State)
        pokemon2State.hp -= damage
        pokemon2State.hp = 0 if pokemon2State.hp <= 0 else pokemon2State.hp

        condition = ConditionState(name='confuso')
        pokemon1State.negEffects.append(condition)

        return False
    return True

def disable_move_1_8_turns(move, pokemon1State, pokemon2State, turn):
    moves = pokemon2State.pokemon.learnedMoves
    r = random.randint(0, len(moves) - 1)

    moves[r].is_eneabled = False
    r = random.randint(1, 8)

    condition = ConditionState(name='deshabilita_mov_v', pokemon=pokemon2State.pokemon, turn=turn, turnsDuration=r)

    return False






move_effects = {
    'Inflicts regular damage with no additional effect.':[normal_attack],
    'Has an increased chance for a critical hit.':[increase_critical_chance],
    'Hits 2-5 times in one turn.':[hits_2_5_times],
    "Scatters money on the ground worth five times the user's level.":[normal_attack],
    "Has a 10_ chance to burn the target.":[perc_to_burn_10],
    "Has a 10_ chance to freeze the target.":[perc_to_freeze_10],
    "Has a 10_ chance to paralyze the target.":[perc_to_paralyze_10],
    "Causes a one-hit KO.":[one_hit_ko],
    "Requires a turn to charge before attacking.":[cargar_oneTurn],   
    "Raises the user's Attack by two stages.":[raises_atk_2_stages],
    "Inflicts regular damage and can hit Pokémon in the air.":[normal_attack],
    "Immediately ends wild battles.  Forces trainers to switch Pokémon.":[],    # agregar efecto negativo extra que sea forzar el cambio de pokemon
    "User flies high into the air, dodging all attacks, and hits next turn.":[fly],
    "Prevents the target from fleeing and inflicts damage for 2-5 turns.":[prevent_fleeing_and_inflicts_damage],
    "Has a 30_ chance to make the target flinch.":[has_30_perc_to_make_flinch],
    "Hits twice in one turn.":[normal_attack, normal_attack],
    "If the user misses, it takes half the damage it would have inflicted in recoil.":[miss_then_take_halfdamage],
    "Lowers the target's accuracy by one stage.":[],  # pendiente
    "Has a 30_ chance to paralyze the target.":[percent_to_paralize_30],
    "User receives 1/4 the damage it inflicts in recoil.":[recoil_un_cuarto],
    "Hits every turn for 2-3 turns, then confuses the user.":[confuses_user],
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
    "Hits three times, increasing power by 100_ with each successful hit.":[triple_kick],
    "Takes the target's item.":[normal_attack], # pendiente lo de robar el objeto del pokemon contrario
    "Prevents the target from leaving battle.":[prevents_leave_to_battle],
    "Ensures that the user's next move will hit the target.":[],   # pendiente efecto positivo
    "Target loses 1/4 its max HP every turn as long as it's asleep.":[nightmare],
    "Has a 10_ chance to burn the target.  Lets frozen Pokémon thaw themselves.":[perc_to_burn_10],  # pendiente lo de descongelarse
    "Has a 30_ chance to make the target flinch.  Only works if the user is sleeping.":[perc_to_flinch_30_if_is_sleeped],
    "Ghosts pay half their max HP to hurt the target every turn.  Others decrease Speed but raise Attack and Defense.":[curse],
    "Inflicts more damage when the user has less HP remaining, with a maximum of 200 power.":[reversal],
    "Changes the user's type to a random type either resistant or immune to the last move used against it.":[],  # pendiente registro de movimientos
    "Lowers the PP of the target's last used move by 4.":[],   # pendiente registro de movimientos
    "Prevents any moves from hitting the user this turn.":[],  # pendiente efectos positivos
    "User pays half its max HP to max out its Attack.":[],   # pendiente efectos positivos
    "Has a 100_ chance to lower the target's accuracy by one stage.":[], # pendiente bajar punteria de los pokemones
    "Has a 50_ chance to lower the target's accuracy by one stage.":[], # pendiente bajar punteria de los pokemones
    "Scatters Spikes, hurting opposing Pokémon that switch in.":[],   # pendiente
    "Has a 100_ chance to paralyze the target.":[perc_to_paralyze_100], 
    "Forces the target to have no Evade, and allows it to be hit by Normal and Fighting moves even if it's a Ghost.":[],   # mucho texto
    "If the user faints this turn, the target automatically will, too.":[dead_then_target_dead],
    "User and target both faint after three turns.":[user_and_target_dead_in_3turns],
    "Has a 100_ chance to lower the target's Speed by one stage.":[perc_to_lowers_speed_onestage_100],
    "Changes the weather to a sandstorm for five turns.":[],  # mucho texto
    "Prevents the user's HP from lowering below 1 this turn.":[], # pendiente efectos positivos
    "Lowers the target's Attack by two stages.":[lowers_target_attack_by_two_stages],
    "Power doubles every turn this move is used in succession after the first, resetting after five turns.":[],  # pendiente  registro de movimientos
    "Cannot lower the target's HP below 1.":[can_not_lower_hp_below_1],
    "Raises the target's Attack by two stages and confuses the target.":[swagger],
    "Power doubles every turn this move is used in succession after the first, maxing out after five turns.":[], # pendiente registro de movimientos
    "Has a 10_ chance to raise the user's Defense by one stage.":[perc_to_raises_user_defense_10],
    "Target falls in love if it has the opposite gender, and has a 50_ chance to refuse attacking the user.":[enfatuatuion],
    "Randomly uses one of the user's other three moves.  Only works if the user is sleeping.":[sleep_talk],
    "Cures the entire party of major status effects.":[cures_entire_group_of_major_negEffects],
    "Power increases with happiness, up to a maximum of 102.":[],  # por implementar felicdad
    "Randomly inflicts damage with power from 40 to 120 or heals the target for 1/4 its max HP.":[present],
    "Power increases as happiness decreases, up to a maximum of 102.":[],   # por implementar felicidad
    "Protects the user's field from major status ailments and confusion for five turns.":[], # por implementar efectos positivos
    "Sets the user's and targets's HP to the average of their current HP.":[pain_split],
    "Has a 50_ chance to burn the target.  Lets frozen Pokémon thaw themselves.":[perc_to_burn_taget_50],  # pendiente efecto de descongelacion
    "Power varies randomly from 10 to 150.":[random_power_10_150],
    "Has a 100_ chance to confuse the target.":[perc_to_confuse_target_100],
    "Allows the trainer to switch out the user and pass effects along to its replacement.":[], # despues
    "Forces the target to repeat its last used move every turn for 2 to 6 turns.":[],  # pendiente registro de movimientos
    "Has double power against, and can hit, Pokémon attempting to switch out.":[normal_attack],
    "Frees the user from binding moves, removes Leech Seed, and blows away Spikes.":[rapid_spin],
    "Lowers the target's evasion by one stage.":[],  # pendiente evasion de pokemones
    "Has a 30_ chance to lower the target's Defense by one stage.":[perc_lowers_target_defense_onestage_30],
    "Has a 10_ chance to raise the user's Attack by one stage.":[perc_raise_user_atack_onestage_10],
    "Heals the user by half its max HP.  Affected by weather.":[heals_halfHpMax],
    "Power and type depend upon user's IVs.  Power can range from 30 to 70.":[hidden_power],
    "Changes the weather to rain for five turns.":[],   # clima mucho texto
    "Changes the weather to sunny for five turns.":[],  # clima kucho texto
    "Has a 20_ chance to lower the target's Defense by one stage.":[perc_lowers_target_defense_onestage_20],
    "Inflicts twice the damage the user received from the last special hit it took.":[],  # pendiente registro de movimientos
    "Discards the user's stat changes and copies the target's.":[copy_targets_stats],
    "Has a 10_ chance to raise all of the user's stats by one stage.":[perc_raise_all_stats_10],
    "Has a 20_ chance to lower the target's Special Defense by one stage.":[perc_lower_specialDefense_onestage_20],
    "Hits the target two turns later.":[], # pendiente efectos positivos
    "Has a 50_ chance to lower the target's Defense by one stage.":[perc_to_lowers_target_defense_onestage_50],
    "Prevents the target from leaving battle and inflicts 1/16 its max HP in damage for 2-5 turns.":[],
    "Hits once for every conscious Pokémon the trainer has.":[beat_up],
    "Can only be used as the first move after the user enters battle.  Causes the target to flinch.":[fake_out],
    "Forced to use this move for several turns.  Pokémon cannot fall asleep in that time.":[],   # pediente efectos positivos
    "Stores energy up to three times for use with Spit Up and Swallow.":[],   # pendiente estados positivos(colocar cargas)
    "Power is 100 times the amount of energy Stockpiled.":[],  # pendiente efectos positivos(depende de las cargas de arriba)
    "Recovers 1/4 HP after one Stockpile, 1/2 HP after two Stockpiles, or full HP after three Stockpiles.":[],  # al igual que el de arriba depende del efecto positivo
    "Changes the weather to a hailstorm for five turns.":[],   # clima
    "Prevents the target from using the same move twice in a row.":[],  # pendiente registro de movimientos
    "Raises the target's Special Attack by one stage and confuses the target.":[raises_specialAtck_confuses_target],
    "Burns the target.":[burn_target],
    "Lowers the target's Attack and Special Attack by two stages.  User faints.":[lowers_target_attack_by_two_stages, lowers_specialAttack_twostages],
    "Power doubles if user is burned, paralyzed, or poisoned.":[facade],
    "If the user takes damage before attacking, the attack is canceled.":[], # pendiente registro de movimientos
    "If the target is paralyzed, inflicts double damage and cures the paralysis.":[smellings_salts],
    "Redirects the target's single-target effects to the user for this turn.":[], # pendiente batalla en equipo
    "Uses a move which depends upon the terrain.":[], # terrenos pendiente
    "Raises the user's Special Defense by one stage.  User's Electric moves have doubled power next turn.":[raise_specialDfs_onestage, ],  # pendiente efecto positivo
    "For the next few turns, the target can only use damaging moves.":[taunt_], 
    "Ally's next move inflicts half more damage.":[], # combates en equipo, por ahora no
    "User and target swap items.":[swap_items],
    "Copies the target's ability.":[],  # no hay habilidades
    "User will recover half its max HP at the end of the next turn.":[], # pendiente efectos positivos
    "Randomly selects and uses one of the trainer's other Pokémon's moves.":[random_trained_pok_moves],
    "Prevents the user from leaving battle.  User regains 1/16 of its max HP every turn.":[ingrain],
    "Lowers the user's Attack and Defense by one stage after inflicting damage.":[superpower],
    "Reflects back the first effect move used on the user this turn.":[], # pendiente
    "User recovers the item it last used up.":[], # pendiente registro de moviminetos
    "Inflicts double damage if the user takes damage before attacking this turn.":[], # pendiente registro de movimientos 
    "Destroys Reflect and Light Screen.":[], # pendiente efectos positivos
    "Target sleeps at the end of the next turn.":[yawn], 
    "Target drops its held item.":[],  # en la primera generación los pokemones no sostienen items
    "Lowers the target's HP to equal the user's.":[lowers_hp_equal_user_is],
    "Inflicts more damage when the user has more HP remaining, with a maximum of 150 power.":[eruption],
    "User and target swap abilities.":[], # no hay habilidades en primera generacion
    "Prevents the target from using any moves that the user also knows.":[], # pendiente despues
    "Cleanses the user of a burn, paralysis, or poison.":[clear_user_burn_paralysis_poison],
    "If the user faints this turn, the PP of the move that fainted it drops to 0.":[], # pendiente registro de movimientos
    "Steals the target's move, if it's self-targeted.":[],  # pendiente estados positivos
    "Has a 30_ chance to inflict a status effect which depends upon the terrain.":[], # terreno
    "User dives underwater, dodging all attacks, and hits next turn.":[],  # pendiente estados positivos
    "User's type changes to match the terrain.":[], # terreno 
    "Raises the user's Special Attack by three stages.":[raises_user_specialAttack_threestages],
    "Has a 50_ chance to lower the target's Special Defense by one stage.":[luster_purge],
    "Has a 50_ chance to lower the target's Special Attack by one stage.":[],
    "Has an increased chance for a critical hit and a 10_ chance to burn the target.":[blaze_kick],
    "Halves all Electric-type damage.":[], # pendiente estados positivos
    "Has a 50_ chance to badly poison the target.":[perc_badly_poison_50],
    "Has a 20_ chance to raise the user's Attack by one stage.":[perc_raise_user_attack_onestage_20],
    "If there be weather, this move has doubled power and the weather's type.":[], # clima no
    "Lowers the target's Special Defense by two stages.":[lower_target_specialDefense_twostages],
    "Lowers the user's Special Attack by two stages after inflicting damage.":[lower_user_specialAttack_twostages_after_damage],
    "Lowers the target's Attack and Defense by one stage.":[lowers_target_defense_onestage, lowers_atk_onestage],
    "Raises the user's Defense and Special Defense by one stage.":[raise_dfs_onestage, raise_specialDfs_onestage],
    "Inflicts regular damage and can hit Bounce and Fly users.":[normal_attack],
    "Has a 30_ chance to lower the target's accuracy by one stage.":[], # accuracy de pokemon pendiente
    "Raises the user's Attack and Defense by one stage.":[raise_atk_onestage, raises_defense_onestage],
    "User bounces high into the air, dodging all attacks, and hits next turn.":[],  # efectos positivos pendiente
    "Has an increased chance for a critical hit and a 10_ chance to poison the target.":[poison_tail],
    "User takes 1/3 the damage inflicted in recoil.  Has a 10_ chance to paralyze the target.":[volt_tackle],
    "Halves all Fire-type damage.":[], # efectos positivos pendiente
    "Raises the user's Special Attack and Special Defense by one stage.":[raise_specialAtk_onestage, raise_specialDfs_onestage],
    "Raises the user's Attack and Speed by one stage.":[raise_atk_onestage, raise_speed_onestage],
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