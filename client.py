import requests as req
import json

import time, random

from constants import *

agent_id = -1

# GESTIÓN DE LLAMADAS A LOS MÉTODOS DEL SERVIDOR
# ------------------------------------------------------------------------------
def _getState():
    resp = req.get(URL+'/getState')
    return json.loads(resp.text)['state']

def _incorporateAgent():
    resp = req.get(URL+'/newAgent')
    return json.loads(resp.text)['agent_id']

def _setNumber(value):
    global agent_id

    data = {'agent_id': agent_id, 'value': value}
    req.get(URL+'/setNumber', params=data)

def _invalidateChoice():
    global agent_id

    data = {'agent_id': agent_id}
    req.get(URL+'/clearNumber', params=data)

def _getChosenNumber():
    resp = req.get(URL+'/getChosenNumber')
    return json.loads(resp.text)['chosen_number']

# AUXILIAR
# ------------------------------------------------------------------------------
def _waitStateChange(state):
    while _getState() == STATE[state]:
        time.sleep(WAIT_TIME) # Espera activa

# MAIN
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    print("BEGIN")

    # Comprobamos el estado del servidor
    if _getState() == STATE['BEGIN']:

        # Notificamos al servidor de la llegada de un nuevo agente
        agent_id = _incorporateAgent()
        print("  ID asignada:", agent_id)

        # Esperamos a que se incorporen todos los agentes
        print("    Esperando al resto de agentes...")
        _waitStateChange('BEGIN')

        # Mientras no haya consenso entre agentes
        while _getState() != STATE['CONSENSUS']:

            print("  Pensando un número...")
            time.sleep(random.uniform(THINK_MIN_TIME, THINK_MAX_TIME))

            value = random.randint(MIN_NUMBER, MAX_NUMBER)
            print("  Elijo el número", value)

            # Comunica el número escogido al servidor
            _setNumber(value)

            # Esperamos a que todos los agentes hagan su elección
            print("    Esperando la elección del resto de agentes...")
            _waitStateChange('CHOOSING')

            # Gestionamos en caso de no haber llegado a un consenso
            if _getState() == STATE['REPEAT']:
                print("  No se ha llegado a un consenso. Hay que elegir de nuevo.")
                _invalidateChoice()

                # Espera a que todos los agentes hayan invalidado su elección
                # antes de repetir la elección
                print("    Esperando al resto de agentes...")
                _waitStateChange('REPEAT')

                print("  Repitiendo la elección.\n")

        # Ha habido consenso, imprimimos el número seleccionado
        chosen_num = _getChosenNumber()
        print("  Se ha llegado a un consenso.")
        print("  El número elegido es el", chosen_num)

    else:
        print("  No se permite involucrar a más agentes en la elección")

    print("END")
