# import sqlite3
import bd.read_bd as read_bd

# conn = sqlite3.connect('pokedex.db')
# cursor = conn.cursor()


class Move():
    def __init__(self, name:str, power:int, pp:int, accuracy:int, type:str, category:str,
                 ailment:str, target:str, effects):  # el efect esta en veremos de que tipo va a ser
        
        self.name = name
        self.power = power
        self.critical_prob = 24    # en rojo fuego la probabilidad de critico es de 1 en 24, en el metodo GetDamage() se hacer random.randint(1, critical_prob)
        self.pp = pp
        self.accuracy = accuracy
        self.type = type
        self.category = category
        self.ailment = ailment
        self.target = target
        self.effects = effects
        self.isEneabled = True

    def DoMove(self, pokemon1State, pokemon2State, turn):
        effects = self.effects
        miss = False
        for i in range(len(effects)):
            effect = effects[i]

            if(effect(self, pokemon1State, pokemon2State, turn)):
                miss = True
        return miss


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
    


def AsignMoves(pokemon):
    result = [0, 0, 0, 0]

    pokemon_id = pokemon.id
    pokemon_lvl = pokemon.lvl

    # cursor.execute(f'SELECT pokemon_id, move_id, learned_at_level FROM Pokemon_Moves WHERE pokemon_id = {pokemon_id}')
    # pokemon_moves = cursor.fetchall()
    pokemon_moves = read_bd.get_pokemon_move_at_lvl(pokemon_id)

    pokemon_moves_at_lvl = []

    for i in range(len(pokemon_moves)):
        if pokemon_moves[i][2] == 0 or pokemon_moves[i][2] > pokemon_lvl:
            continue
        else:
            pokemon_moves_at_lvl.append(pokemon_moves[i])

    # ordenamos en orden ascendente según el lvl y nos quedamos con los 4 últimos
    pokemon_moves_at_lvl = OrderByLearnedAtLvl(pokemon_moves_at_lvl)
    

    for i in range(len(pokemon_moves_at_lvl)):
        pokemon_move = pokemon_moves_at_lvl[i]
        pokemon_move_id = pokemon_move[1]

        m = read_bd.get_move(pokemon_move_id)
        # cursor.execute(f'SELECT * FROM Moves WHERE id = {pokemon_move_id}')
        # m = cursor.fetchall()[0]

        move = Move(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8]) # move(id, name, power, pp, accuracy, type_id, category, ailment, target, effect)
        result[i] = move
    
    return result

