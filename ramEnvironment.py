import simpy
import random

CPU_INST = 3
AVAILABLE_CPU = 1
PROCESOS = 25
TIEMPO = 10
UNIDAD = 1
RAM_CAPACITY = 100
INTERVALO = 10


def procesos(env, nombre, ramCapacidad, ramNeeded, inst_req, tiempo, velocidad):

    #NEW
    yield env.timeout(tiempo)

    tiempoInicial = env.now
    print("%s necesita %d de RAM" % (nombre, ramNeeded))
    print("Tiempo en ejecucion: %a" % (tiempo))

    #READY
    yield ramCapacidad.get(ramNeeded)
    print("%s utilizando %d de RAM" % (nombre, ramNeeded))

    next_inst = inst_req
    inst_utilizadas = 0

    #RUNNING
    while inst_req > inst_utilizadas:
        with cpu.request() as req:
            yield req

            next_inst = inst_req - inst_utilizadas

            if (next_inst >= velocidad):

                ejecutado = velocidad
            
            else:

                ejecutado = next_inst

            print("Ejecutando %s - El CPU utiliza %d instrucciones" % (nombre, ejecutado))

            yield env.timeout(ejecutado/velocidad)

            inst_utilizadas += ejecutado
            print("Ejecutado %s - Instrucciones utilizadas: (%d/%d)" % (nombre, inst_utilizadas, inst_req))
        
        waiting = random.randint(1,2)

        if (waiting == 1 and inst_req > inst_utilizadas):
            yield env.timeout(INTERVALO)

    tiempo = env.now - tiempoInicial
    yield ramCapacidad.put(ramNeeded)
    print("%s ha liberado %d de RAM" % (nombre, ramNeeded))
    print("Tiempo ejecutado: %a" % (tiempo))

env = simpy.Environment()
memoria_ram = simpy.Container(env, capacity=RAM_CAPACITY, init=RAM_CAPACITY)
cpu = simpy.Resource(env, capacity=AVAILABLE_CPU)

for i in range(PROCESOS):
    ram_neeeded = random.randint(1, 10)
    instrucciones = random.randint(1,10)
    tiempo = random.expovariate(1.0/INTERVALO)

    env.process(procesos(env, "Proceso " + str(i), memoria_ram, ram_neeeded,instrucciones,tiempo,CPU_INST))

env.run()


