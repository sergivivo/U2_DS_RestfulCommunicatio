from flask import Flask, request, jsonify

import random
from functools import reduce

from constants import *

# VARIABLES
# ------------------------------------------------------------------------------
app = Flask(__name__)

agents = 0 # cuenta los agentes incorporados

numbers = [] # números elegidos por cada agente
choice = []  # array de booleanos, indica si se trata de una elección actualizada

# Gestión de estados y número elegido por consenso
state = STATE['BEGIN']
chosen_num = None

# MÉTODOS
# ------------------------------------------------------------------------------
@app.get("/getState")
def get_state():
    global state
    return jsonify({'state': state}), 200

@app.get("/newAgent")
def new_agent():
    global agents, numbers, choice, state

    # Sólo permitir incorporar nuevos agentes en el estado BEGIN
    if state != STATE['BEGIN']:
        return 'Current state does not allow new agents.\n', 405

    agent_id = agents
    agents += 1

    numbers.append(None)
    choice.append(False)

    # Cuando se hayan incorporado todos los agentes, comenzar la elección
    if agents == NUM_AGENTS:
        state = STATE['CHOOSING']

    # Devolver la ID asignada al agente
    return jsonify({'agent_id': agent_id}), 201

@app.get("/setNumber")
def set_number():
    global numbers, choice

    agent_id = int(request.args.get('agent_id'))
    value = int(request.args.get('value'))

    # Los agentes acceden vía ID a su índice correspondiente
    numbers[agent_id] = value
    choice[agent_id] = True

    # Comprueba que todos los agentes hayan elegido su número
    all_choose = reduce(lambda acc, val: acc and val, choice, True)
    if all_choose:
        _checkConsensus()

    return jsonify({'agent_id': agent_id, 'value': value}), 201

@app.get("/clearNumber")
def clear_number():
    global state, choice

    # Es importante exigir que sean los agentes los que anulen su número,
    # pues es necesario sincronizarlos antes de repetir la elección.

    agent_id = int(request.args.get('agent_id'))
    choice[agent_id] = False

    # Comprueba que todos los agentes hayan restablecido su elección
    all_reset = reduce(lambda acc, val: acc and not val, choice, True)
    print(all_reset)
    if all_reset:
        state = STATE['CHOOSING'] # Regresa al estado de elección

    return jsonify({'agent_id': agent_id}), 201

def _checkConsensus():
    global numbers, state, chosen_num

    # Cuenta las ocurrencias de cada número elegido
    count = {}
    for e in numbers:
        if e in count:
            count[e] += 1
        else:
            count[e] = 1

    # Obtiene la clave y el valor más grande
    max_key = max(count, key=count.get)
    max_count = count[max_key]

    # Comprueba mayoría absoluta
    if max_count > NUM_AGENTS/2:
        # Consenso
        chosen_num = max_key
        state = STATE['CONSENSUS']
    else:
        # No consenso, se repite la elección
        state = STATE['REPEAT']

@app.get("/getChosenNumber")
def get_chosen_number():
    global state, chosen_num

    # Al finalizar la elección y haber consenso, permite a los agentes conocer
    # el número que ha salido seleccionado.

    if state == STATE['CONSENSUS']:
        return jsonify({'chosen_number': chosen_num}), 200

    return "Consensus was still not reached.\n", 405

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)

