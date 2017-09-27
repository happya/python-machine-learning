from vec3 import *

class ray():
    def __init__(self,v1,v2):
        self.A = v1
        self.B = v2
        self.origin = self.A
        self.direc = self.B

    def point_at_para(self,t):
        return self.A + t*self.B

def color(r):
    unit_dir = r.direc.unit_v()
    #print "unit: ",unit_dir.e
    t = float(0.5*unit_dir.y+1.0)
    return Vec3([1.0,1.0,1.0]).mul_c(1.0-t)+Vec3([0.5,0.7,1.0]).mul_c(t)

nx = 200
ny = 100
f = open('test2.ppm','w')
head = 'P3\n'+ str(nx)+' '+ str(ny)+'\n255\n'
f.write(head)
lower_left_corner = Vec3([-2.0,-1.0,-1.0])
hori = Vec3([4.0,0.0,0.0])
vert = Vec3([0.0,2.0,0.0])
orig = Vec3([0.0,0.0,0.0])

for j in range(ny-1,-1,-1):
    for i in range(0,nx):
        u = float(i)/nx
        v = float(j)/ny
        r = ray(orig,lower_left_corner+hori.mul_c(u)+vert.mul_c(v))
        col = color(r)
        ir = int(255.99*col.e[0])
        ig = int(255.99*col.e[1])
        ib = int(255.99*col.e[2])
        line = str(ir)+' '+str(ig)+' '+str(ib)+'\n'
        f.write(line)
f.close()