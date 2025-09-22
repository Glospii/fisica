# Importación de librerías
import numpy as np  # Para operaciones numéricas y creación de arrays
import matplotlib.pyplot as plt  # Para crear gráficos y visualizaciones
from matplotlib.animation import FuncAnimation  # Para crear animaciones
import math  # Para funciones matemáticas como sqrt

# Definición de constantes
GRAVEDAD_TIERRA = 9.8  # m/s² - Aceleración gravitacional en la Tierra
GRAVEDAD_LUNA = 1.625  # m/s² - Aceleración gravitacional en la Luna

def calcular_altura_maxima(altura_inicial, velocidad_inicial, gravedad):
    """
    Calcula la altura máxima alcanzada por el objeto utilizando ecuaciones de movimiento uniformemente acelerado.
    
    Parámetros:
    altura_inicial (float): Altura inicial en metros desde la superficie
    velocidad_inicial (float): Velocidad inicial en m/s (positiva hacia arriba)
    gravedad (float): Aceleración de la gravedad en m/s² (siempre positiva)
    
    Retorna:
    float: Altura máxima alcanzada en metros
    """
    # Si la velocidad inicial es negativa o cero, el objeto no sube
    if velocidad_inicial <= 0:
        return altura_inicial  # La altura máxima es la posición inicial
    
    # Fórmula física: h_max = y0 + (v0²)/(2*g)
    # Donde:
    # y0 = altura inicial
    # v0 = velocidad inicial
    # g = aceleración gravitacional
    altura_maxima = altura_inicial + (velocidad_inicial**2) / (2 * gravedad)
    return altura_maxima

def calcular_tiempo_altura_maxima(velocidad_inicial, gravedad):
    """
    Calcula el tiempo que tarda en alcanzar la altura máxima (punto donde velocidad=0).
    
    Parámetros:
    velocidad_inicial (float): Velocidad inicial en m/s
    gravedad (float): Aceleración de la gravedad en m/s²
    
    Retorna:
    float: Tiempo hasta altura máxima en segundos
    """
    # Si la velocidad inicial es negativa o cero, nunca alcanza altura máxima
    if velocidad_inicial <= 0:
        return 0.0  # El objeto comienza a descender inmediatamente
    
    # Fórmula física: t_max = v0 / g
    # Donde la velocidad se hace cero: v0 - g*t = 0
    tiempo_maximo = velocidad_inicial / gravedad
    return tiempo_maximo

def calcular_velocidad_tiempo(velocidad_inicial, gravedad, tiempo):
    """
    Calcula la velocidad instantánea en un tiempo específico usando la ecuación de velocidad.
    
    Parámetros:
    velocidad_inicial (float): Velocidad inicial en m/s
    gravedad (float): Aceleración de la gravedad en m/s²
    tiempo (float): Tiempo transcurrido en segundos
    
    Retorna:
    float: Velocidad en el tiempo especificado (positiva hacia arriba, negativa hacia abajo)
    """
    # Fórmula física: v(t) = v0 - g*t
    # Signo negativo porque la gravedad actúa en dirección opuesta al movimiento ascendente
    velocidad = velocidad_inicial - gravedad * tiempo
    return velocidad

def calcular_altura_tiempo(altura_inicial, velocidad_inicial, gravedad, tiempo):
    """
    Calcula la posición vertical (altura) en un instante de tiempo determinado.
    
    Parámetros:
    altura_inicial (float): Altura inicial en metros
    velocidad_inicial (float): Velocidad inicial en m/s
    gravedad (float): Aceleración de la gravedad en m/s²
    tiempo (float): Tiempo transcurrido en segundos
    
    Retorna:
    float: Altura en el tiempo especificado en metros
    """
    # Fórmula física: y(t) = y0 + v0*t - 0.5*g*t²
    # Término cuadrático representa el efecto de la aceleración constante
    altura = altura_inicial + velocidad_inicial * tiempo - 0.5 * gravedad * tiempo**2
    return altura

def calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, gravedad):
    """
    Calcula el tiempo total de vuelo hasta que el objeto impacta el suelo (y=0).
    Resuelve la ecuación cuadrática del movimiento.
    
    Parámetros:
    altura_inicial (float): Altura inicial en metros
    velocidad_inicial (float): Velocidad inicial en m/s
    gravedad (float): Aceleración de la gravedad en m/s²
    
    Retorna:
    float: Tiempo total de vuelo en segundos o infinito si nunca impacta
    """
    # Caso especial: si no hay gravedad (entorno sin aceleración)
    if gravedad == 0:
        if velocidad_inicial == 0:
            return float('inf')  # Permanece flotando a altura constante
        else:
            # Movimiento rectilíneo uniforme
            if altura_inicial > 0:
                return abs(altura_inicial / velocidad_inicial)  # Tiempo para recorrer distancia
            else:
                return 0  # Ya está en el suelo
    
    # Ecuación cuadrática general: 0.5*g*t² - v0*t - y0 = 0
    # Forma estándar: a*t² + b*t + c = 0
    a = -0.5 * gravedad  # Coeficiente cuadrático
    b = velocidad_inicial  # Coeficiente lineal
    c = altura_inicial  # Término independiente
    
    # Cálculo del discriminante para determinar existencia de raíces reales
    discriminante = b**2 - 4*a*c
    
    # Si el discriminante es negativo, no hay soluciones reales
    if discriminante < 0:
        return float('inf')  # El objeto nunca alcanza y=0
    
    # Fórmula cuadrática para encontrar raíces
    t1 = (-b + math.sqrt(discriminante)) / (2*a)
    t2 = (-b - math.sqrt(discriminante)) / (2*a)
    
    # Filtrar solo tiempos positivos (físicamente meaningful)
    tiempos = [t for t in [t1, t2] if t >= 0]
    
    # Si no hay tiempos positivos, el objeto nunca cae
    if not tiempos:
        return float('inf')
    
    # Devolver el mayor tiempo positivo (cuando impacta después de subir y bajar)
    return max(tiempos)

def animar_tiro_vertical(altura_inicial, velocidad_inicial, gravedad):
    """
    Crea una animación gráfica del movimiento de tiro vertical.
    Utiliza matplotlib.animation para crear frames sucesivos.
    
    Parámetros:
    altura_inicial (float): Altura inicial en metros
    velocidad_inicial (float): Velocidad inicial en m/s
    gravedad (float): Aceleración de la gravedad en m/s²
    """
    # Calcular tiempo total de vuelo para determinar duración de animación
    tiempo_vuelo = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, gravedad)
    
    # Si el tiempo es infinito, usar un valor default para visualización
    if tiempo_vuelo == float('inf'):
        tiempo_vuelo = 10  # 10 segundos por defecto para visualización
    
    # Crear array de 100 puntos temporales equidistantes
    tiempos = np.linspace(0, tiempo_vuelo, 100)
    
    # Calcular la altura para cada punto temporal
    alturas = [calcular_altura_tiempo(altura_inicial, velocidad_inicial, gravedad, t) for t in tiempos]
    
    # Configurar la figura y ejes del gráfico
    fig, ax = plt.subplots()
    ax.set_xlim(0, 2)  # Rango fijo en eje X para visualización
    ax.set_ylim(0, max(max(alturas), altura_inicial) * 1.1)  # Rango en Y con margen
    ax.set_xlabel('Posición X (m)')  # Etiqueta eje X
    ax.set_ylabel('Altura (m)')  # Etiqueta eje Y
    ax.set_title('Animación de Tiro Vertical')  # Título
    ax.grid(True)  # Activar grid para mejor referencia visual
    
    # Crear punto rojo que representará el objeto en movimiento
    punto, = ax.plot([1], [altura_inicial], 'ro', markersize=10)
    
    # Función de inicialización para la animación
    def init():
        punto.set_data([1], [altura_inicial])  # Posición inicial
        return punto,  # Devolver tuple con elementos a animar
    
    # Función de animación que se llama para cada frame
    def animate(i):
        if i < len(tiempos):
            punto.set_data([1], [alturas[i]])  # Actualizar posición
        return punto,  # Devolver tuple con elementos actualizados
    
    # Crear animación con:
    # - fig: figura donde se dibuja
    # - animate: función que actualiza cada frame
    # - init_func: función de inicialización
    # - frames: número de frames (puntos temporales)
    # - interval: tiempo entre frames en milisegundos
    # - blit: optimización para redibujar solo elementos cambiados
    anim = FuncAnimation(fig, animate, init_func=init,
                         frames=len(tiempos), interval=50, blit=True)
    
    # Mostrar la animación
    plt.show()

