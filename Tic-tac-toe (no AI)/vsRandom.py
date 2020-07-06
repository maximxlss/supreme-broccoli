from game import game

instance = game()
while 1:
    instance.readMove()
    instance.render()
    state = instance.checkBoard()
    if state == True:
        print("\033[31m\033[43m    " + ("x" if instance.turn == 2 else "o") + " won!    \033[0m")
        instance.reset()
        instance.render()
        continue
    elif state == "tie":
        print("\033[31m\033[43m    Tie!    \033[0m")
        instance.reset()
        instance.render()
        continue

    instance.randMove()
    instance.render()
    state = instance.checkBoard()
    if state == True:
        print("\033[31m\033[43m    " + ("x" if instance.turn == 2 else "o") + " won!    \033[0m")
        instance.reset()
        instance.render()
        continue
    elif state == "tie":
        print("\033[31m\033[43m    Tie!    \033[0m")
        instance.reset()
        instance.render()
        continue
