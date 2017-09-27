
import numpy as np
class Vec3():
    def __init__(self,e):
        self.e = np.array(e)
        self.x = self.e[0]
        self.y = self.e[1]
        self.z = self.e[2]
        self.r = self.e[0]
        self.g = self.e[1]
        self.b = self.e[2]
        self.length = np.sqrt(np.dot(self.e,self.e))

    def __add__(self, v1):
        return Vec3(v1.e+self.e)
    def __sub__(self,v1):
        return Vec3(self.e-v1.e)
    def mul_c(self,v1):
        if isinstance(v1,Vec3):
            return Vec3(self.e*v1.e)
        elif isinstance(v1,(float,int)):
            return Vec3(self.e*float(v1))
    def div_c(self,v1):
        return self.e/v1.e
    def dot_c(self,v1):
        return np.dot(self.e,v1.e)
    def cross_c(self,v1):

        return Vec3((self.e[1]*v1.e[2]-self.e[2]*v1.e[1]),\
                             (-self.e[0]*v1.e[2]+self.e[2]*v1.e[0]),\
                             (self.e[0]*v1.e[1]-self.e[1]*v1.e[0]))

    def unit_v(self):
        return Vec3(self.e/self.length)

nx = 200
ny = 100
f = open('test_vec3.ppm','w')
head = 'P3\n'+ str(nx)+' '+ str(ny)+'\n255\n'
f.write(head)
for j in range(ny-1,-1,-1):
    for i in range(0,nx):
        col = Vec3([float(i)/nx,float(j)/ny,0.2])
        ir = int(255.99*col.e[0])
        ig = int(255.99*col.e[1])
        ib = int(255.99*col.e[2])
        line = str(ir)+' '+str(ig)+' '+str(ib)+'\n'
        f.write(line)
f.close()

