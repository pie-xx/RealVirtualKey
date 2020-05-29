from stl import mesh
import math
import numpy as np
import copy
from mpl_toolkits import mplot3d

def STLmaker():
        return STLLathe()

class STLLathe():
    def __init__(self, **kwargs):
        self.faces=[]

    def perpendicular( A, B, P ):
        if( A==B ):
            return A, 0
        if math.fabs(A[0]-B[0]) < 0.00001 :
            return (A[0], P[1]), 0
        if math.fabs(A[1]-B[1]) < 0.00001 :
            return (P[0], A[1]), 0
        a = ( A[0]-B[0], A[1]-B[1] )
        qx = (a[0]**2*P[0]+a[0]*a[1]*(P[1]-A[1])+a[1]**2*A[0])/(a[0]**2+a[1]**2)
        k = a[0]/(A[0]-qx)
        qy = A[1] - a[1]/k
        return (qx, qy), k

    """
    A=(0,0)
    B=(2,2)
    P=(0,4)
    print(perpendicular(A,B,P))
    """
    def getra( x, y ):
        c = math.sqrt(x**2 + y**2 )
        a = 0
        b = 0
        if c!= 0.0:
            a = 1.0 * y / c
            b = 1.0 * x / c
        else:
            if x==0.0:
                a = 0.0
                b = 1.0
            else:
                a = 1.0
                b = 0.0
        return a, b

    def distance( a, b ):
        d = (a[0] - b[0])**2 + (a[1] - b[1])**2
        return d

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

    def save(self,  fname ):
        self.getMesh().save( fname )
        
    def getMesh(self):
        b = np.array(self.faces).reshape([len(self.faces), 3, 3])
        data = np.zeros(len(b), dtype=mesh.Mesh.dtype)
        data['vectors']=b
        your_mesh = mesh.Mesh(data, remove_empty_areas=False)
        return your_mesh
    
    def setMesh(self, data):
        self.faces=data.vectors
    
    def rotate(self, axis, rad ):
        mesh = self.getMesh()
        mesh.rotate( axis, rad )
        mesh.update_normals()
        self.setMesh(mesh)
    
    def addMesh(self, mesh):
        b =  mesh.vectors
        self.faces = np.concatenate( [self.faces, b] )

    def plot( self, fig ):
        your_mesh = self.getMesh()
        axes = mplot3d.Axes3D(fig)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten('C')
        axes.auto_scale_xyz(scale, scale, scale)

def Edgemaker():
    return TurtleEdge()

class TurtleEdge():
    def __init__(self, **kwargs):
        self.edge=[]
        self.dirt=0.0
        self.dirx=1.0
        self.diry=0.0

    def moveTo(self, p ):
        self.edge.append(p)

    def moveToR( self, rx, ry ):
        if len(self.edge)==0:
                self.edge.append((0.0,0.0))
        lastp = self.edge[-1]
        self.dirx=rx
        self.diry=ry
        self.edge.append((lastp[0]+rx, lastp[1]+ry))

    def forward( self, d ):
        c2=self.dirx**2+self.diry**2
        if d==0.0 or c2 == 0.0 :
            return
        c=math.sqrt( c2 )
        rx = self.dirx * (d / c )
        ry = self.diry * (d / c )
        self.moveToR( rx, ry )

    def turn( self, t ):
        cost=math.cos(t)
        sint=math.sin(t)
        c2=self.dirx**2+self.diry**2
        if c2 == 0.0 :
            self.dirx=cost
            self.diry=sint
            return
        c=math.sqrt( c2 )
        rx=self.dirx/c
        ry=self.diry/c
        self.dirx = ry*sint + rx * cost 
        self.diry = ry*cost - rx * sint

    def turnD( self, d ):
        self.turn( d / 180 * math.pi )

    def pieTurn(self, srad, trad, radius, center, partnum):
        for n in range(partnum):
            t = ( n / partnum )*(trad-srad) + srad
            cost = math.cos(t)
            sint = math.sin(t)
            self.edge.append((cost*radius+center[0], sint*radius+center[1]))
        cost = math.cos(trad)
        sint = math.sin(trad)
        self.edge.append((cost*radius+center[0], sint*radius+center[1]))


    def getEdge(self):
        return self.edge

    def getRevEdge(self):
        redge=copy.copy(self.edge)
        redge.reverse()
        return redge

    def appendEdge(self, a):
        self.edge.append( a )

    def setLoop(self):
        self.edge.append( self.edge[0] )

    def plot(self, fig):
        ax = fig.add_subplot(111)
        px=[]
        py=[]
        n=0
        for p in self.edge:
            px.append(p[0])
            py.append(p[1])
            if n!=0:
                ax.text(p[0],p[1], "{}".format(n), size = 8, color = "green")
            n=n+1

        ax.plot(px, py, color = "red", linestyle = "-")

def createHole( radius, depth ):
    holeedge=createTurtleEdge()
    holeedge.pieTurn( 0, math.pi*2, radius, (0.0, 0.0), 32 )
    holeedge.setLoop()

    hstl = create()
    pl0 = holeedge.getRevEdge()[25:33]
    pl0.append((radius,0.0))
    hstl.addSide( 0.0, holeedge.getRevEdge(), depth, holeedge.getRevEdge() )
    hstl.addPiePlane( 0.0, (radius,radius), pl0)
    pl0.reverse()
    hstl.addPiePlane( depth, (radius,radius), pl0)

    pl0=holeedge.getRevEdge()[17:25]
    pl0.append((0.0,radius))
    hstl.addPiePlane( 0.0, (-radius,radius), pl0)
    pl0.reverse()
    hstl.addPiePlane( depth, (-radius,radius), pl0)

    pl0=holeedge.getRevEdge()[9:17]
    pl0.append((-radius,0))
    hstl.addPiePlane( 0.0, (-radius,-radius), pl0)
    pl0.reverse()
    hstl.addPiePlane( depth, (-radius,-radius), pl0)

    pl0=holeedge.getRevEdge()[1:9]
    pl0.append((0,-radius))
    hstl.addPiePlane( 0.0, (radius,-radius), pl0)
    pl0.reverse()
    hstl.addPiePlane( depth, (radius,-radius), pl0)

    return hstl

def createNutHole( nheadradius, nholeradius, ndepth, theight, twidth ):
    holeedge = createTurtleEdge()
    holeedge.pieTurn( 0, math.pi*2, nholeradius, (0.0, 0.0), 32 )

    hexedge = createTurtleEdge()
    hexedge.pieTurn( 0, math.pi*2, nheadradius, (0.0, 0.0), 6 )

    outedge = createTurtleEdge()
    outedge.appendEdge( (twidth, twidth ) )
    outedge.appendEdge( (-twidth, twidth ) )
    outedge.appendEdge( (-twidth, -twidth ) )
    outedge.appendEdge( (twidth, -twidth ) )
    outedge.setLoop()

    mstl = create()
    mstl.addSide( 0.0, hexedge.getRevEdge(), ndepth, hexedge.getRevEdge() )
    mstl.addSide( ndepth, holeedge.getRevEdge(), theight, holeedge.getRevEdge() )
    mstl.addSide( 0.0, outedge.getEdge(), theight, outedge.getEdge() )

    return mstl