def comparar_tierra_luna(altura_inicial, velocidad_inicial):
    """
    Compara cuantitativamente el movimiento entre Tierra y Luna.
    Muestra diferencias en altura máxima, tiempos y velocidades.
    
    Parámetros:
    altura_inicial (float): Altura inicial en metros
    velocidad_inicial (float): Velocidad inicial en m/s
    """
    print("\n=== COMPARACIÓN TIERRA vs LUNA ===")
    
    # Calcular resultados para la Tierra
    hmax_tierra = calcular_altura_maxima(altura_inicial, velocidad_inicial, GRAVEDAD_TIERRA)
    tmax_tierra = calcular_tiempo_altura_maxima(velocidad_inicial, GRAVEDAD_TIERRA)
    tvuelo_tierra = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, GRAVEDAD_TIERRA)
    
    # Calcular resultados para la Luna
    hmax_luna = calcular_altura_maxima(altura_inicial, velocidad_inicial, GRAVEDAD_LUNA)
    tmax_luna = calcular_tiempo_altura_maxima(velocidad_inicial, GRAVEDAD_LUNA)
    tvuelo_luna = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, GRAVEDAD_LUNA)
    
    # Mostrar resultados en formato tabular
    print("Resultados en la Tierra:")
    print(f"  Altura máxima: {hmax_tierra:.2f} m")
    print(f"  Tiempo hasta altura máxima: {tmax_tierra:.2f} s")
    print(f"  Tiempo total de vuelo: {tvuelo_tierra:.2f} s")
    
    print("\nResultados en la Luna:")
    print(f"  Altura máxima: {hmax_luna:.2f} m")
    print(f"  Tiempo hasta altura máxima: {tmax_luna:.2f} s")
    print(f"  Tiempo total de vuelo: {tvuelo_luna:.2f} s")
    
    # Análisis cualitativo de las diferencias
    print("\n=== REFLEXIÓN ===")
    print("En la Luna, al tener una gravedad menor (1.625 m/s² vs 9.8 m/s² en la Tierra):")
    print("- El objeto alcanza una altura máxima mayor")
    print("- Tarda más tiempo en llegar a la altura máxima")
    print("- El tiempo total de vuelo es significativamente mayor")
    print("- La velocidad cambia más lentamente debido a la menor aceleración")
    
    # Cálculo de diferencias porcentuales para cuantificar la comparación
    if hmax_tierra > 0:
        diff_altura = ((hmax_luna - hmax_tierra) / hmax_tierra) * 100
        print(f"\nLa altura máxima en la Luna es {diff_altura:.1f}% mayor que en la Tierra")
    
    if tmax_tierra > 0:
        diff_tiempo = ((tmax_luna - tmax_tierra) / tmax_tierra) * 100
        print(f"El tiempo hasta altura máxima en la Luna es {diff_tiempo:.1f}% mayor que en la Tierra")

def obtener_entrada_numerica(mensaje, min_valor=None, max_valor=None):
    """
    Solicita y valida entrada numérica del usuario con manejo de errores.
    
    Parámetros:
    mensaje (str): Mensaje a mostrar al usuario
    min_valor (float): Valor mínimo permitido (opcional)
    max_valor (float): Valor máximo permitido (opcional)
    
    Retorna:
    float: Valor numérico validado ingresado por el usuario
    """
    while True:
        try:
            valor = float(input(mensaje))  # Intentar convertir a float
            # Validar límites si se especificaron
            if min_valor is not None and valor < min_valor:
                print(f"Error: El valor debe ser mayor o igual a {min_valor}")
                continue
            if max_valor is not None and valor > max_valor:
                print(f"Error: El valor debe ser menor o igual a {max_valor}")
                continue
            return valor  # Valor válido
        except ValueError:
            print("Error: Por favor ingrese un número válido")  # Manejo de error de conversión

