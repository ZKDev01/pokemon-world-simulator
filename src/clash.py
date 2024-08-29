from Entrenador import *

class Clash():
    def __init__(self, couch1:Couch, couch2:Couch):
        self.couch1 = couch1
        self.pokemonStateCouch1 = couch1.pokemonLider.actualState

        self.couch2 = couch2
        self.pokemonSateCouch2 = couch2.pokemonLider.actualState

    # pendiente

    def DoClach(self):
        couch1_pokemon = self.couch1.pokemonLider
        couch2_pokemon = self.couch2.pokemonLider
        turn = 1

        register_moves = []

        while(not self.VerifyEndToClash()):  # mientras ambos entrenadores puedan seguir combatiendo

            # hacer cumplir los efectos negativos (pendiente)

            if couch1_pokemon.actualState.speed > couch2_pokemon.actualState.speed:
                couch1_turn = self.couch1
                couch2_turn = self.couch2
            else:
                couch1_turn = self.couch2
                couch2_turn = self.couch1
            
            couch1_move:Move = couch1_turn.GetMove_at_Battle(couch1_turn.pokemonLider.actualState, couch2_turn.pokemonLider.actualState)
            register_moves.append(couch1_move)

            couch2_move:Move = couch2_turn.GetMove_at_Battle(couch2_turn.pokemonLider.actualState, couch1_turn.pokemonLider.actualState)
            register_moves.append(couch2_move)

                       



    # verifica si alguno de los dos entrenadores no le quedan pokemones para seguir el combate
    def VerifyEndToClash(self):
        couch1_end = 1   # 0 si el equipo del couch1 puede continuar, 1 si el equipo del couch1 esta desmayado

        couch1_deck = self.couch1.deck
        for i in range(len(couch1_deck)):
            pokemon = couch1_deck[i]
            if pokemon.actualState.hp > 0:   # cada pokemon tiene la caracteristica actualState que le da su situacion actual 
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