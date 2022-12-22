# CONSTANTES
# ------------------------------------------------------------------------------
# Constantes accesibles desde el lado del cliente y desde el lado del servidor.

# Server side
HOST = '127.0.0.1'
PORT = '5000'
URL = 'http://'+HOST+':'+PORT

NUM_AGENTS = 3

STATE = {'BEGIN': 0, 'CHOOSING': 1, 'REPEAT': 2, 'CONSENSUS': 3} # Enumerado

# Client side
THINK_MIN_TIME, THINK_MAX_TIME = 1., 5. # time interval to think new number
MIN_NUMBER, MAX_NUMBER = 1, 10          # number choice interval

WAIT_TIME = 2 # time to wait before resending a state request

