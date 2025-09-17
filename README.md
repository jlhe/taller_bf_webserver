
# Buscador de Directorios por Fuerza Bruta

Este script es una herramienta educativa diseñada para talleres de seguridad web. Su objetivo es demostrar cómo un atacante puede descubrir directorios "ocultos" en un servidor web mediante un ataque de fuerza bruta dirigido.

La herramienta está optimizada para ser rápida y eficiente, utilizando concurrencia para enviar múltiples peticiones simultáneamente.

## Características

*   **Rápido y Concurrente**: Utiliza un `ThreadPoolExecutor` para realizar múltiples peticiones HTTP en paralelo, acelerando significativamente el proceso de búsqueda.
*   **Búsqueda Dirigida**: Configurado para buscar combinaciones específicas (por defecto, 4 letras mayúsculas) en lugar de una fuerza bruta ciega, lo que lo hace ideal para escenarios de taller con pistas.
*   **Feedback Visual**: Incluye una barra de progreso (`tqdm`) que muestra el estado de la búsqueda en tiempo real, la velocidad de las peticiones y el tiempo estimado.
*   **Robusto**: Maneja errores de conexión y timeouts para evitar que el script se detenga inesperadamente.
*   **Fácil de Configurar**: Las variables principales como la URL objetivo, la longitud de la palabra y los hilos de trabajo se encuentran en la parte superior del script para una fácil modificación.

## Requisitos

*   Python 3.6+
*   Librerías externas: `requests`, `tqdm`

### Archivo `requirements.txt`

Crea un archivo llamado `requirements.txt` en el mismo directorio que el script con el siguiente contenido:

```txt
requests
tqdm
```

## Instalación

Sigue estos pasos para configurar tu entorno y poder ejecutar el script.

1.  **Clona o descarga el script** en un directorio de tu elección.

2.  **Abre una terminal** y navega a ese directorio.

3.  **(Recomendado) Crea un entorno virtual** para aislar las dependencias del proyecto:
    ```bash
    python -m venv venv
    ```

4.  **Activa el entorno virtual**:
    *   En **Windows**:
        ```bash
        .\venv\Scripts\activate
        ```
    *   En **macOS / Linux**:
        ```bash
        source venv/bin/activate
        ```

5.  **Instala las dependencias** usando el archivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración del Script

Antes de ejecutar el script, ábrelo (`directory_finder.py`) y modifica la siguiente variable para que apunte a la aplicación web de tu taller:

```python
# --- Configuración del Taller ---
# Modifica esta URL para que apunte al servidor local de tu taller.
# Asegúrate de que no tenga la barra final '/'.
BASE_URL = "http://127.0.0.1:8000" 
```

Puedes también ajustar `WORD_LENGTH`, `CHARACTERS` y `MAX_WORKERS` según las necesidades del ejercicio.

## Ejecución

Una vez que el entorno esté configurado y el script ajustado, simplemente ejecuta el siguiente comando en tu terminal:

```bash
python directory_finder.py
```

El script comenzará a probar todas las combinaciones posibles y te notificará en cuanto encuentre un directorio que devuelva un código de estado `200 OK`.

### Ejemplo de Salida

```
[*] Iniciando búsqueda de directorio en: http://127.0.0.1:8000
[*] Configuración: 4 caracteres, mayúsculas. Usando 20 hilos.
[*] Total de combinaciones a probar: 456976
Buscando:  15%|█▌        | 69420/456976 [00:05<00:31, 12450.84it/s]

[+] ¡ÉXITO! Directorio encontrado: http://127.0.0.1:8000/DATA
```

---

### **Descargo de Responsabilidad**

Esta herramienta ha sido creada con fines estrictamente educativos. Utilízala únicamente en entornos controlados y sobre aplicaciones de las que tengas permiso explícito para auditar. El uso de esta herramienta contra sistemas sin autorización es ilegal.