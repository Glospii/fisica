# Importación de librerías
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

# Constantes físicas
GRAVEDAD_TIERRA = 9.8  # m/s²
GRAVEDAD_LUNA = 1.625  # m/s²

# --- FUNCIONES DE CÁLCULO FÍSICO ---

def calcular_altura_maxima(altura_inicial, velocidad_inicial, gravedad):
    # Si la velocidad inicial es negativa, la altura máxima es la inicial
    if velocidad_inicial <= 0:
        return altura_inicial
    # Fórmula: h_max = y0 + (v0²)/(2*g)
    altura_maxima = altura_inicial + (velocidad_inicial**2) / (2 * gravedad)
    return altura_maxima

def calcular_tiempo_altura_maxima(velocidad_inicial, gravedad):
    # Si la velocidad inicial es negativa, tiempo máximo es 0
    if velocidad_inicial <= 0:
        return 0.0
    # Fórmula: t_max = v0 / g (cuando v=0)
    tiempo_maximo = velocidad_inicial / gravedad
    return tiempo_maximo

def calcular_velocidad_tiempo(velocidad_inicial, gravedad, tiempo):
    # Fórmula: v(t) = v0 - g*t
    velocidad = velocidad_inicial - gravedad * tiempo
    return velocidad

def calcular_altura_tiempo(altura_inicial, velocidad_inicial, gravedad, tiempo):
    # Fórmula: y(t) = y0 + v0*t - 0.5*g*t²
    altura = altura_inicial + velocidad_inicial * tiempo - 0.5 * gravedad * tiempo**2
    return altura

def calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, gravedad):
    # Caso especial: sin gravedad
    if gravedad == 0:
        if velocidad_inicial == 0:
            return float('inf')  # Permanece flotando
        else:
            if altura_inicial > 0:
                return abs(altura_inicial / velocidad_inicial)  # MRU
            else:
                return 0  # Ya está en el suelo
    
    # Resolver ecuación cuadrática: 0.5*g*t² - v0*t - y0 = 0
    a = -0.5 * gravedad
    b = velocidad_inicial
    c = altura_inicial
    
    discriminante = b**2 - 4*a*c
    
    # Si no hay soluciones reales, el objeto nunca cae
    if discriminante < 0:
        return float('inf')
    
    # Calcular raíces de la ecuación cuadrática
    t1 = (-b + math.sqrt(discriminante)) / (2*a)
    t2 = (-b - math.sqrt(discriminante)) / (2*a)
    
    # Filtrar solo tiempos positivos
    tiempos = [t for t in [t1, t2] if t >= 0]
    
    if not tiempos:
        return float('inf')  # Nunca alcanza y=0
    
    # Devolver el mayor tiempo positivo (impacto después de subir y bajar)
    return max(tiempos)

# --- FUNCIONES DE VISUALIZACIÓN ---

def animar_tiro_vertical(altura_inicial, velocidad_inicial, gravedad):
    # Calcular tiempo total de vuelo para la animación
    tiempo_vuelo = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, gravedad)
    
    # Si el tiempo es infinito, usar valor por defecto
    if tiempo_vuelo == float('inf'):
        tiempo_vuelo = 10
    
    # Crear array de tiempos y calcular alturas
    tiempos = np.linspace(0, tiempo_vuelo, 100)
    alturas = [calcular_altura_tiempo(altura_inicial, velocidad_inicial, gravedad, t) for t in tiempos]
    
    # Configurar gráfico
    fig, ax = plt.subplots()
    ax.set_xlim(0, 2)  # Rango fijo en X
    ax.set_ylim(0, max(max(alturas), altura_inicial) * 1.1)  # Rango en Y con margen
    ax.set_xlabel('Posición X (m)')
    ax.set_ylabel('Altura (m)')
    ax.set_title('Animación de Tiro Vertical')
    ax.grid(True)
    
    # Crear punto que representa el objeto
    punto, = ax.plot([1], [altura_inicial], 'ro', markersize=10)
    
    def init():
        # Inicializar animación en posición inicial
        punto.set_data([1], [altura_inicial])
        return punto,
    
    def animate(i):
        # Actualizar posición para cada frame
        if i < len(tiempos):
            punto.set_data([1], [alturas[i]])
        return punto,
    
    # Crear animación
    anim = FuncAnimation(fig, animate, init_func=init,
                         frames=len(tiempos), interval=50, blit=True)
    
    plt.show()

