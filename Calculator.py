import numpy as np
import Space
import random as rd
import copy

class Calculator:
    #Variables
    #fonctionK : Complexity Function
    #gradientK : Complexity Function Gradient
    
    def __init__(self, FKSource, GKSource):
        "Constructor using FKSource (source complexity function) and its gradient GKSource"
        self.functionKSource = FKSource
        self.gradientKSource = GKSource
        
    def executeFunctionK(self, pointCoordinates, network):
        #anciennement executerFonctionK
        "Execute the complexity function. Inputs : pointCoordinates is a numpy list of the Point coordinates, network is a Points list"
        return self.functionKSource(network, pointCoordinates)
    
    def executeGradientK(self, pointCoordinates, network):
        #anciennement executerGradientK
        "Execute the complexity function gradient. Inputs : pointCoordinates is a numpy list of the Point coordinates, network is a Points list"
        return self.gradientKSource(network, pointCoordinates)
        
    def getSavedDescentValue(self):
        #anciennement getValeurStockageDescente
        return self.savedDescentValue
        
    def norm(self, a):
        s = 0
        for i in range(a.shape[0]):
            s += a[i]**2
        return np.sqrt(s)
        
    def multiDimGradientDescent(self,f,fp,x0,epsilon,Nmax,network):
        #anciennement descenteGradientMultiDim
        "Inputs : network is a Points list, x0 : the starting numpy vector"
        #print("*** Fonction descenteGradienMultiDim ***"+str(x0))
        dimension = np.size(x0)
        gap = epsilon+1;
        next_x=np.copy(x0)
        step_index = 0
        alpha=0.01
        #graphX =[]
        #graphY= []
        
        while gap>epsilon and step_index<Nmax:
        
            former_x = np.copy(next_x)
        # print("xprecedent "+str(x_precedent))
            #Le np.int64 permet de gerer les valeurs grandes de gradien en 64 bits
            gradient = np.array(fp(network, former_x),np.int64)
            
            for i in range(dimension):
                #On fait la distinction si la norme = 0 alors c'est que le gradien est nul
                # mais on ne peut pas faire "0/0" donc on définie a la main le coeff a 0 dans ce cas
                if np.linalg.norm(gradient)!=0:                
                    coeff = gradient/self.norm(gradient)
                else :
                    coeff = np.zeros(dimension)
                next_x[i] = former_x[i] - coeff[i]*alpha
                signe = f(network, next_x)-f(network, former_x)
                #J'ai choisis d'incrementer peu alpha, car on place normalement les protos pas trop loins de la bonne valeur
                if signe>0 :
                    alpha = alpha*2
                else :
                    alpha = alpha*0.5
            #graphY.append(x_suivant, reseau) 
            #graphX.append(nb_etape)        
            gap = self.norm(former_x-next_x)
            step_index+=1
        #  print("nb etapes = "+str(nb_etape)+" | alpha = "+str(alpha)+" | ecart = "+str(ecart))
        
    # plt.plot(graphX,graphY ,color = 'r',linestyle = '-', marker='o')    
    # print("Le minimum trouve vaut : "+str(x_suivant))
    # print("***")
        return next_x,f(network,next_x)
        
    def getRandomPoints(self, X, f):
        L = copy.copy(X)
        i = 0
        ret = []
        while(i < (len(X)*f)):
            index = rd.randint(0, len(L) - 1)
            ret.append(L[index])
            del L[index]
            i += 1
        return ret
    
    def sourceGradientDescent(self,P,epsilon,Nmax):
        #anciennement descenteGradientSource
        "Descente de Gradient"
        network = self.getRandomPoints(P.getNetwork(), 0.01)
        network = network + [P]
        descentValue = []
        spaceForBary = Space.Space([],[])
        barycentre = spaceForBary.getBarycentrePoints(P.getNetwork() + [P])
        final_x,minimum = self.multiDimGradientDescent(self.functionKSource, self.gradientKSource, barycentre, epsilon, Nmax, network)
        for i in network :
            x,value = self.multiDimGradientDescent(self.functionKSource, self.gradientKSource, np.array(i.getCoordinates()),epsilon,Nmax,network)
            descentValue.append(value)
            if value < minimum :
                final_x = x
                minimum = value
        for i in range(final_x.shape[0]):
            P.setCoordinate(final_x[i], i)
        return P, descentValue