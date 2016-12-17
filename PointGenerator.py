from sklearn import datasets
import Point
import Prototype
import random as rd
import copy
import numpy as np


class PointGenerator:
    
    def __init__(self):
        return
        
    def digits(self):
        "Generate the digit distribution"
        digit = datasets.load_digits()
        return self.matrixAndLabelsToPoints(digit.data, digit.target)
        
    def uniformPoints(self,n, dim, a, b):
        #anciennement pointsUniforme
        "Retourne un liste de points générés"
        X=[]
        for i in range(0,n):
            xi = Point.Point(-1,[i for i in range(dim)],30)
            for j in range(dim):
                xi.setCoordinate(rd.uniform(a,b), j)
            xi.setId(i)
            
            if (xi.getCoordinate(0) < (b+a)/2):
                xi.setLabel(0)
            else :
                xi.setLabel(1)
                
            X += [xi]
        return X   
        
    def splitDistrib(self, X, f):
        "Splits the distribution in half"
        x1 = X[0:(int)(f*len(X))]
        x2 = X[(int)(f*len(X)):len(X)]
        return x1, x2

    def uniformPointsWithoutLabel(self,n, dim, a, b):
        #anciennement pointsUniformeWithoutLabel
        "Generate a list of points without label"
        X=[]
        for i in range(0,n):
            xi = Point.Point(-1,[i for i in range(dim)],30)
            for j in range(dim):
                xi.setCoordinate(rd.uniform(a,b), j)
            xi.setId(i)
                
            X += [xi]
        return X
        
    def putLabelsOnHalfSplittingUniform(self, pointsList, a,b):
        #anciennement putLabelsMoitieUniform
        "Put labels on a separated in half uniform distribution"
        workingList = copy.deepcopy(pointsList)
        j=0
        for i in workingList:
            if (i.getCoordinate(0)<((b+a)/2)):
                i.setLabel(0)
                j+=1
            else :
                i.setLabel(1)
        return workingList
            
    def matrixAndLabelsToPoints(self, X, labelsList):
        "Generate Point objects from their coordinates and their label"
        points = []
        for i in range(X.shape[0]):
            coordinates = []
            for j in range(X.shape[1]):
                coordinates.append(X[i,j])
            points.append(Point.Point(i, coordinates, labelsList[i]))
        return points
        
    def pointsToMatrixAndLabels(self, points):
        "Generate the coordinates matrix and label list from Point objects"
        X = np.zeros((len(points), len(points[0].getCoordinates())))
        Y = np.zeros((len(points)))
        for i in range(len(points)):
            for j in range(len(points[i].getCoordinates())):
                X[i,j] = points[i].getCoordinate(j)
            Y[i] = points[i].getLabel()
        return X,Y
    
    def blobToPoints(self, blobs, labelsList):
        "Generate points forming a blob"
        points = []
        for k in range(len(blobs)):
            X = blobs[k]
            for i in range(X.shape[0]):
                coordinates = []
                for j in range(X.shape[1]):
                    coordinates.append(X[i,j])
                points.append(Point.Point(i, coordinates, labelsList[i]))
        return points
        
    def generateNoisyCircles(self, n_samples):
        (X, labs) = datasets.make_circles(n_samples=n_samples, factor=.5,noise=.05)
        return self.matrixAndLabelsToPoints(X, labs)
    
    def generateNoisyMoons(self, n_samples):
        (X, labs) = datasets.make_moons(n_samples=n_samples, noise=.05)
        return self.matrixAndLabelsToPoints(X, labs)
        
    def generateBlobs(self, n_samples):
        blobs = datasets.make_blobs(n_samples=n_samples, random_state=8)
        print(blobs)
        (X, labs) = blobs
        return self.matrixAndLabelsToPoints(X, labs)
        
    def generateDeformation(self, nPointsSide, delta, length):
        angle = delta
        nPoints = 2 * nPointsSide + 1
        X = np.zeros((nPoints,2))
        for i in range(nPointsSide):
            x = X[2*i,:]
            X[2*i+2,:] = [x[0] + length * np.sin(angle), x[1] + length * np.cos(angle)]
            X[2*i+1,:] = [X[2*i+2,0], -X[2*i+2,1]]
            angle = angle + delta
        return X
    
    def generateBlob(self, nPoints):
        rhos = np.random.rand(nPoints)
        thetas = 2 * np.pi * np.random.rand(nPoints)
        x = rhos * np.cos(thetas)
        y = rhos * np.sin(thetas)
        
        return np.transpose(np.vstack((x,y)))
        
    def eraseLabels(self, points):
        pointsCopy = copy.deepcopy(points)
        for i in pointsCopy:
            i.setLabel(30)
        return pointsCopy
    
    def generateWholeDriftProblemByStep(self, nbPoints, thetaMax, nbEtapes):
        listeEtapes = []
        for i in range(nbEtapes):
            theta = (i+1)*thetaMax/nbEtapes
            listeEtapes.append(self.generateWholeDriftProblemTheta(nbPoints, theta))
        return listeEtapes
        
    def generateWholeDriftProblemTheta(self, nbrePoints, theta = 0):
        nPointsSide = nbrePoints - 1
        radius = 1
        nPointsBlob = nbrePoints
        nPoints = 2 * nPointsSide + 1
        maxAngle = 2 * np.pi / nPoints
        L0 = 1.0 / nPointsSide
        L1 = 2 * radius * np.sin(np.pi / nPoints)        
        delta = maxAngle * theta
        length = L0 + (L1 - L0) * theta
        X = self.generateDeformation(nPointsSide, delta, length)
        blob = [1.0, 0.0] + 0.25 * self.generateBlob(nPointsBlob)
        #return blobs, transf, Y