def comparar_tierra_luna(altura_inicial, velocidad_inicial):
    # Comparar resultados entre Tierra y Luna
    print("\n=== COMPARACIÓN TIERRA vs LUNA ===")
    
    # Cálculos para Tierra
    hmax_tierra = calcular_altura_maxima(altura_inicial, velocidad_inicial, GRAVEDAD_TIERRA)
    tmax_tierra = calcular_tiempo_altura_maxima(velocidad_inicial, GRAVEDAD_TIERRA)
    tvuelo_tierra = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, GRAVEDAD_TIERRA)
    
    # Cálculos para Luna
    hmax_luna = calcular_altura_maxima(altura_inicial, velocidad_inicial, GRAVEDAD_LUNA)
    tmax_luna = calcular_tiempo_altura_maxima(velocidad_inicial, GRAVEDAD_LUNA)
    tvuelo_luna = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, GRAVEDAD_LUNA)
    
    # Mostrar resultados
    print("Resultados en la Tierra:")
    print(f"  Altura máxima: {hmax_tierra:.2f} m")
    print(f"  Tiempo hasta altura máxima: {tmax_tierra:.2f} s")
    print(f"  Tiempo total de vuelo: {tvuelo_tierra:.2f} s")
    
    print("\nResultados en la Luna:")
    print(f"  Altura máxima: {hmax_luna:.2f} m")
    print(f"  Tiempo hasta altura máxima: {tmax_luna:.2f} s")
    print(f"  Tiempo total de vuelo: {tvuelo_luna:.2f} s")
    
    # Análisis cualitativo
    print("\n=== REFLEXIÓN ===")
    print("En la Luna, al tener una gravedad menor (1.625 m/s² vs 9.8 m/s² en la Tierra):")
    print("- El objeto alcanza una altura máxima mayor")
    print("- Tarda más tiempo en llegar a la altura máxima")
    print("- El tiempo total de vuelo es significativamente mayor")
    
    # Cálculo de diferencias porcentuales
    if hmax_tierra > 0:
        diff_altura = ((hmax_luna - hmax_tierra) / hmax_tierra) * 100
        print(f"\nLa altura máxima en la Luna es {diff_altura:.1f}% mayor que en la Tierra")
    
    if tmax_tierra > 0:
        diff_tiempo = ((tmax_luna - tmax_tierra) / tmax_tierra) * 100
        print(f"El tiempo hasta altura máxima en la Luna es {diff_tiempo:.1f}% mayor que en la Tierra")

# --- FUNCIONES DE INTERFAZ DE USUARIO ---

def obtener_entrada_numerica(mensaje, min_valor=None, max_valor=None):
    # Solicitar y validar entrada numérica del usuario
    while True:
        try:
            valor = float(input(mensaje))
            # Validar límites si se especifican
            if min_valor is not None and valor < min_valor:
                print(f"Error: El valor debe ser mayor o igual a {min_valor}")
                continue
            if max_valor is not None and valor > max_valor:
                print(f"Error: El valor debe ser menor o igual a {max_valor}")
                continue
            return valor
        except ValueError:
            print("Error: Por favor ingrese un número válido")

def main():
    # Función principal del programa
    print("=== PROGRAMA DE TIRO VERTICAL ===")
    print("Este programa calcula el movimiento de un objeto lanzado verticalmente hacia arriba.")
    print()
    
    # Solicitar parámetros iniciales
    altura_inicial = obtener_entrada_numerica("Ingrese la altura inicial (m) [≥0]: ", 0)
    velocidad_inicial = obtener_entrada_numerica("Ingrese la velocidad inicial (m/s): ")
    
    # Advertencia si la velocidad es negativa
    if velocidad_inicial < 0:
        print("Nota: La velocidad inicial es negativa. Esto significa que el objeto se lanza hacia abajo.")
    
    # Menú de selección de gravedad
    print("\nSeleccione el cuerpo celeste:")
    print("1. Tierra (g = 9.8 m/s²)")
    print("2. Luna (g = 1.625 m/s²)")
    print("3. Otro valor")
    
    # Validar selección
    while True:
        opcion = input("Ingrese su opción (1-3): ")
        if opcion in ['1', '2', '3']:
            break
        print("Error: Por favor ingrese 1, 2 o 3")
    
    # Asignar valor de gravedad según selección
    if opcion == '1':
        gravedad = GRAVEDAD_TIERRA
        cuerpo_celeste = "Tierra"
    elif opcion == '2':
        gravedad = GRAVEDAD_LUNA
        cuerpo_celeste = "Luna"
    else:
        gravedad = obtener_entrada_numerica("Ingrese el valor de la gravedad (m/s²) [>0]: ", 0)
        cuerpo_celeste = f"cuerpo con g={gravedad} m/s²"
    
    # Realizar cálculos principales
    altura_maxima = calcular_altura_maxima(altura_inicial, velocidad_inicial, gravedad)
    tiempo_maximo = calcular_tiempo_altura_maxima(velocidad_inicial, gravedad)
    tiempo_vuelo = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, gravedad)
    
    # Mostrar resultados
    print("\n=== RESULTADOS ===")
    print(f"En la {cuerpo_celeste}:")
    print(f"Altura máxima alcanzada: {altura_maxima:.2f} m")
    print(f"Tiempo hasta altura máxima: {tiempo_maximo:.2f} s")
    
    # Manejar caso especial de no impacto
    if tiempo_vuelo == float('inf'):
        print("Tiempo total de vuelo: Infinito (el objeto nunca cae al suelo)")
    else:
        print(f"Tiempo total de vuelo: {tiempo_vuelo:.2f} s")
    
    # Consultar valores en tiempo específico
    tiempo_consulta = obtener_entrada_numerica("\nIngrese un tiempo para calcular la velocidad y altura (s) [≥0]: ", 0)
    velocidad_consulta = calcular_velocidad_tiempo(velocidad_inicial, gravedad, tiempo_consulta)
    altura_consulta = calcular_altura_tiempo(altura_inicial, velocidad_inicial, gravedad, tiempo_consulta)
    
    print(f"En t = {tiempo_consulta} s:")
    print(f"  Velocidad: {velocidad_consulta:.2f} m/s")
    print(f"  Altura: {altura_consulta:.2f} m")
    
    # Comparación adicional si es Tierra o Luna
    if opcion in ['1', '2']:
        comparar_tierra_luna(altura_inicial, velocidad_inicial)
    else:
        # Análisis para gravedad personalizada
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
    
    # Opción de animación
    animar = input("\n¿Desea ver una animación del movimiento? (s/n): ").lower()
    if animar == 's':
        print("Generando animación...")
        animar_tiro_vertical(altura_inicial, velocidad_inicial, gravedad)

# Punto de entrada del programa
if __name__ == "__main__":
    main()
