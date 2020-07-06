import os

if inp := input("Крестики-нолики - 1\nЗмейка - 2\nSpacewar - 3\nКликер - 4") == "1":
  os.system('python3 "Tic-tac-toe (no AI)/vsRandom.py"')
elif inp == "2":
  os.system('python3 "Snake/launcher.py"')
elif inp == "3":
  os.system('python3 "Spacewar/game.py"')
elif inp == "4":
  os.system('python3 "Clicker/example.py"')