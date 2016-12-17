import numpy as np
import Space
import PointGenerator
import Display
import copy
import matplotlib.pyplot as plt
import time

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
    
if 0 :
    generator = PointGenerator.PointGenerator()
    points = generator.generateWholeDriftProblemTheta(100, 1)
    proto = generator.generatePrototypes([6, 2], points, [0, 1])
    space = Space.Space(points,proto)
        
    space.associateProtosPoints()
    display = Display.Display()
    
    space.adjustProtos(15, 1e-5, fKSource, gradKSource)
    nSteps = 10
    thetaMax = 0.2
    # *****      Debut du Transfert      *****
    for i in range(nSteps):
        theta = (i+1)/nSteps
        if(theta > thetaMax):
            break
        correctTargetPoints = generator.generateWholeDriftProblemTheta(100, theta)
        generatedTargetPoints = generator.eraseLabels(correctTargetPoints)
        #affichage.printPoints(pointsTargetGeneres)
        targetSpace = Space.Space(generatedTargetPoints,[])
        for i in targetSpace.protosList:
            if i.getCoordinate(0)>2:
                print("Not working l 58")
        targetSpace = space.transfer(targetSpace)
        targetSpace.associateProtosPoints()
        targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
        targetSpace.associateProtosPointsAndModifyLabels()
        targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
        #affichage.afficherEspace(espaceTarget,True)
        space = copy.deepcopy(targetSpace)
    print("Success rate: "+str(targetSpace.errorCalculation(correctTargetPoints)))
    display.displaySpace(targetSpace,True)

    generator = PointGenerator.PointGenerator()
    points = generator.generateWholeDriftProblemTheta(100, 1)
    proto = generator.generatePrototypes([6, 2], points, [0, 1])
    space = Space.Space(points,proto)
    space.associateProtosPoints()
    space.adjustProtos(15, 1e-5, fKSource, gradKSource)
    
if 0:
    generator = PointGenerator.PointGenerator()
    points = generator.generateWholeDriftProblemTheta(100, 0)
    proto = generator.generatePrototypes([6, 2], points, [0, 1])
    space = Space.Space(points,proto)
    space.associateProtosPoints()
    space.adjustProtos(15, 1e-5, fKSource, gradKSource)
    
    steps = generator.generateWholeDriftProblemByStep(100, 1, 10)
    targetSpace, error = space.transferStepByStep(space, steps, fKSource, gradKSource)
    print("Success rate: "+str(error))
    display = Display.Display()
    display.displaySpace(targetSpace, True)
    
if 0:
    display = Display.Display()
    generator = PointGenerator.PointGenerator()
    points = generator.generateWholeDriftProblemTheta(200, 0)
    proto = generator.generatePrototypes([5, 2], points, [0, 1])
    space = Space.Space(points,proto)
    space.associateProtosPoints()
    space.adjustProtos(500, 1e-5, fKSource, gradKSource)
    display.displaySpace(space, True)
    steps = generator.generateWholeDriftProblemByStep(200, 1, 10)
    targetSpace, error = space.transferStepByStep(space, steps, fKSource, gradKSource)
    print("Success rate: "+str(error))
    
    display.displaySpace(targetSpace, True)

start = time.time()
 
if 1:
    generator = PointGenerator.PointGenerator()
    results = []
    fracs = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75]
    #fracs = [0.4]
    N = 1
    for i in fracs:
        result = 0
        for k in range(N): #Averaging
            digit = generator.digits()
            digitSpace = Space.Space(digit, [])
            digit1 = digitSpace.getPointsFromLabel(1)
            digit1HalfSource, digit1HalfTarget = generator.splitDistrib(digit1, i)
            otherSource = digitSpace.getPointsFromLabel(7) + digitSpace.getPointsFromLabel(3) + digitSpace.getPointsFromLabel(4) + digitSpace.getPointsFromLabel(5)
            for j in otherSource:
                j.setLabel(0)
            otherTarget = digitSpace.getPointsFromLabel(6) + digitSpace.getPointsFromLabel(2) + digitSpace.getPointsFromLabel(8) + digitSpace.getPointsFromLabel(9)
            for j in otherTarget:
                j.setLabel(0)
            source = digit1HalfSource + otherSource
            target = otherTarget + digit1HalfTarget
            targetWithoutLabel = generator.eraseLabels(target)
            protos = generator.generateUnevenPrototypes([40, 10], source, [0, 1])
            sourceSpace = Space.Space(source, protos)
            sourceSpace.associateProtosPoints()
            sourceSpace.adjustProtos(500, 1e-5, fKSource, gradKSource)
            targetSpace = Space.Space(targetWithoutLabel, [])
            targetSpace = sourceSpace.transfer(targetSpace)
            targetSpace.associateProtosPoints()
            targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
            targetSpace.associateProtosPointsAndModifyLabels()
            targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
            succes = targetSpace.errorCalculation(target)
            print("Success : ", str(succes))
            result += succes
        result = result / N
        results.append(result)
    for i in range(len(fracs)):
        print(str(fracs[i]), " : ", results[i])
    plt.plot(fracs, results)
    plt.show()

print('Execution time: ' + str(time.time() - start))      
    
if 0:
    display = Display.Display()
    generator = PointGenerator.PointGenerator()
    points = generator.uniformPoints(200, 2, 0, 20)
    proto = generator.generateUnevenPrototypes([4, 4], points, [0, 1])
    space = Space.Space(points,proto)
    space.associateProtosPoints()
    space.adjustProtos(500, 1e-5, fKSource, gradKSource)
    display.displaySpace(space, True)
    targetPoints = generator.uniformPoints(200, 2, 60, 100)
    pointsWithoutLabel = generator.eraseLabels(targetPoints)
    targetSpace = Space.Space(pointsWithoutLabel, [])
    targetSpace = space.transfer(targetSpace)    
    display.displaySpace(targetSpace, True)
    targetSpace.associateProtosPoints()
    display.displaySpace(targetSpace)
    targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
    display.displaySpace(targetSpace)
    targetSpace.associateProtosPointsAndModifyLabels()
    display.displaySpace(targetSpace)
    targetSpace.adjustProtos(15, 1e-5, fKSource, gradKSource)
    display.displaySpace(targetSpace)
    error = targetSpace.errorCalculation(targetPoints)
    print("Success: ", str(error))
#generator = PointGenerator.PointGenerator()
#points = generator.generateNoisyMoons(200)
#protos = generator.generatePrototypes(5,points, [0, 1])
#space = Space.Space(points,protos)
#space.associateProtosPoints()
#space.adjustProtos(500, 1e-5, fKSource, gradKSource)
#
#
#display = Display.Display()
#display.displaySpace(space)
