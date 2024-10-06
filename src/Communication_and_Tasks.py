'''
En el intercambio de información, o comunicación entre los agentes existen tres tipos de posibles interacciones:
1. Afirmaciones
2. Preguntas
3. Propuestas de intercambio

Cuando se hable de agente o de pokemon en la informacion, siempre se referira al id del mismo
'''

class Information():
    def __init__(self):
        pass

    
    # Afirmaciones
    
    @staticmethod
    def agente_encontrado(agente, coordenada):
        return f'Agente {agente} encontrado en coordenada {coordenada}'
    
    @staticmethod
    def pokemon_encontrado(pokemon, coordenada):
        return f'Pokemon {pokemon} encontrado en coordenada {coordenada}'
    
    @staticmethod
    def agente_tiene_pokemon(agente, pokemon):
        return f'Agente {agente} tiene Pokemon {pokemon}'
    
    @staticmethod
    def agente_tiene_propuesta(agente, propuesta):
        return f'Agente {agente} tiene Propuesta: {propuesta}'    

    # Preguntas

    @staticmethod
    def que_sabes_de_agente(agente):
        return f'Que sabes de Agente {agente}'
    
    @staticmethod
    def que_sabes_de_pokemon(pokemon):
        return f'Que sabes de Pokemon {pokemon}'
    

    # Propuestas de venta

    @staticmethod
    def vendo_pokemon(pokemon, precio):
        return f'Vendo Pokemon {pokemon} a {precio} unidades'
    
    @staticmethod
    def vendo_informacion_de_pokemon(pokemon, precio):
        return f'Vendo informacion sobre Pokemon {pokemon} a {precio} unidades'
    
    @staticmethod
    def vendo_informacion_de_agente(agente, precio):
        return f'Vendo informacion sobre Agente {agente} a {precio} unidades'
    

    # Propuesta de cambio
    
    @staticmethod
    def cambio_pokemon_por_pokemon(pokemon_a_dar, pokemon_a_recibir):
        return f'Cambio Pokemon {pokemon_a_dar} por Pokemon {pokemon_a_recibir}'
    
    @staticmethod
    def cambio_pokemon_por_informacion_pokemon(pokemon_a_dar, pokemon_inf_a_recibir):
        return f'Cambio Pokemon {pokemon_a_dar} por informacion sobre Pokemon {pokemon_inf_a_recibir}'
    
    @staticmethod
    def cambio_pokemon_por_informacion_agente(pokemon_a_dar, agente_inf_a_recibir):
        return f'Cambio Pokemon {pokemon_a_dar} por informacion sobre Agente {agente_inf_a_recibir}'
    
    @staticmethod
    def cambio_inf_pokemon_por_pokemon(pokemon_inf_a_dar, pokemon_a_recibir):
        return f'Cambio informacion sobre Pokemon {pokemon_inf_a_dar} por Pokemon {pokemon_a_recibir}'
    
    @staticmethod
    def cambio_inf_pokemon_por_inf_pokemon(pokemon_inf_a_dar, pokemon_inf_a_recibir):
        return f'Cambio informacion sobre Pokemon {pokemon_inf_a_dar} por informacion sobre Pokemon {pokemon_inf_a_recibir}'
    
    @staticmethod
    def cambio_inf_pokemon_por_inf_agente(pokemon_inf_a_dar, agente_inf_a_recibir):
        return f'Cambio informacion sobre Pokemon {pokemon_inf_a_dar} por informacion sobre Agente {agente_inf_a_recibir}'

    @staticmethod
    def cambio_inf_agente_por_pokemon(agente_inf_a_dar, pokemon_a_recibir):
        return f'Cambio informacion sobre Agente {agente_inf_a_dar} por Pokemon {pokemon_a_recibir}'
    
    @staticmethod
    def cambio_inf_agente_por_inf_pokemon(agente_inf_a_dar, pokemon_inf_a_recibir):
        return f'Cambio informacion sobre Agente {agente_inf_a_dar} por informacion sobre Pokemon {pokemon_inf_a_recibir}'
    
    @staticmethod
    def cambio_inf_agente_por_inf_agente(agente_inf_a_dar, agente_inf_a_recibir):
        return f'Cambio informacion sobre Agente {agente_inf_a_dar} por informacion sobre Agente {agente_inf_a_recibir}'
    


'''
    Se clasificarán las informaciones dependiendo que que tipo de información tengan, ejemplo relacionada con un 
Pokemon, un agente, una propuesta, etc
'''    

class Afirmation():
    def __init__(self, agente=None, pokemon=None, precio=None, coordenada=None, propuesta=None):
        self.information = None

        if agente != None and pokemon == None and precio == None and coordenada != None:  # entonces la afirmacion es sobre ubicacione del agente
            self.information = Information.agente_encontrado(agente=agente, coordenada=coordenada)
            self.type = ['Agente']
        elif agente == None and pokemon != None and precio == None and coordenada != None: # entonces la afirmacion es sobre ubicacion de pokemon
            self.information = Information.pokemon_encontrado(pokemon=pokemon, coordenada=coordenada)
            self.type = ['Pokemon']
        elif  agente != None and pokemon != None and precio == None and coordenada == None:
            self.information = Information.agente_tiene_pokemon(agente=agente, pokemon=pokemon)
            self.type = ['Agente', 'Pokemon']
        elif agente != None and propuesta != None:
            self.information = Information.agente_tiene_propuesta(agente=agente, propuesta=propuesta)
            self.type = ['Agente', 'Propuesta']

    def __str__(self) -> str:
        return self.information
    


