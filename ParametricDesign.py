import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
recLen = gridSize
x = extentX+1 
y = extentY+1

cen=[]
net = []
line=[]
mid=[]
node= []
midLine=[]
for i in range(x):
    for j in range(y):
        net.append(rg.Point3d(i*recLen,j*recLen,0))
        if i==0 or j==0:
            pass
        else:
            line.append(rs.AddLine(rg.Point3d(i*recLen,j*recLen,0),rg.Point3d((i-1)*recLen,j*recLen,0)))
            line.append(rs.AddLine(rg.Point3d(i*recLen,j*recLen,0),rg.Point3d(i*recLen,(j-1)*recLen,0)))
        if i!=x-1 and j!=y-1:
            cen.append(rg.Point3d(i*recLen+recLen/2,j*recLen+recLen/2,0))

for i in cen:
    for j in net:
        if rs.Distance(i,j)<recLen:
            line.append(rs.AddLine(i,j))
            node.append((j-i)*p+i)
for i in net:
    for j in net:
        if rs.Distance(i,j)==recLen:
            mid.append((i+j)/2)
for i in mid:
    for j in node:
        if rs.Distance(i,j)<=recLen/2:
            midLine.append(rs.AddLine(i,j))
rec = rs.AddRectangle(rs.WorldXYPlane(),net[-1].X,net[-1].Y)

lines = midLine+line
diagrid = line