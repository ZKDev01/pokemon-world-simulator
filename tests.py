from bd.pokemon import *
from bd import fill_bd as fill
from src.pokedex import Pokedex

#----------------------------------------BD TESTS----------------------------------------

# pokemon = 'pichu'
# fill.get_all_pokemons()
# fill.get_evolutions()
# for evol_chain in all_evol.get_all_evolutions():
#     if pokemon in evol_chain.get_pokes():
#         print(evol_chain.get_by_name(pokemon).species)
#         break
# all_pokes.get_by_name('pichu').id

# fill.get_all_pokemons(151)
# fill.get_evolutions()
# fill.get_all_items()

# fill.fill_pokemons()
# fill.fill_evolutions()
# fill.fill_pokemon_evolutions()

#----------------------------------------MAPA TESTS----------------------------------------

# from mapa.create_map import *

# # build_random_map()

# map = build_kanto_map()
# # print(map)
# # print(map.get_next_locations('mt-moon'))
# areas = map.get_areas('mt-moon')
# print(areas)
# print(areas[0].get_pokemons())
# print(areas[0].get_ecosystems())

#----------------------------------------POKEDEX TESTS----------------------------------------
pokedex_user = Pokedex()
pichu = pokedex_user.get_pokemon('pichu')
print(pichu.evolves_to)
pikachu = pokedex_user.get_pokemon('pikachu')
print(pikachu.evolves_from)

eevee = pokedex_user.get_pokemon('eevee')
print(eevee.evolves_to)
vaporeon = pokedex_user.get_pokemon('vaporeon')
print(vaporeon.evolves_from)
jolteon = pokedex_user.get_pokemon('jolteon')   
print(jolteon.evolves_from)
flareon = pokedex_user.get_pokemon('flareon')
print(flareon.evolves_from)
espeon = pokedex_user.get_pokemon('espeon')
print(espeon.evolves_from)
umbreon = pokedex_user.get_pokemon('umbreon')
print(umbreon.evolves_from)
# leafeon = pokedex_user.get_pokemon('leafeon')
# print(leafeon.evolves_from)
print('---------------------------------')

# alakazam = pokedex_user.get_pokemon('alakazam')
# print(alakazam.name)
# print(alakazam.height)
# print(alakazam.weight)
# # print(alakazam.abilities)
# print(alakazam.stats)
# print(alakazam.types)
# print(alakazam.moves)
# print(alakazam.habitat)
# print(alakazam.evolves_from)
# print(alakazam.evolves_to)
print(pichu.evolves_from)