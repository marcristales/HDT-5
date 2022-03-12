from curses import flash
import simpy

CPU_INST = 3
AVAILABLE_CPU = 1
PROCESOS = 50
TIEMPO = 10
UNIDAD = 1
RAM_CAPACITY = 100




def procesos(env, nombre, ramCapacidad, ramNeeded, inst_req, tiempo, velocidad):

    #NEW
    yield env.timeout(tiempo)

    tiempoInicial = env.now
    print("%p necesita %c de RAM" % (nombre, ramNeeded))
    
