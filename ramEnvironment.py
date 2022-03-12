import simpy
import random

#variables para el funcionamiento del environment
RANDOM_SEED = 0
random.seed(RANDOM_SEED)
CPU_INST = 3
AVAILABLE_CPU = 1
PROCESOS = 25
TIEMPO = 10
UNIDAD = 1
RAM_CAPACITY = 100
INTERVALO = 10

#funcion de los procesos
def procesos(env, nombre, ramCapacidad, ramNeeded, inst_req, tiempo, velocidad):

    #NEW
    yield env.timeout(tiempo)

    tiempoInicial = env.now #Se guarda el tiempo en el que inician los procesos
    print("%s necesita %d de RAM" % (nombre, ramNeeded))
    print("Tiempo en ejecucion: %a" % (tiempo)) #se indica cuanta RAM necesita el proceso creado

    #READY
    yield ramCapacidad.get(ramNeeded)
    print("%s utilizando %d de RAM" % (nombre, ramNeeded))

    inst_rest = inst_req
    inst_utilizadas = 0 #Se inicia la variable que guarda las instrucciones usadas por un proceso

    #RUNNING
    while inst_req > inst_utilizadas: #mientras las instrucciones requeridas sean mayores a las instrucciones usadas por el proceso:
        with cpu.request() as req:
            yield req

            inst_rest = inst_req - inst_utilizadas #instrucciones restantes indican cuantas instrucciones hacen falta del proceso

            if (inst_rest >= velocidad):

                ejecutado = velocidad #ejecutado igual a la velocidad del CPU, la maxima cantidad de instrucciones que puede operar el CPU
            
            else:

                ejecutado = inst_rest #si las instrucciones restantes son menores a 3, el CPU realiza esas instrucciones

            print("Ejecutando %s - El CPU utiliza %d instrucciones" % (nombre, ejecutado))

            yield env.timeout(ejecutado/velocidad)

            inst_utilizadas += ejecutado
            print("Ejecutado %s - Instrucciones utilizadas: (%d de %d)" % (nombre, inst_utilizadas, inst_req)) #indica cuantas instrucciones se han realizado del proceso
        
        waiting = random.randint(1,2)

        if (waiting == 1 and inst_req > inst_utilizadas):
            yield env.timeout(INTERVALO) #entra a la cola de espera

    #TERMINATED
    tiempo = env.now - tiempoInicial
    yield ramCapacidad.put(ramNeeded)
    print("%s ha liberado %d de RAM" % (nombre, ramNeeded))
    print("Tiempo ejecutado: %a" % (tiempo)) #tiempo ejecutado total del proceso

    #Se crea una variable global del tiempo total para poder calcular el promedio de tiempo al final
    global tiempo_total
    tiempo_total += (env.now - tiempoInicial)


#se crea el environment
env = simpy.Environment()
memoria_ram = simpy.Container(env, capacity=RAM_CAPACITY, init=RAM_CAPACITY)
cpu = simpy.Resource(env, capacity=AVAILABLE_CPU)
tiempo_total = 0

#ciclo que se realiza PROCESOS cantidad de veces 
for i in range(PROCESOS):
    ram_neeeded = random.randint(1, 10)
    instrucciones = random.randint(1,10)
    tiempo = random.expovariate(1.0/INTERVALO)

    env.process(procesos(env, "Proceso " + str(i), memoria_ram, ram_neeeded,instrucciones,tiempo,CPU_INST))

env.run()

#Promedio Tiempo
print("Tiempo promedio es de: " + str((tiempo_total/PROCESOS)) + " segundos")

