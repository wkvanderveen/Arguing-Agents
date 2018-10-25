import main
from system import System

DISPLAY = False

SYSTEM = System(DISPLAY)

for i in range(2):
    main.run_simulation(SYSTEM=SYSTEM, DISPLAY=DISPLAY)
