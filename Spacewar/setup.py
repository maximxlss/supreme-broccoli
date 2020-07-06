from cx_Freeze import setup, Executable

base = None    

executables = [Executable("game.py", base=base)]

packages = ["pygame", "time", "numpy", "math", "random", "physics"]
options = {
    'build_exe': {
        'packages':packages,
    },    
}

setup(
    name = "Spacewar demo",
    options = options,
    version = "0.1",
    description = 'fdsklafjurnive',
    executables = executables
)