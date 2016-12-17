import numpy as np
import Space
import Display 
import PointGenerator
import matplotlib.pyplot as plt
import time

fig = plt.figure()

def fKSource(listX, P):
    "Return the source complexity function K"
    result = 0
    conversionSpace = Space.Space(listX,None)
    list2X = conversionSpace.pointsListToMatrix()
    for i in range(len(list2X)):
        for j in range(len(P)):
            result += np.log2(1+np.abs(list2X[i][j]-P[j]))
    return result
    
def gradKSource(listX, P):
    "Return the source complexity function gradient"
    R = np.zeros(len(P))
    conversionSpace = Space.Space(listX,None)
    list2X = conversionSpace.pointsListToMatrix()
    for i in range(len(P)):
        result = 0
        for j in range(len(list2X)):
            
            result += np.sign(list2X[j][i]-P[i])*(-1)/(1+np.abs(list2X[j][i]-P[i]))
        R[i] = result
    return R
    
def iterateUniform(n,dim) :
    errorValue = 0
    for i in range(n):    
        pointGenerator = PointGenerator.PointGenerator()
        generatedPoints = pointGenerator.uniformPoints(100,dim,0,30)    
        generatedProtos = pointGenerator.generatePrototypes(4,generatedPoints,[0,1])
        
        space = Space.Space(generatedPoints,generatedProtos)
        
        space.associateProtosPoints()
        
        #savedDescentValue = space.adjustProtos(15, 1e-5, fKSource, gradKSource)
        #print(savedDescentValue)
        #print("*****     Final Prototypes     *****")
        #display.printProtos(space.getProtosList())
        #display.displaySpace(space,False)
        #adisplay.displayDescentValue(savedDescentValue)
        
        # *****      Transfer Start      *****
        generatedTargetPoints = pointGenerator.uniformPointsWithoutLabel(100,dim,30,100)
        targetSpace = Space.Space(generatedTargetPoints,[])
        #adisplay.printPoints(generatedTargetPoints)
        targetSpace = space.transfer(targetSpace)
        targetSpace.associateProtosPoints()
        targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
        targetSpace.associateProtosPointsAndModifyLabels()
        targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
        #display.displaySpace(targetSpace,True)
        properTargetPoints = pointGenerator.putLabelsOnHalfSplittingUniform(generatedTargetPoints,30,100)
        errorValue += targetSpace.errorCalculation(properTargetPoints)
    print("Success rate on  "+str(n)+" iterations: "+str(errorValue/n))
    return errorValue/n

def errorByDim(dimMax,n):
    "Return the success rate according to the dimension of the source space using n iterations of uniform distribution"
    list_dim = [i for i in range(1,dimMax+1)]
    list_error = []
    for i in range(len(list_dim)):
        list_error.append(iterateUniform(n,i+1))
    return list_dim, list_error
    
# *****      Debut des instructions      *****
#display = Display.Display()
#pointGenerator = PointGenerator.PointGenerator()
#generatedPoints = pointGenerator.uniformPoints(200,2,0,30)
##display.printPoints(generatedPoints)    
#generatedProtos = pointGenerator.generatePrototypes(4,generatedPoints,[0,1])
#
#space = Space.Space(generatedPoints,generatedProtos)
#        
#space.associateProtosPoints()
#
##X , Y = errorByDim(10,5)
##
##affichage.afficherErrorByDim(X,Y)
#
##affichage.printProtos(protosGeneres)
##affichage.printPoints(pointsGeneres)
#
#savedDescentValue = space.adjustProtos(15, 1e-5, fKSource, gradKSource)
#print(savedDescentValue)
#print("*****     Final Prototypes     *****")
##display.printProtos(space.getProtosList())
#dim = len(space.getPointsList()[0].getCoordinates())
#if(dim==2):
#    display.displaySpace(space,False)
#elif(dim==3):
#    display.display3DSpace(space,False,fig)
##affichage.afficherValeurDescente(stockageValeurDescente)
#
## *****      Debut du Transfert      *****
#generatedTargetPoints = pointGenerator.uniformPointsWithoutLabel(200,2,30,100)
#targetSpace = Space.Space(generatedTargetPoints,[])
##display.printPoints(generatedTargetPoints)
#targetSpace = space.transfer(targetSpace)
#targetSpace.associateProtosPoints()
#targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
#targetSpace.associateProtosPointsAndModifyLabels()
#targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
#if(dim==2):
#    display.displaySpace(targetSpace,True)
#elif(dim==3):
#    display.display3DSpace(targetSpace,True,fig)
#properTargetPoints = pointGenerator.putLabelsOnHalfSplittingUniform(generatedTargetPoints,30,100)
##display.printPoints(properTargetPoints)
#print("The success rate is: "+str(targetSpace.errorCalculation(properTargetPoints)))
#if(dim==3):
#    plt.show(fig)

start = time.time()
iterateUniform(10,2)
print("Time to complete: ", str(time.time() - start))

