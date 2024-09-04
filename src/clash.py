from Entrenador import *
from utils import *

class Clash():
    def __init__(self, couch1:Couch, couch2:Couch):
        self.couch1 = couch1
        self.pokemonStateCouch1 = couch1.pokemonLider.actualState

        self.couch2 = couch2
        self.pokemonSateCouch2 = couch2.pokemonLider.actualState

    # la idea del combate es la siguiente: paso 1 verificar los efectos negativos de ambos pokemones, los efectos que 
    # pertenecen a la clase de verificar si salen de ese estado negativo, como por ejemplo congelación o parálisis, 
    # luego se le pide a los entrenadores que proporcionen un movimiento, luego se ve la prioridad de movimiento que 
    # radica en la matriz de prioridad de movimiento y en la velocidad de los pokemones, luego se verifican los efectos 
    # negativos que pueden afectar la ejecución de movimientos como parálisis, luego se procede a calcular el daño, 
    # luego se verifica hay ko por parte de los pokemones, luego se repite el proceso hasta que el entrenador no tenga
    # más pokemones que proporcionar



    def DoClach(self):
        couch1_pokemon = self.couch1.pokemonLider    # se declaran los pokemones que van a dar la cara en el combate
        couch2_pokemon = self.couch2.pokemonLider
        turn = 1    # se declara el turno inicial

        register_moves = []      # aquí se almacenarán los movimientos

        while(not self.VerifyEndToClash()):  # mientras ambos entrenadores puedan seguir combatiendo

            # se verifican los efectos que pueden hacer salir a los pokemones de los estados negativos

            pokemon1_negEffects = self.couch1.pokemonLider.actualState.negEffects   # 

            for i in range(len(pokemon1_negEffects)):
                negEffect1:ConditionState = pokemon1_negEffects[i]
                if globals()[negEffect1.name] in verificar_salida_del_estado:
                    negEffect1.ActivateEffect(turn=turn, pokemon1=self.couch1.pokemonLider)

            pokemon2_negEffect = self.couch2.pokemonLider.actualState.negEffects

            for i in range(len(pokemon2_negEffect)):
                negEffect2:ConditionState = pokemon2_negEffect[i]
                if globals()[negEffect1.name] in verificar_salida_del_estado:
                    negEffect1.ActivateEffect(turn=turn, pokemon1=self.couch2.pokemonLider)

            # fin de verificación de liberación de estados negativos #

            # selección de movimientos por parte de los entrenadores

            couch1_move:Move = self.couch1.GetMove_at_Battle(self.couch1.pokemonLider.actualState, self.couch2.pokemonLider.actualState)
            couch2_move:Move = self.couch2.GetMove_at_Battle(self.couch2.pokemonLider.actualState, self.couch1.pokemonLider.actualState)

            # fin de la selección de movimientos por parte de los entrenadores #


            # selección de cual movimiento se ejecuta primero y ejecución de dicho movimiento

            try:
                couch1_move_speed = prioridad_de_acciones[couch1_move.name]
            except:
                couch1_move_speed = 0
            
            try:
                couch2_move_speed = prioridad_de_acciones[couch2_move.name]
            except:
                couch2_move_speed = 0

            if couch1_move_speed > couch2_move_speed:     # guardamos la info de la manera turn_(turn, couch, pokemonLider_couch_actualState)
                turn1 = turn, couch1_move, self.couch1.pokemonLider.actualState
                turn2 = turn, couch2_move, self.couch2.pokemonLider.actualState
            elif couch1_move_speed < couch2_move_speed:
                turn1 = turn, couch2_move, self.couch2.pokemonLider.actualState
                turn2 = turn, couch1_move, self.couch1.pokemonLider.actualState
            elif self.couch1.pokemonLider.actualState.speed >= self.couch2.pokemonLider.actualState.speed:  # si tienen la misma prioridad entonces se comparan las velocidades de cada pokemon
                turn1 = turn, couch1_move, self.couch1.pokemonLider.actualState
                turn2 = turn, couch2_move, self.couch2.pokemonLider.actualState
            else:
                turn1 = turn, couch2_move, self.couch2.pokemonLider.actualState
                turn2 = turn, couch1_move, self.couch1.pokemonLider.actualState
                # se tienen los movimientos almacenados en turn1 y turn2 respectivamente

            # fin de la selección de cuál movimiento se ejecuta primero y ejecución de dicho movimiento #


            # ejecución de los movimientos basándose en si tienen efectos negativos que afecten en la determinación del movimiento o no

            negEffect1:ConditionState = pokemon1_negEffects
            if globals()[negEffect1.name] in afectan_ejecucion_de_movimiento:  
                if not negEffect1.ActivateEffect(turn=turn, pokemon1=turn1[2]):

                    pass  # pendiente de ejecutar el movimiento con su respectivo efecto 
            
            negEffect2:ConditionState = pokemon2_negEffect
            if globals()[negEffect2.name] in afectan_ejecucion_de_movimiento:
                if not negEffect2.ActivateEffect(turn=turn, pokemon1=turn2[2]):

                    pass  # al igual que el de arriba pendiente

            # fin de la ejecución de movimientos #
                       



    # verifica si alguno de los dos entrenadores no le quedan pokemones para seguir el combate
    def VerifyEndToClash(self):
        couch1_end = 1   # 0 si el equipo del couch1 puede continuar, 1 si el equipo del couch1 está desmayado

        couch1_deck = self.couch1.deck
        for i in range(len(couch1_deck)):
            pokemon = couch1_deck[i]
            if pokemon.actualState.hp > 0:   # cada pokemon tiene la característica actualState que le da su situación actual 
                couch1_end = 0
                break
        
        if couch1_end == 0:
            couch2_deck = self.couch2.deck

            for i in range(len(couch2_deck)):
                pokemon = couch2_deck[i]
                if pokemon.actualState.hp > 0:
                    return True
            
            return False
        else:
            return False