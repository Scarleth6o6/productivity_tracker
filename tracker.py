# productivity_tracker/tracker.py
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "time_log.csv"

def start_new_task():
    task_name = input("¿Qué tarea vas a empezar? Ej: 'Estudiar Python', 'MVP Productividad': ")
    
    new_entry = {
        'task_name': task_name,
        'start_time': datetime.now(),
        'end_time': None,
        'duration_min': None
    }
    
    df_new = pd.DataFrame([new_entry])
    
    if os.path.exists(DATA_FILE):
        df_old = pd.read_csv(DATA_FILE)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        df_combined.to_csv(DATA_FILE, index=False)
    else:
        df_new.to_csv(DATA_FILE, index=False)
    
    print(f"✅ ¡Tarea '{task_name}' iniciada a las {new_entry['start_time'].strftime('%H:%M')}!")
    
# Añade esta función
def current_status():
    if not os.path.exists(DATA_FILE):
        print("No hay tareas registradas.")
        return
    
    df = pd.read_csv(DATA_FILE)
    unfinished = df[df['end_time'].isna()]
    
    if unfinished.empty:
        print("No hay tareas activas en este momento.")
    else:
        current_task = unfinished.iloc[-1]
        start_time = pd.to_datetime(current_task['start_time'])
        elapsed = round((datetime.now() - start_time).total_seconds() / 60, 2)
        print(f"📍 Tarea actual: '{current_task['task_name']}'")
        print(f"   Llevas: {elapsed} minutos")

# En el menú principal, añade esta opción:
# print("4. Ver tarea actual")
# Y en las opciones: elif choice == '4': current_status()

# --- NUEVA FUNCIÓN PARA FINALIZAR TAREAS ---
def stop_current_task():
    # Verificar si existe el archivo de datos
    if not os.path.exists(DATA_FILE):
        print("❌ No hay tareas registradas. Inicia una tarea primero.")
        return
    
    # Leer los datos
    df = pd.read_csv(DATA_FILE)
    
    # Encontrar la última tarea sin terminar (end_time vacío)
    unfinished_tasks = df[df['end_time'].isna()]
    
    if unfinished_tasks.empty:
        print("❌ No hay tareas activas. Todas las tareas están completadas.")
        return
    
    # Tomar la última tarea sin terminar
    last_task_index = unfinished_tasks.index[-1]
    task_name = df.loc[last_task_index, 'task_name']
    
    # Registrar hora de finalización
    end_time = datetime.now()
    df.loc[last_task_index, 'end_time'] = end_time
    
    # Calcular duración en minutos
    start_time = pd.to_datetime(df.loc[last_task_index, 'start_time'])
    duration = round((end_time - start_time).total_seconds() / 60, 2)
    df.loc[last_task_index, 'duration_min'] = duration
    
    # Guardar los datos actualizados
    df.to_csv(DATA_FILE, index=False)
    
    print(f"✅ Tarea '{task_name}' finalizada!")
    print(f"   Duración: {duration} minutos")
    print(f"   Hora de fin: {end_time.strftime('%H:%M')}")

def main():
    while True:
        print("\n--- Mi Rastreador de Productividad ---")
        print("1. Iniciar una nueva tarea")
        print("2. Ver tarea actual") 
        print("3. Finalizar la tarea actual ")
        print("4. Salir")
        
        choice = input("Elige una opción (1-4): ")
        
        if choice == '1':
            start_new_task()
        elif choice == '2':
            current_status()
        elif choice == '3':
            stop_current_task()  # ¡Ahora sí funciona!
        elif choice == '4':
            print("¡Hasta luego! Programa terminado.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()