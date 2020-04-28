import math
import STLLathe

mstl = STLLathe.create()

edgeI = mstl.createPieEdge(0,2.0*math.pi,4.0,(0.0,0.0),32)
edgeI.append(edgeI[0])
edgeO = mstl.createPieEdge(0,2.0*math.pi,9.0,(0.0,0.0),32)
edgeO.append(edgeO[0])

edgeI2 = mstl.createPieEdge(0,2.0*math.pi,5.5,(0.0,0.0),32)
edgeI2.append(edgeI2[0])
edgeI3 = mstl.createPieEdge(0,2.0*math.pi,7.0,(0.0,0.0),32)
edgeI3.append(edgeI3[0])


mstl.addSide(0.0,edgeI,0.0,edgeO)
mstl.addSide(1.0,edgeI,0.0,edgeI)
mstl.addSide(0.0,edgeO,1.0,edgeO)

mstl.addSide(1.0,edgeI2,1.0,edgeI)
mstl.addSide(1.0,edgeO,1.0,edgeI3)

mstl.addSide(10.0,edgeI2, 1.0, edgeI2)
mstl.addSide(1.0,edgeI3, 10.0, edgeI3)

mstl.addSide(10.0,edgeI3, 10.0, edgeI2)


mstl.save('kb5.5.stl')
