import numpy as np
import Point

class Prototype(Point.Point):
    #Variables :
    #network : Points list
    
    def __init__(self):
        super(Point,self).__init__()
        self.network = []
    
    def __init__(self, id, coordinates, label, network):
        super(Point.Point,self).__init__()
        self.id=id
        self.coordinates = coordinates
        self.label=label
        self.network = network
    
    def getNetwork(self):
        #anciennement getReseau
        return self.network
        
    def setNetwork(self, network):
        #anciennement setReseau
        self.network = network
    
    def networkToMatrix(self):
        #anciennement reseauToMatrix
        "Convert the network of a prototype into a matrix containing the coordinates of the points belonging to the network of the protype calling this function"
        network = np.zeros((len(self.network), len(self.network[0].getCoordinates())))
        for i in range (len(self.network)):
            coordinates = self.network[i].getCoordinates()
            for j in range (len(coordinates)):
                network[i,j] = coordinates[j]
        return network
        