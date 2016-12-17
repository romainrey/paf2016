

class Point:
    #Attributes :
    #id : Integer
    #coordonnees : List of Integers
    #label : Integer
    
    def __init__(self):
        self.id = 0
        self.coordinates = []
        self.label = 0
    
    def __init__(self, id, coordinates, label):
        self.id = id
        self.coordinates = coordinates
        self.label = label
    
    def getId(self):
        return self.id
        
    def setId(self, id):
        self.id = id
    
    def getCoordinates(self):
        #anciennement getCoordonnees
        return self.coordinates
        
    def getCoordinate(self, i):
        #anciennement getCoordonnee
        return self.coordinates[i]
        
    def setCoordinates(self, coordinates):
        #anciennement setCoordonnees
        "Parameter: List of coordinates"
        self.coordinates = coordinates
    
    def setCoordinate(self, coordinate, i):
        #anciennement setCoordonnee
        self.coordinates[i] = coordinate
    
    def getLabel(self):
        return self.label
        
    def setLabel(self, label):
        self.label = label