def main():
    """
    Función principal que orquesta la ejecución del programa.
    Maneja la interacción con el usuario y coordina las funciones.
    """
    print("=== PROGRAMA DE TIRO VERTICAL ===")
    print("Este programa calcula el movimiento de un objeto lanzado verticalmente hacia arriba.")
    print()
    
    # Solicitar datos al usuario con validación
    altura_inicial = obtener_entrada_numerica("Ingrese la altura inicial (m) [≥0]: ", 0)
    velocidad_inicial = obtener_entrada_numerica("Ingrese la velocidad inicial (m/s): ")
    
    # Advertencia si la velocidad inicial es negativa (hacia abajo)
    if velocidad_inicial < 0:
        print("Nota: La velocidad inicial es negativa. Esto significa que el objeto se lanza hacia abajo.")
    
    # Menú de selección de gravedad
    print("\nSeleccione el cuerpo celeste:")
    print("1. Tierra (g = 9.8 m/s²)")
    print("2. Luna (g = 1.625 m/s²)")
    print("3. Otro valor")
    
    # Validar selección de opción
    while True:
        opcion = input("Ingrese su opción (1-3): ")
        if opcion in ['1', '2', '3']:
            break
        print("Error: Por favor ingrese 1, 2 o 3")
    
    # Asignar gravedad según selección
    if opcion == '1':
        gravedad = GRAVEDAD_TIERRA
        cuerpo_celeste = "Tierra"
    elif opcion == '2':
        gravedad = GRAVEDAD_LUNA
        cuerpo_celeste = "Luna"
    else:
        gravedad = obtener_entrada_numerica("Ingrese el valor de la gravedad (m/s²) [>0]: ", 0)
        cuerpo_celeste = f"cuerpo con g={gravedad} m/s²"
    
    # Cálculos principales
    altura_maxima = calcular_altura_maxima(altura_inicial, velocidad_inicial, gravedad)
    tiempo_maximo = calcular_tiempo_altura_maxima(velocidad_inicial, gravedad)
    tiempo_vuelo = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, gravedad)
    
    # Presentación de resultados
    print("\n=== RESULTADOS ===")
    print(f"En la {cuerpo_celeste}:")
    print(f"Altura máxima alcanzada: {altura_maxima:.2f} m")
    print(f"Tiempo hasta altura máxima: {tiempo_maximo:.2f} s")
    
    # Manejo especial para caso de no impacto
    if tiempo_vuelo == float('inf'):
        print("Tiempo total de vuelo: Infinito (el objeto nunca cae al suelo)")
    else:
        print(f"Tiempo total de vuelo: {tiempo_vuelo:.2f} s")
    
    # Consulta de valores en tiempo específico
    tiempo_consulta = obtener_entrada_numerica("\nIngrese un tiempo para calcular la velocidad y altura (s) [≥0]: ", 0)
    velocidad_consulta = calcular_velocidad_tiempo(velocidad_inicial, gravedad, tiempo_consulta)
    altura_consulta = calcular_altura_tiempo(altura_inicial, velocidad_inicial, gravedad, tiempo_consulta)
    
    print(f"En t = {tiempo_consulta} s:")
    print(f"  Velocidad: {velocidad_consulta:.2f} m/s")
    print(f"  Altura: {altura_consulta:.2f} m")
    
    # Comparación adicional entre Tierra y Luna si aplica
    if opcion in ['1', '2']:
        comparar_tierra_luna(altura_inicial, velocidad_inicial)
    else:
        # Análisis cualitativo para gravedad personalizada
        print("\n=== REFLEXIÓN ===")
        print(f"Con una gravedad de {gravedad} m/s²:")
        if gravedad < GRAVEDAD_TIERRA:
            print("Al ser menor que la gravedad terrestre, el objeto alcanzará")
            print("mayores alturas y tardará más tiempo en caer.")
        elif gravedad > GRAVEDAD_TIERRA:
            print("Al ser mayor que la gravedad terrestre, el objeto alcanzará")
            print("menores alturas y tardará menos tiempo en caer.")
        else:
            print("La gravedad es igual a la terrestre.")
    
    # Opción de visualización animada
    animar = input("\n¿Desea ver una animación del movimiento? (s/n): ").lower()
    if animar == 's':
        print("Generando animación...")
        animar_tiro_vertical(altura_inicial, velocidad_inicial, gravedad)

# Punto de entrada del programa
if __name__ == "__main__":
    main()  # Ejecutar función principal
