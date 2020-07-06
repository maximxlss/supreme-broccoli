from customFuncs import *

class worker():
    def __init__(self, game, name, level=1, price=1, eff=1, speed=None,
                 lv_type=lv_multiply, price_type=price_multiply, **kwargs):
        self.game = game
        self.name = name
        self.level = level
        self.eff = eff
        self.bought = False
        if speed is None:
            speed = game.speed
        self.speed = speed
        self.lv_type = lv_type
        self.price_type = price_type
        self.price = price
        if kwargs == {} and (lv_type is lv_multiply or price_type is price_multiply):
            kwargs = {"lv_multiplier" : 1.5, "price_multiplier" : 4} 
        self.kwargs = kwargs
        
    def levelUp(self):
        self.lv_type(self)
        self.level += 1
        self.price_type(self)
        try:
            self.game.kwargs["levelUp_callback"](self.game)
        except KeyError:
            pass
    
    def update(self):
        self.game.money += int(self.eff)
        try:
            self.game.kwargs["update_callback"](self.game)
        except KeyError:
            pass
        try:
            self.game.kwargs["money_update_callback"](self.game)
        except KeyError:
            pass

def bp():
    breakpoint

class game():
    def __init__(self, speed=1, workerList=None,  
                 clickWorker=None, **kwargs):
        self.money = 0
        self.speed = speed
        self.workerList = workerList
        if self.workerList is None:
            self.workerList = [worker(self, "click"), worker(self, "test2"), worker(self, "test3")] # TODO: make support for custom workers
        self.clickWorker = clickWorker
        if self.clickWorker is None:
            self.clickWorker = self.workerList[0]
        self.workers = [self.clickWorker]
        self.kwargs = kwargs
    
    def update(self):
        for worker in self.workers[1:]:
            worker.update()
        try:
            self.kwargs["global_update_callback"](self)
        except KeyError:
            pass
        try:
            self.kwargs["money_update_callback"](self)
        except KeyError:
            pass
    
    def click(self):
        self.clickWorker.update()
    
    def buy(self, id, click=False):
        if self.money >= self.workerList[id].price:
            if self.workerList[id] not in self.workers:
                self.workers.append(self.workerList[id])
                self.workerList[id].bought = True
                self.money -= self.workerList[id].price
                try:
                    self.kwargs["new_worker_callback"](self, self.workerList[id])
                except KeyError:
                    pass
                try:
                    self.kwargs["money_update_callback"](self)
                except KeyError:
                    pass
            else:
                self.money -= self.workerList[id].price
                self.workerList[id].levelUp()
                try:
                    self.kwargs["money_update_callback"](self)
                except KeyError:
                    pass
        else:
            try:
                self.kwargs["not_enough_money_callback"](self, self.workerList[id])
            except KeyError:
                pass
