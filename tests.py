from bd.pokemon import *
from bd import fill_bd as fill

#----------------------------------------BD TESTS----------------------------------------

# pokemon = 'pichu'
# fill.get_all_pokemons()
# fill.get_evolutions()
# for evol_chain in all_evol.get_all_evolutions():
#     if pokemon in evol_chain.get_pokes():
#         print(evol_chain.get_by_name(pokemon).species)
#         break
# all_pokes.get_by_name('pichu').id

fill.get_all_pokemons(151)
fill.get_evolutions()
fill.get_all_items()

fill.fill_pokemons()
fill.fill_evolutions()
fill.fill_pokemon_evolutions()

#----------------------------------------MAPA TESTS----------------------------------------

from mapa.create_map import *
