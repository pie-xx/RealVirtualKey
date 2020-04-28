from stl import mesh
import math
import numpy as np

def create():
		return STLLathe()

class STLLathe():
	def __init__(self, **kwargs):
		self.faces=[]

	def createPieEdge(self, srad,trad,radius,center,partnum):
		edge=[]
		for n in range(partnum):
			t = ( n / partnum )*(trad-srad) + srad
			cost = math.cos(t)
			sint=math.sin(t)
			edge.append((cost*radius, sint*radius))
		return edge

	def addCirclePlane(self,  z, center, edge ):
		cP = [center[0], center[1], z ]
		oP = [ edge[-1][0], edge[-1][1], z ]
		for e in edge:
			eP = [ e[0], e[1], z ]
			self.faces.append([cP, eP, oP])
			oP = eP

	def addPiePlane(self,  z, center, edge ):
		cP = [center[0], center[1], z ]
		se = edge[0]
		oP = [ se[0], se[1], z ]
		for n in range(1,len(edge)):
			e = edge[n]
			eP = [ e[0], e[1], z ]
			self.faces.append([cP, eP, oP])
			oP = eP

	def addSide(self, top, edgetop, bottom, edgebtm):
		oT = edgetop[0]
		oB = edgebtm[0]
		for n in range(1,len(edgetop)):
			cT = edgetop[n]
			cB = edgebtm[n]

			pt0=[oT[0],oT[1],top]
			pt1=[cT[0],cT[1],top]
			pb0=[oB[0],oB[1],bottom]
			pb1=[cB[0],cB[1],bottom]
			self.faces.append([pt0,pb1,pb0])
			self.faces.append([pt0,pt1,pb1])
			oT=cT
			oB=cB

	def save(self,	fname ):
		b = np.array(self.faces).reshape([len(self.faces), 3, 3])
		data = np.zeros(len(b), dtype=mesh.Mesh.dtype)
		data['vectors']=b
		your_mesh = mesh.Mesh(data, remove_empty_areas=False)
		your_mesh.save( fname )


