# color parameters
GREY = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (66, 146, 244)
RED = (244, 92, 65)
YELLOW = (244, 211, 65)
GREEN = (151, 244, 65)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

INF = 9999999

N_AGENTS = 30
MAX_TIME = 100

# agent parameters
MONEY = 200.0  # initial money of an agent
MAXPATIENCE = 0.4  # maximum patience an agent has

RANDOM_WALK = 0
SEARCH_AGENT = 1
NEGOTIATE = 2


starting_counter_price = 0.0001

MIN_MAXBUY = 20
MAX_MAXBUY = 30

MIN_MINSELL = 35
MAX_MINSELL = 45

MIN_QUANTITY = 0
MAX_QUANTITY = 10


# Window parameters
RECTDIST = 1  # size of borders between tiles
RECTSIZE = 40  # size of tiles
MAX_UPDATES_PER_S = 10

TILES_X = 15  # number of tiles on each row
TILES_Y = 15  # number of tiles in each column

WIDTH = TILES_X * (RECTDIST + RECTSIZE) + RECTDIST
HEIGHT = TILES_Y * (RECTDIST + RECTSIZE) + RECTDIST

FRUITS=["MANGOES",
        "ORANGES",
        "APPLES",
        "BANANAS",
        "STRAWBERRIES",
        "BLUEBERRIES",
        "TOMATOS",
        "PAPAYAS",
        "PINEAPPLES",
        "GRAPES",
        "LEMONS",
        ]
