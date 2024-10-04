from Communication import *

afirmation = Afirmation(agente=1, coordenada=(3,4))
print(afirmation)

afirmation = Afirmation(pokemon=2, coordenada=(3,4))
print(afirmation)

afirmation = Afirmation(agente=1, pokemon=2)
print(afirmation)

information = Information.cambio_pokemon_por_pokemon(pokemon_a_dar=1, pokemon_a_recibir=3)

afirmation = Afirmation(agente=1, propuesta=information)
print(afirmation)

question = Question(agente=1)
print(question)

question = Question(pokemon=1)
print(question)

prop_venta_inf = PropuestaVentaInformation(agente=1, precio=100, propuesta=information)
print(prop_venta_inf)

prop_venta_inf = PropuestaVentaInformation(pokemon=1, precio=10, propuesta=information)
print(prop_venta_inf)

prop_venta_pok = PropuestaVentaPokemon(pokemon=1, precio=10)
print(prop_venta_pok)


prop_cambio = PropuestaCambio(pokemon_a_dar=1, pokemon_a_recibir=2)
print(prop_cambio)

prop_cambio = PropuestaCambio(pokemon_a_dar=1, agente_inf_a_recibir=1)
print(prop_cambio)

prop_cambio = PropuestaCambio(pokemon_a_dar=1, pokemon_inf_a_recibir=1)
print(prop_cambio)


prop_cambio = PropuestaCambio(agente_inf_a_dar=1, pokemon_a_recibir=1)
print(prop_cambio)

prop_cambio = PropuestaCambio(agente_inf_a_dar=1, agente_inf_a_recibir=2)
print(prop_cambio)

prop_cambio = PropuestaCambio(agente_inf_a_dar=1, pokemon_inf_a_recibir=2)
print(prop_cambio)


prop_cambio = PropuestaCambio(pokemon_inf_a_dar=1, pokemon_a_recibir=2)
print(prop_cambio)

prop_cambio = PropuestaCambio(pokemon_inf_a_dar=1, agente_inf_a_recibir=2)
print(prop_cambio)

prop_cambio = PropuestaCambio(pokemon_inf_a_dar=1, pokemon_inf_a_recibir=2)
print(prop_cambio)

'''
Test de creacion de informacion finalizado
'''