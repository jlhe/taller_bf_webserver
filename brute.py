import requests
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import string

BASE_URL = "http://51.222.25.88"

# Pista: Sabemos que el directorio tiene 4 caracteres y son letras mayúsculas.
WORD_LENGTH = 5
CHARACTERS = string.ascii_uppercase  # Genera 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Número de hilos para ejecutar en paralelo. Un buen punto de partida es 10-50.
# Un número mayor no siempre es más rápido debido a la sobrecarga y los límites de la red.
MAX_WORKERS = 20

# --- Fin de la Configuración ---

def check_directory(directory_name):
    """
    Construye una URL y comprueba si devuelve un código de estado 200.
    
    Args:
        directory_name (str): El nombre del directorio a probar.
        
    Returns:
        str: La URL completa si se encuentra (código 200), de lo contrario None.
    """
    try:
        # Construimos la URL completa a probar
        test_url = f"{BASE_URL}/{directory_name}"
        
        # Añadimos un User-Agent para simular un navegador real.
        # Esto hace que la petición sea menos "obvia" para firewalls o logs básicos.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0'
        }
        
        # Hacemos la petición GET. Usamos un timeout para no quedarnos esperando indefinidamente.
        # `allow_redirects=False` es útil para que un 301/302 a una página de "login" no cuente como éxito.
        response = requests.get(test_url, headers=headers, timeout=5, allow_redirects=False)
        
        # ¡Éxito! Si el código es 200, hemos encontrado el directorio.
        if response.status_code == 200:
            return test_url
            
    except requests.exceptions.RequestException:
        # Ignoramos errores de conexión, timeouts, etc.
        pass
        
    return None

def main():
    """
    Función principal que orquesta la generación de palabras y la ejecución concurrente.
    """
    print(f"[*] Iniciando búsqueda de directorio en: {BASE_URL}")
    print(f"[*] Configuración: {WORD_LENGTH} caracteres, mayúsculas. Usando {MAX_WORKERS} hilos.")

    # 1. Generar todas las combinaciones posibles
    # 'itertools.product' es extremadamente eficiente para esto.
    # Creamos una lista para poder obtener el total de combinaciones para la barra de progreso.
    possible_dirs = [''.join(p) for p in itertools.product(CHARACTERS, repeat=WORD_LENGTH)]
    total_combinations = len(possible_dirs)
    print(f"[*] Total de combinaciones a probar: {total_combinations}")

    found_url = None

    # 2. Usar ThreadPoolExecutor para ejecutar las peticiones en paralelo
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Creamos un diccionario de 'futuros' para poder obtener el resultado cuando terminen
        future_to_dir = {executor.submit(check_directory, directory): directory for directory in possible_dirs}
        
        # 3. Procesar los resultados a medida que se completan
        # tqdm nos dará una bonita barra de progreso
        for future in tqdm(as_completed(future_to_dir), total=total_combinations, desc="Buscando"):
            result = future.result()
            if result:
                print(f"\n[+] ¡ÉXITO! Directorio encontrado: {result}")
                found_url = result
                # Una vez encontrado, cancelamos las tareas pendientes para terminar rápido.
                executor.shutdown(wait=False, cancel_futures=True)
                break
    
    if not found_url:
        print("\n[-] Búsqueda completada. No se encontró ningún directorio con los parámetros dados.")

if __name__ == "__main__":
    main()