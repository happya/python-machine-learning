class PartyAnimal:
    x=0
    def party(self):
        self.x=self.x+1
        print "OK",self.x

an=PartyAnimal()

an.party()
an.party()
print "Type: ",type(an)
print 'Dir: ',dir(an)

an.