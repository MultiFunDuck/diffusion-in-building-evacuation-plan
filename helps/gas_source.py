class gas_source:

    def __init__(self, x, y, len, power):
        self.x = x
        self.y = y
        self.len = len
        self.power = power


    def dist_from_src(self, x, y):
        dx = self.x - x
        dy = self.y - y
        return (dx*dx + dy*dy)

    
    def contain(self, x, y):
        return (x - self.x)*(x - self.x) + (y - self.y)*(y - self.y) <= self.len*self.len