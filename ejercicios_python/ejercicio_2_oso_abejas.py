"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.4 (Sincronización con semáforos)
"""

import sys
import threading
import time
import random

# Configuración UTF-8 para consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10                  # Capacidad del tarro de miel
NUM_ABEJAS = 5          # Número de abejas obreras
tarro_miel = 0          # Variable compartida
simulacion_activa = True

# TODO PARA EL ESTUDIANTE:
# 1. Define los mecanismos de sincronización necesarios:
# - Un cerrojo (Lock) o semáforo binario para exclusión mutua en el tarro.
# - Un semáforo para despertar al oso cuando el tarro esté lleno.
# - Un semáforo para que las abejas esperen si el tarro está lleno o el oso está comiendo.
mutex = threading.Lock()
sem_oso = threading.Semaphore(0)
sem_tarro_disponible = threading.Semaphore(1)

def abeja(id_abeja):
    global tarro_miel, simulacion_activa
    while simulacion_activa:
        time.sleep(random.uniform(0.05, 0.2))
        
        # TODO: Sincronizar el acceso al tarro de miel:
        # 1. Esperar a que el tarro esté disponible. 
        sem_tarro_disponible.acquire()
        # 2. Entrar en exclusión mutua con el tarro.
        with mutex:
            print("La abeja entró en exclusion mutua con el tarro de miel")
        # 3. Depositar una porción de miel (tarro_miel += 1).
            tarro_miel += 1
            print("Se deposita porcion de miel")
            print(f"tarro de miel: {tarro_miel}")
        # 4. Si tarro_miel == M, avisar/despertar al oso dormido.
            if tarro_miel == M :
                print("Tarro de miel lleno, DESPERTAR AL OSO")
                sem_oso.release()
        # 5. Si no está lleno, permitir que otras abejas sigan produciendo.
            else:
                print("entro")
                sem_tarro_disponible.release()
        pass

def oso(max_tarros=2):
    global tarro_miel, simulacion_activa
    tarros_comidos = 0
    while tarros_comidos < max_tarros and simulacion_activa:
        # =====================================================================
        # TODO PARA EL ESTUDIANTE:
        # 1. Esperar pasivamente (bloqueado) hasta que una abeja señale que el tarro está lleno:
        sem_oso.acquire()
        print("Oso despierto")
        # 2. Comerse toda la miel (tarro_miel = 0).
        with mutex:
            print("Oso entra en exclusion mutua para comer")
            tarro_miel = 0
        # 3. Incrementar tarros_comidos += 1.
            tarros_comidos += 1
            print(f"Tarro de miel comidos por el oso: {tarros_comidos}")
        # 4. Avisar a las abejas que el tarro está vacío y disponible (sem_tarro_disponible.release()).
        print("Tarro de miel vacio, avisar a las abejas")
        sem_tarro_disponible.release()
        # =====================================================================
        pass
        time.sleep(0.05)
        #break  # Evita bucle infinito si el alumno no implementó el TODO
        
    simulacion_activa = False

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)
    # TODO: Crear e iniciar los hilos para el oso y las N abejas
    hilo_oso = threading.Thread(target=oso, args=(2,)); 
    hilo_oso.start()
    hilos_abejas = []
    for i in range(NUM_ABEJAS):
        hilos_abejas = threading.Thread(target=abeja, args=(i + 1,))
        #hilos_abejas.daemon = True  # Para asegurar que finalicen cuando el programa concluya
        hilos_abejas.start()
    pass

