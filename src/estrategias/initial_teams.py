from pokedex import Pokedex
import random

pokedex = Pokedex()

def random_team():
    '''
    Selecciona un equipo de 6 pokemones aleatorios de la pokedex.
    
    Returns:
    list: Lista de 6 pokemones.
    '''
    team = []
    for i in range(6):
        team.append(random.choice(pokedex.pokemones))
    return team