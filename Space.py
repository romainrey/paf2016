import numpy as np
import Prototype
import Point
import Calculator
import copy
from math import sqrt
import PointGenerator
import time
import scipy.ndimage


class Space:
    "Un espace contient tous les points et protos de notre espace"

    
    def __init__(self): # Constructor w/o parameters
        self.pointsList = []
        self.protosList = []
        self.labelList = []
        self.formerProtoList = []
        self.graph_K = []
        self.initialProtoList = []
        
    def __init__(self,pointsList,protosList): # Constructor w parameters
        self.pointsList = pointsList
        self.labelList = []
        for i in self.pointsList:
            if((i.getLabel() in self.labelList) == False):
                self.labelList.append(i.getLabel())
        self.protosList = protosList
        self.formerProtoList = []
        self.graph_K = []
        self.initialProtoList = copy.deepcopy(protosList)
        
    def setListeLabel(self,sourceLabelList):
        self.labelList = sourceLabelList
        
    def distanceCalculation(self,a,b):
        #anciennement calculDistance
        "Inputs : a and b are Points. Return :  euclidean distance"
        s=0
        for i in range(len(a.getCoordinates())):
            s+=(a.getCoordinates()[i]-b.getCoordinates()[i])**2
        return sqrt(s)
        
    def getPointsList(self):
        return self.pointsList
        
    def getProtosList(self):
        return self.protosList
        
    def addProto(self, P):
        self.protosList.append(P)

    def getGraph(self):
        return self.graph_K
    
    def pointsNumber(self):
        return len(self.pointsList)
    
    def protosNumber(self):
        return len(self.protosList)
    
# Permet d'obtenir une matrice contenant les coordonnes des points     
    def pointsListToMatrix(self):
        "Return a matrix containing the points coordinates"
        #anciennement listePointsToMatrix
        return np.array(np.array([i.getCoordinates() for i in self.pointsList]))
  
# Permet d'obtenir une matrice contenant les coordonnes des protos     
    def protosListToMatrix(self):
        "Return a matrix containing the prototypes coordinates"
        #anciennement listeProtosToMatrix
        return np.array([i.getCoordinates() for i in self.protosList])
        
    def otherPointsListToMatrix(self, points):
        #anciennement ListeOtherPointsToMatrix
        "Return a matrix containing the other points coordinates"
        return np.array(np.array([i.getCoordinates() for i in points]))
        
    def matrixToPointsList(self,pointsMatrix, pointsLabels):
        #anciennement MatrixToListePoints
        "Return a Points list using the matrix of their coordinates"
        return [Point(i,pointsMatrix[i], pointsLabels[i]) for i in range(len(pointsMatrix))]
        
    def matrixToProtosList(self,protosMatrix, protosLabels):
        #anciennement MatrixToListeProtos
        "Return a Prototypes list using the matrix of their coordinates with an initially empty network. To complete the network, we use associateProtosPoints"
        return [Prototype(i,protosMatrix[i], protosLabels[i], []) for i in range(len(protosMatrix))]
        
    def transferStepByStep(self, startingSpace, stepsList, fKSource, gradKSource):
        #anciennement transfertParEtapes
        
        space = startingSpace
        generator = PointGenerator.PointGenerator()
        for i in range(len(stepsList)):
            generatedTargetPoints = generator.eraseLabels(stepsList[i])
            targetSpace = Space(generatedTargetPoints,[])
            targetSpace = space.transfer(targetSpace)
            targetSpace.associateProtosPoints()
            targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
            targetSpace.associateProtosPointsAndModifyLabels()
            targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
            space = copy.deepcopy(targetSpace)
        error = space.ErrorCalculation(stepsList[len(stepsList) - 1])
        return (space, error)
    
    def associateProtosPoints(self):
        #anciennement associerProtosPoints
        "Return : a modified version of the prototypes list so that their networks are filled optimally according to the points"
        time1 = time.time()
        # -----------------New Version-----------------
#        for p in self.protosList:
#            p.setNetwork([])
#        for i in self.labelList:
#            pointsLabel = self.getPointsFromLabel(i)
#            protosLabel = self.getProtosFromLabel(i)
#            #idPointsList = [j.getId() for j in pointsLabel]
#            #idProtosList = [j.getId() for j in protosLabel]
#            pointsMatrix = self.otherPointsListToMatrix(pointsLabel)
#            protosMatrix = self.otherPointsListToMatrix(protosLabel)
#            mytree = scipy.spatial.cKDTree(protosMatrix)
#            d,index = mytree.query(pointsMatrix,1)
#            for i in range(len(index)) :
#                protosLabel[index[i]].network+=[pointsLabel[i]]
                
         #-----------Former version -----------------"      
                
        for l in self.protosList:
            l.setNetwork([])
        for i in self.pointsList:
        #La distance est une simple norme de la difference entre le point et un proto
            k=0
            while (i.getLabel() != self.protosList[k].getLabel()) :
                k+=1
            min_distance = self.distanceCalculation(i,self.protosList[k])    
            min_proto = self.protosList[k]
            for j in self.protosList:
                if(i.getLabel() == j.getLabel()):
                    distance = self.distanceCalculation(i,j)
                    #print("distance de proto "+str(j.getId())+" avec point "+str(i.gteId())+" = "+str(distance))
                    if distance < min_distance :
                        min_distance = distance
                        min_proto = j
            min_proto.network.append(i)
        print("Time to complete: "+str(time.time()-time1))
        return self.protosList
        
    def associateProtosPointsAndModifyLabels(self):
        #anciennement associerProtosPointsEtModifLabels
        "Return : a modified version of the prototypes list so that their networks are filled optimally according to the points regardless of their label"
        for l in self.protosList:
            l.setNetwork([])
        for i in self.pointsList:
        #La distance est une simple norme de la difference entre le point et un proto
            k=0
            while (i.getLabel() != self.protosList[k].getLabel()) :
                k+=1
            min_distance = self.distanceCalculation(i,self.protosList[k])    
            min_proto = self.protosList[k]
            for j in self.protosList:
                distance = self.distanceCalculation(i,j)
                #print("distance de proto "+str(j.getId())+" avec point "+str(i.gteId())+" = "+str(distance))
                if distance < min_distance :
                    min_distance = distance
                    min_proto = j
            min_proto.network.append(i)
            if (min_proto.getLabel() != i.getLabel()):
                i.setLabel(min_proto.getLabel())
        return self.protosList
        
    def setPointLabelFromProto(self):
        for i in self.pointsList:
            min_proto = self.protosList[0]
            min_dist = self.distanceCalculation(i, min_proto)
            for j in self.protosList:
                dist = self.distanceCalculation(i, j)
                if(dist < min_dist):
                    min_proto = j
                    min_dist = dist
            i.setLabel(min_proto.getLabel())
        return 0
         
    def getPointsFromLabel(self, label):
        ret = []
        for i in self.pointsList:
            if(i.getLabel() == label):
                ret.append(i)
        return ret
        
    def getProtosFromLabel(self, label):
        ret = []
        for i in self.protosList:
            if(i.getLabel() == label):
                ret.append(i)
        return ret
    
    def f(x):
        return x
        
    def getBarycentrePoints(self, points):