class Question():
    def __init__(self, agente= None, pokemon = None):
        self.information = None

        if agente != None and pokemon == None:
            self.information = Information.que_sabes_de_agente(agente=agente)
            self.type = 'agente'
        elif agente == None and pokemon != None:
            self.information = Information.que_sabes_de_pokemon(pokemon=pokemon)
            self.type = 'pokemon'
    
    def __str__(self) -> str:
        return self.information


class PropuestaVentaInformation():
    def __init__(self, agente=None, pokemon=None, precio=None, propuesta:Afirmation=None):
        self.information = None
        self.propuesta = propuesta

        if agente != None and pokemon == None and precio != None and propuesta != None:
            self.information = Information.vendo_informacion_de_agente(agente=agente, precio=precio)
        elif agente == None and pokemon != None and precio != None and propuesta != None:
            self.information = Information.vendo_informacion_de_pokemon(pokemon=pokemon, precio=precio)
    
    def __str__(self) -> str:
        return self.information


class PropuestaVentaPokemon():
    def __init__(self, pokemon, precio):
        self.information = Information.vendo_pokemon(pokemon=pokemon, precio=precio)
    
    def __str__(self) -> str:
        return self.information


class PropuestaCambio():    # se asume que solo se le pasaran dos parametros
    def __init__(self, pokemon_a_dar=None, pokemon_a_recibir=None, agente_inf_a_dar=None, agente_inf_a_recibir=None, pokemon_inf_a_dar=None, pokemon_inf_a_recibir=None):
        self.information = None

        if pokemon_a_dar != None:
            if pokemon_a_recibir != None:
                self.information = Information.cambio_pokemon_por_pokemon(pokemon_a_dar=pokemon_a_dar, pokemon_a_recibir=pokemon_a_recibir)
            elif pokemon_inf_a_recibir != None:
                self.information = Information.cambio_pokemon_por_informacion_pokemon(pokemon_a_dar=pokemon_a_dar, pokemon_inf_a_recibir=pokemon_inf_a_recibir)
            elif agente_inf_a_recibir != None:
                self.information = Information.cambio_pokemon_por_informacion_agente(pokemon_a_dar=pokemon_a_dar, agente_inf_a_recibir=agente_inf_a_recibir)

        elif agente_inf_a_dar != None:
            if pokemon_a_recibir != None:
                self.information = Information.cambio_inf_agente_por_pokemon(agente_inf_a_dar=agente_inf_a_dar, pokemon_a_recibir=pokemon_a_recibir)
            elif agente_inf_a_recibir != None:
                self.information = Information.cambio_inf_agente_por_inf_agente(agente_inf_a_dar=agente_inf_a_dar, agente_inf_a_recibir=agente_inf_a_recibir)
            elif pokemon_inf_a_recibir != None:
                self.information = Information.cambio_inf_agente_por_inf_pokemon(agente_inf_a_dar=agente_inf_a_dar, pokemon_inf_a_recibir=pokemon_inf_a_recibir)
        
        elif pokemon_inf_a_dar != None:
            if pokemon_a_recibir != None:
                self.information = Information.cambio_inf_pokemon_por_pokemon(pokemon_inf_a_dar=pokemon_inf_a_dar, pokemon_a_recibir=pokemon_a_recibir)
            elif agente_inf_a_recibir != None:
                self.information = Information.cambio_inf_pokemon_por_inf_agente(pokemon_inf_a_dar=pokemon_inf_a_dar, agente_inf_a_recibir=agente_inf_a_recibir)
            elif pokemon_inf_a_recibir != None:
                self.information = Information.cambio_inf_pokemon_por_inf_pokemon(pokemon_inf_a_dar=pokemon_inf_a_dar, pokemon_inf_a_recibir=pokemon_inf_a_recibir)

    def __str__(self) -> str:
        return self.information
        

'''
    La funcion del objetivo es tener un conjunto de tareas o Tasks que hagan cumplir dicho objetivo, y verificar constantemente
en caso de que se haga cumplir dicho objetivo
'''        

class Objetivo():   
    def __init__(self, pokemones=None):
        self.tasks = []

        if pokemones != None:
            for i in range(len(pokemones)):
                task = Task(pokemones[i].id)
                self.tasks.append(task)

        self.cumplido = False



    def VerificarCumplido(self, pokemon_inventory):   # recibe como parametro un inventario de pokemon, verifica si el pok esta ahi
                                                      # en caso de que si entonces el objetivo se cumplio
        for i in range(len(self.tasks)):
            if not pokemon_inventory[i].cumplido:
                return False
        
        self.cumplido = True
        return True



class Task():
    def __init__(self, pokemon=None):
        self.cumplida = False

        if pokemon != None:
            self.task = f'Obtener a Pokemon {pokemon}.'
            self.formas_de_cumplir = ['Capturar', 'Comprar', 'Cambiar']
            self.type == 'Pokemon'

    def __str__(self) -> str:
        return self.task