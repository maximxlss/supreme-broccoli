import math

def lv_multiply(self, predict=None):
    if predict is not None:
        feff = self.eff
        for _ in range(predict):
            feff *= self.kwargs["price_multiplier"]
            feff = math.ceil(feff)
        return feff
    else:
        self.eff *= self.kwargs["lv_multiplier"] * self.speed
        self.eff = math.ceil(self.eff)

def price_multiply(self, predict=None):
    if predict is not None:
        fprice = self.price
        for _ in range(predict):
            fprice *= self.kwargs["price_multiplier"]
            fprice = math.ceil(fprice)
        return fprice
    else:
        self.price *= self.kwargs["price_multiplier"]
        self.price = math.ceil(self.price)