#        calc = Calculator.Calculator(self.f, self.f)
#        extractedPoints = calc.getRandomPoints(points, 0.1)
#        matrix = self.otherPointsListToMatrix(points)
        matrix = self.otherPointsListToMatrix(points)
        length= len(matrix)        
        barycentre = np.zeros((1, len(matrix[0])))
        for i in range(len(matrix[0])):
            composante_i = np.sum(matrix[:, i])
            barycentre[0][i]=composante_i
        return barycentre[0]/length
        
    def transfer(self, targetSpace):
        #anciennement transfert
        "Transfer from the source space and distribution to the target space and distribution"
        targetSpace.setListeLabel(self.labelList)
        sourceBary = self.getBarycentrePoints(self.pointsList)
        targetBary = targetSpace.getBarycentrePoints(targetSpace.getPointsList())
        globalTranslation = targetBary - sourceBary
        for i in self.protosList:
            proto = Prototype.Prototype(i.getId(), copy.copy(i.getCoordinates()), i.getLabel(), [])
            targetSpace.addProto(proto)
        for i in targetSpace.protosList:
            coordinates = []
            for j in range(len(i.getCoordinates())):
                coordinates.append(i.getCoordinate(j) + globalTranslation[j])
            i.setCoordinates(coordinates)
        targetSpace.setPointLabelFromProto()
        for l in targetSpace.labelList:
            targetBaryL = targetSpace.getBarycentrePoints(targetSpace.getPointsFromLabel(l))
            protosFromLabel = targetSpace.getProtosFromLabel(l)
            protoBaryL = targetSpace.getBarycentrePoints(protosFromLabel)
            classTransformation = targetBaryL - protoBaryL
            for k in protosFromLabel:
                for j in range(len(k.getCoordinates())):
                    k.setCoordinate(k.getCoordinate(j) + classTransformation[j], j)
            
        return targetSpace
    
    def adjustProtos(self, nmax, epsilon, functionKSource, gradientKSource):
        #anciennement ajusterProtos
        "Readjust the prototypes position according to their network. Returns the values of the gradient descent in order to display it"
        n = 0
        resumeLoop = True
        savedDescentValue = []
        while(n < nmax and resumeLoop):
            print("passage")
            self.listeProtos = self.associateProtosPoints()
            resumeLoop = False
            tmp_res = 0
            percent20 = False
            percent40 = False
            percent60 = False
            percent80 = False
            
            for i in range(len(self.listeProtos)):
                pourcentage = i*100/len(self.listeProtos)
                if(pourcentage > 20 and pourcentage < 30 and percent20 == False):
                    print("Descente ", str(pourcentage), " %")
                    percent20 = True
                if(pourcentage > 40 and pourcentage < 50 and percent40 == False):
                    print("Descente ", str(pourcentage), " %")
                    percent40 = True
                if(pourcentage > 60 and pourcentage < 70 and percent60 == False):
                    print("Descente ", str(pourcentage), " %")
                    percent60 = True
                if(pourcentage > 80 and pourcentage < 90 and percent80 == False):
                    print("Descente ", str(pourcentage), " %")
                    percent80 = True
                self.formerProtoList.append(self.protosList[i].getCoordinates())
                calc = Calculator.Calculator(functionKSource,gradientKSource)
                formerProto = self.protosList[i]
                proto, descentValue = calc.sourceGradientDescent(self.protosList[i],epsilon,nmax)
                tmp_res += calc.executeFunctionK(proto.getCoordinates(), proto.getNetwork())
                if self.distanceCalculation(proto,formerProto)!=0:
                    resumeLoop = True
                    self.protosList[i] = proto
            print("Descente 100%")
            savedDescentValue.append(descentValue)
            self.graph_K.append(tmp_res)
            n += 1
        self.protosList = self.associateProtosPoints()
        return savedDescentValue
        
    def errorCalculation(self,labeledPointsList):
        "Return the success percentage rate"
        #anciennement calculErreur
        error,n = 0, len(self.pointsList)
        for i in range(n):
            if (self.pointsList[i].getLabel() != labeledPointsList[i].getLabel()):
                error += 1
        return (n-error)/n
            

