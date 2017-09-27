
nx = 200
ny = 100
f = open('test1.ppm','w')
head = 'P3\n'+ str(nx)+' '+ str(ny)+'\n255\n'
f.write(head)
for j in range(ny-1,-1,-1):
    for i in range(0,nx):
        r = float(i)/nx
        g = float(j)/ny
        b = 0.2
        ir = int(255.99*r)
        ig = int(255.99*g)
        ib = int(255.99*b)
        line = str(ir)+' '+str(ig)+' '+str(ib)+'\n'
        f.write(line)
f.close()