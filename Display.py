import matplotlib.pyplot as plt



class Display:
    "Class used to display all the graphs needed"
        
    def displayPoints(self,X):
        #anciennement afficherPoints"
        "X : list of Points. Displaying points in the shape of a cross"
        color_list=['b', 'r', 'g', 'y', 'm', 'c']
        for i in X :
            color = color_list[i.getLabel() % len(color_list)]
            if i.getLabel() == 30:
                color = 'k'
            plt.plot(i.getCoordinates()[0], i.getCoordinates()[1], color = color, linestyle = '', marker='x', markersize = 5)
        plt.grid()
        plt.show()
        
    def display3DPoints(self,X, fig):
        #anciennement afficherPoints3D
        "X : list of Points. Displaying points in the shape of a cross"
        ax = fig.gca(projection='3d')
        color_list=['b', 'r', 'g', 'y', 'm', 'c']
        for i in X :
            ax.scatter(i.getCoordinates()[0],i.getCoordinates()[1], i.getCoordinates()[2] ,color = color_list[i.getLabel() % len(color_list)], marker='o', s = 5, depthshade = True)
        ax.grid()
        
          
        
    def displayInitialPrototypes(self,P):
        #anciennement afficherProtosInitiaux
        "P : list of Prototypes. Shape of initial prototypes : round"
        color_list=['b', 'r', 'g', 'y', 'm', 'c']
        for i in P :
            plt.plot(i.getCoordinates()[0], i.getCoordinates()[1], color = color_list[i.getLabel() % len(color_list)], linestyle = '', marker='x', markersize = 5)
        plt.grid()
        plt.show()    
        
    def displayInitial3DPrototypes(self,P, fig):
        #anciennement afficherProtosInitiaux3D
        "P : list of Prototypes. Shape of initial prototypes : round"
        ax = fig.gca(projection='3d')
        color_list=['b', 'r', 'g', 'y', 'm', 'c']
        for i in P :
            ax.scatter(i.getCoordinates()[0],i.getCoordinates()[1], i.getCoordinates()[2] , color = color_list[i.getLabel() % len(color_list)], marker='^', s = 50, depthshade = True)
        ax.grid()
        
        
        
    def displayFinalPrototypes(self,P):
        #anciennement afficherProtosFinaux
        "P : list of Prototypes. Shape of initial prototypes : square. Also displaying the network links" 
        color_list=['b', 'r', 'g', 'y', 'm', 'c']        
        for i in P:
            absP = i.getCoordinates()[0]
            ordP = i.getCoordinates()[1]
            labelP = i.getLabel()
            plt.plot(absP, ordP, color = color_list[labelP % 6], linestyle = '', marker='s', markersize = 10,  markeredgecolor = 'r')
            network = []
            network = i.getNetwork()
            for j in network :
                plt.plot([absP, j.getCoordinates()[0]], [ordP, j.getCoordinates()[1]], color = color_list[labelP % len(color_list)], linestyle = '--', marker='', linewidth = '0.5')
        plt.grid()
        plt.show()

    def displayFinal3DPrototypes(self,P, fig):
        #anciennement afficherProtosFinaux3D
        "P : list of Prototypes. Shape of initial prototypes : square. Also displaying the network links"
        ax = fig.gca(projection='3d')
        color_list=['b', 'r', 'g', 'y', 'm', 'c']
        for i in P:
            absP = i.getCoordinates()[0]
            ordP = i.getCoordinates()[1]
            Zcoord = i.getCoordinates()[2]
            labelP = i.getLabel()
            ax.scatter(absP,ordP, Zcoord ,color = color_list[labelP % 6], marker='^', s = 50, depthshade = True)
            network = []
            network = i.getNetwork()
            for j in network :
                ax.plot([absP,j.getCoordinates()[0]],[ordP,j.getCoordinates()[1]],[Zcoord,j.getCoordinates()[2]],color = color_list[labelP % len(color_list)],linestyle = '--', marker='', linewidth = '0.5')
        ax.grid()
        
        
        
        
        
    def displayIntermediatesPrototypes(self,formerProtoList):
        #anciennement afficherProtosIntermediaires
        "Input : list of coordinates. Display intermediate prototypes in the shape of small black square"
        for i in formerProtoList:
            plt.plot(i[0],i[1] ,color = 'k',linestyle = '', marker='s', markersize = 1)
        plt.grid()
        plt.show()
        
    
        
    def displayFunction(self,X):
        #anciennement afficherFonction
        "To be used after displaying the Points. Input : list of values. Return : values"
        print("affiche fontion "+str(X))        
        plt.figure()
        plt.plot([i for i in range(len(X))],X)
        plt.show()
        
        
    def displaySpace(self,space,finish=True):
        #anciennement afficherEspace
       # if finish :
        #    plt.close()
        plt.figure()        
        self.displayPoints(space.pointsList)
        self.displayInitialPrototypes(space.initialProtoList)
        self.displayFinalPrototypes(space.protosList)
        self.displayIntermediatesPrototypes(space.formerProtoList)
        #self.displayFunction(space.graph_K)
        
        
    def display3DSpace(self,space,finish,fig):
        #anciennement afficherEspace3D
       # if finish :
        #    plt.close()

        self.display3DPoints(space.pointsList, fig)
        self.displayInitial3DPrototypes(space.initialProtoList, fig)
        self.displayFinal3DPrototypes(space.protosList, fig)
        
        
    
    def printPoints(self,X) :
        for i in X :
            string3=""
            k=0
            for l in i.getCoordinates():
                k+=1
                string3 += " | X"+str(k)+" = "+str(l)
            print("Point = "+str(i.getId())+string3+" | label = "+str(i.label))
    
    
    def printProtos(self,P):
        for i in P :
            string2 ="Point "
            k=0
            string3=""
            for j in i.network :
                string2 += str(j.getId())+", "
            for l in i.getCoordinates():
                k+=1
                string3 += " | X"+str(k)+" = "+str(l)
            print("Proto  id = "+str(i.getId())+string3+" | label = "+str(i.label)+" | Reseau = "+string2)
            
    def displayDescentValue(self,savedDescentValue) :
        "Displays the different final values of the gradient descent"
        #anciennement afficherValeurDescente
        print(savedDescentValue)
      #  for i in stockageValeurDescente:
       #     plt.figure()
      #      plt.plot([j for j in range(len(i))],i)
        plt.figure()
        plt.plot([j for j in range(len(savedDescentValue[0]))],savedDescentValue[0]) 
        plt.show()
    
    def displayErrorByDim(self,X,Y):
        #anciennement afficherErrorByDim
        plt.figure()
        plt.plot(X,Y)
        plt.show()
        