#        print(len(transf[0]))
#        print(len(Y))
#        return (self.matrixAndLabelsToPoints(blobs, Y), self.matrixAndLabelsToPoints(transf, Y))
        return self.matrixAndLabelsToPoints(X, np.zeros((len(X)))) + self.matrixAndLabelsToPoints(blob, np.ones((len(X))))

        
        
    def slicePoints(self, X, labels):
        #anciennement decouper_X
        listXByLabels = []
        for label in labels:
            labelI = []
            for i in X:
                if(i.getLabel() == label):
                    labelI.append(i)
            listXByLabels.append(labelI)
        return listXByLabels
        
    def generateUnevenPrototypes(self, m, X, labels):
        "In that case, m is a list containing the number of prototypes for each label"
        listP = []
        listXByLabel = self.slicePoints(X, labels)
        indexesList = []
        for i in range(len(labels)):
            indexesList.append([])
        maxM=max(m)
        for i in range(len(m)):
            for j in range(len(labels)):
                if i > m[j] - 1:
                    continue
                proto=Prototype.Prototype(-1,[i for i in range(len(X[0].getCoordinates()))],30,[])
                index = rd.randint(0, len(listXByLabel[j])-1)
                while index in indexesList[j]:
                    index = rd.randint(0, len(listXByLabel[j])-1)
                indexesList[j].append(index)
                for k in range(len(listXByLabel[j][index].getCoordinates())):
                    proto.setCoordinate(listXByLabel[j][index].getCoordinate(k),k)
                proto.label = labels[j]
                proto.reseau = []
                proto.id = i + labels[j]*maxM
                listP.append(proto)
        return listP
        
    def generatePrototypes(self, m, X, labels):
        "There is the same number of prototype for each label"
        listP = []
        listXByLabel = self.slicePoints(X, labels)
        indexesList = []
        for l in range(len(labels)):
            indexesList.append([])
        for i in range(m):
            for j in range(len(labels)):
                proto=Prototype.Prototype(-1,[i for i in range(len(X[0].getCoordinates()))],30,[])
                index = rd.randint(0, len(listXByLabel[j])-1)
                while index in indexesList[j]:
                    index = rd.randint(0, len(listXByLabel[j])-1)
                indexesList[j].append(index)
                for k in range(len(listXByLabel[j][index].getCoordinates())):
                    proto.setCoordinate(listXByLabel[j][index].getCoordinate(k),k)
                proto.label = labels[j]
                proto.network = []
                proto.id = i + labels[j]*m
                listP.append(proto)
        return listP
        