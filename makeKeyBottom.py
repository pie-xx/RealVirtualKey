import math
import STLLathe

tedgeI = STLLathe.createTurtleEdge()
tedgeI.pieTurn(0,2.0*math.pi,4.0,(0.0,0.0),32)
tedgeI.setLoop()
edgeI = tedgeI.getEdge()
tedgeO = STLLathe.createTurtleEdge()
tedgeO.pieTurn(0,2.0*math.pi,9.0,(0.0,0.0),32)
tedgeO.setLoop()
edgeO = tedgeO.getEdge()
tedge2 = STLLathe.createTurtleEdge()
tedge2.pieTurn(0,2.0*math.pi,5.5,(0.0,0.0),32)
tedge2.setLoop()
edgeI2 = tedge2.getEdge()
tedge3 = STLLathe.createTurtleEdge()
tedge3.pieTurn(0,2.0*math.pi,7.0,(0.0,0.0),32)
tedge3.setLoop()
edgeI3 = tedge3.getEdge()



mstl = STLLathe.create()

#edgeI = mstl.createPieEdge(0,2.0*math.pi,4.0,(0.0,0.0),32)
#edgeI.append(edgeI[0])
#edgeO = mstl.createPieEdge(0,2.0*math.pi,9.0,(0.0,0.0),32)
#edgeO.append(edgeO[0])

#edgeI2 = mstl.createPieEdge(0,2.0*math.pi,5.5,(0.0,0.0),32)
#edgeI2.append(edgeI2[0])
#edgeI3 = mstl.createPieEdge(0,2.0*math.pi,7.0,(0.0,0.0),32)
#edgeI3.append(edgeI3[0])


mstl.addSide(0.0,edgeI,0.0,edgeO)
mstl.addSide(1.0,edgeI,0.0,edgeI)
mstl.addSide(0.0,edgeO,1.0,edgeO)

mstl.addSide(1.0,edgeI2,1.0,edgeI)
mstl.addSide(1.0,edgeO,1.0,edgeI3)

mstl.addSide(10.0,edgeI2, 1.0, edgeI2)
mstl.addSide(1.0,edgeI3, 10.0, edgeI3)

mstl.addSide(10.0,edgeI3, 10.0, edgeI2)


mstl.save('kb5.5.b.stl')
