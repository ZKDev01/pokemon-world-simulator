class Move():
    def __init__(self, name:str, power:int, pp:int, accuracy:int, type_id:int, category:str,
                 ailment:str, target:str, effect):  # el efect esta en veremos de que tipo va a ser
        
        self.name = name
        self.power = power
        self.pp = pp
        self.accuracy = accuracy
        self.type_id = type_id
        self.category = category
        self.ailment = ailment
        self.target = target
        self.effect = effect