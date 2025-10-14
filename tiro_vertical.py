# Importacion de librerias
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation #Incluye las funciones para crear animaciones
import math # Libreria estandar de python, la necesitamos para sacar raices cuadradas de manera simple

# Constantes fisicas
# NO MODIFIQUEN LAS CONSTANTES!
GRAVEDAD_TIERRA = 9.8  # m/s²
GRAVEDAD_LUNA = 1.625  # m/s²
# los def nos permitiran reutulizar codigo
# y0=altura inicial, v0=velocidad inicial, g=gravedad.

def calcular_altura_maxima(altura_inicial, velocidad_inicial, gravedad):
    # Si la velocidad inicial es negativa, la altura maxima es la inicial MRUA
    if velocidad_inicial <= 0: 
        return altura_inicial
    # Formula: h_max = y0 + (v0²)/(2*g)
    altura_maxima = altura_inicial + (velocidad_inicial**2) / (2 * gravedad)
    return altura_maxima

def calcular_tiempo_altura_maxima(velocidad_inicial, gravedad):
    # Si la velocidad inicial es negativa, tiempo maximo es 0
    if velocidad_inicial <= 0:
        return 0.0
    # Formula: t_max = v0 / g (cuando v=0)
    tiempo_maximo = velocidad_inicial / gravedad
    return tiempo_maximo

def calcular_velocidad_tiempo(velocidad_inicial, gravedad, tiempo):
    # Formula: v(t) = v0 - g*t
    velocidad = velocidad_inicial - gravedad * tiempo
    return velocidad

def calcular_altura_tiempo(altura_inicial, velocidad_inicial, gravedad, tiempo):
    # Formula: y(t) = y0 + v0*t - 0.5*g*t²
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
                return 0  # Ya esta en el suelo
    
    # Resolver ecuacion cuadratica: 0.5*g*t² - v0*t - y0 = 0
    a = -0.5 * gravedad
    b = velocidad_inicial
    c = altura_inicial
    
    discriminante = b**2 - 4*a*c
    # Manejo de casos especiales: g=0, discriminante negativo
    # Si no hay soluciones reales, el objeto nunca cae
    if discriminante < 0:
        return float('inf')
    # Calcular raices de la ecuacion cuadratica
    t1 = (-b + math.sqrt(discriminante)) / (2*a)
    t2 = (-b - math.sqrt(discriminante)) / (2*a)
    
    # Filtrar solo tiempos positivos
    tiempos = [t for t in [t1, t2] if t >= 0]
    
    if not tiempos:
        return float('inf')  # Nunca alcanza y=0
    
    # Devolver el mayor tiempo positivo (impacto despues de subir y bajar)
    return max(tiempos)
#Funcion anidada: init() y animate()
#FuncAnimation para animar frames
#np.linspace genera tiempos equiespaciados

def animar_tiro_vertical(altura_inicial, velocidad_inicial, gravedad):
    # Calcular tiempo total de vuelo para la animacion
    tiempo_vuelo = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, gravedad)
    
    # Si el tiempo es infinito, usar valor por defecto
    if tiempo_vuelo == float('inf'):
        tiempo_vuelo = 10
    
    # Crear array de tiempos y calcular alturas
    tiempos = np.linspace(0, tiempo_vuelo, 100)
    alturas = [calcular_altura_tiempo(altura_inicial, velocidad_inicial, gravedad, t) for t in tiempos]
    
    # Configurar grafico
    fig, ax = plt.subplots() # fig representa la ventana, ax las coordenadas del plano
    ax.set_xlim(0, 2)  # Rango fijo en X
    ax.set_ylim(0, max(max(alturas), altura_inicial) * 1.1)  # Rango en Y con margen (1.1 le da un margen de 10%)
    ax.set_xlabel('Posicion X (m)') #Etiqueta del grafico en X
    ax.set_ylabel('Altura (m)')# Mismo funcionamiento para el eje Y
    ax.set_title('Animacion de Tiro Vertical') # Titulo de grafico
    ax.grid(True)
    
    # Crear punto que representa el objeto
    punto, = ax.plot([1], [altura_inicial], 'ro', markersize=10) #ax.plot esta en valor 1 por ser tiro vertical
    
    def init():
        # Inicializar animacion en posicion inicial
        punto.set_data([1], [altura_inicial])
        return punto,
    
    def animate(i):
        # Actualizar posicion para cada frame
        if i < len(tiempos):
            punto.set_data([1], [alturas[i]])
        return punto,
    
    # Crear animacion
    anim = FuncAnimation(fig, animate, init_func=init,
                         frames=len(tiempos), interval=50, blit=True)
    
    plt.show() #muestra la animacion en pantalla

def comparar_tierra_luna(altura_inicial, velocidad_inicial):
    # Comparar resultados entre Tierra y Luna
    print("\n=== COMPARACION TIERRA vs LUNA ===")
    
    # Calculos para Tierra
    hmax_tierra = calcular_altura_maxima(altura_inicial, velocidad_inicial, GRAVEDAD_TIERRA)
    tmax_tierra = calcular_tiempo_altura_maxima(velocidad_inicial, GRAVEDAD_TIERRA)
    tvuelo_tierra = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, GRAVEDAD_TIERRA)
    
    # Calculos para Luna
    hmax_luna = calcular_altura_maxima(altura_inicial, velocidad_inicial, GRAVEDAD_LUNA)
    tmax_luna = calcular_tiempo_altura_maxima(velocidad_inicial, GRAVEDAD_LUNA)
    tvuelo_luna = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, GRAVEDAD_LUNA)
    
    # Mostrar resultados
    print("Resultados en la Tierra:")
    print(f"  Altura maxima: {hmax_tierra:.2f} m")
    print(f"  Tiempo hasta altura maxima: {tmax_tierra:.2f} s")
    print(f"  Tiempo total de vuelo: {tvuelo_tierra:.2f} s")
    
    print("\nResultados en la Luna:")
    print(f"  Altura maxima: {hmax_luna:.2f} m")
    print(f"  Tiempo hasta altura maxima: {tmax_luna:.2f} s")
    print(f"  Tiempo total de vuelo: {tvuelo_luna:.2f} s")
    
    # Analisis cualitativo
    print("\n=== REFLEXION ===")
    print("En la Luna, al tener una gravedad menor (1.625 m/s² vs 9.8 m/s² en la Tierra):")
    print("- El objeto alcanza una altura maxima mayor")
    print("- Tarda mas tiempo en llegar a la altura maxima")
    print("- El tiempo total de vuelo es significativamente mayor")
    
    # Calculo de diferencias porcentuales
    if hmax_tierra > 0:
        diff_altura = ((hmax_luna - hmax_tierra) / hmax_tierra) * 100
        print(f"\nLa altura maxima en la Luna es {diff_altura:.1f}% mayor que en la Tierra")
    
    if tmax_tierra > 0:
        diff_tiempo = ((tmax_luna - tmax_tierra) / tmax_tierra) * 100
        print(f"El tiempo hasta altura maxima en la Luna es {diff_tiempo:.1f}% mayor que en la Tierra")
        
def obtener_entrada_numerica(mensaje, min_valor=None, max_valor=None):
    # Solicitar y validar entrada numerica del usuario
    while True:
        try:
            valor = float(input(mensaje))
            # Validar limites si se especifican
            if min_valor is not None and valor < min_valor:
                print(f"Error: El valor debe ser mayor o igual a {min_valor}")
                continue
            if max_valor is not None and valor > max_valor:
                print(f"Error: El valor debe ser menor o igual a {max_valor}")
                continue
            return valor
        except ValueError:
            print("Error: Por favor ingrese un numero valido")

def main():
    # Funcion principal del programa
    print("=== PROGRAMA DE TIRO VERTICAL ===")
    print("Este programa calcula el movimiento de un objeto lanzado verticalmente hacia arriba.")
    print()
    
    # Solicitar parametros iniciales
    altura_inicial = obtener_entrada_numerica("Ingrese la altura inicial (m) [≥0]: ", 0)
    velocidad_inicial = obtener_entrada_numerica("Ingrese la velocidad inicial (m/s): ")
    
    # Advertencia si la velocidad es negativa
    if velocidad_inicial < 0:
        print("Nota: La velocidad inicial es negativa. Esto significa que el objeto se lanza hacia abajo.")
    
    # Menu de seleccion de gravedad
    print("\nSeleccione el cuerpo celeste:")
    print("1. Tierra (g = 9.8 m/s²)")
    print("2. Luna (g = 1.625 m/s²)")
    print("3. Otro valor")
    
    # Validar seleccion
    while True:
        opcion = input("Ingrese su opcion (1-3): ")
        if opcion in ['1', '2', '3']:
            break
        print("Error: Por favor ingrese 1, 2 o 3")
    
    # Asignar valor de gravedad segun seleccion
    if opcion == '1':
        gravedad = GRAVEDAD_TIERRA
        cuerpo_celeste = "Tierra"
    elif opcion == '2':
        gravedad = GRAVEDAD_LUNA
        cuerpo_celeste = "Luna"
    else:
        gravedad = obtener_entrada_numerica("Ingrese el valor de la gravedad (m/s²) [>0]: ", 0)
        cuerpo_celeste = f"cuerpo con g={gravedad} m/s²"
    
    # Realizar calculos principales
    altura_maxima = calcular_altura_maxima(altura_inicial, velocidad_inicial, gravedad)
    tiempo_maximo = calcular_tiempo_altura_maxima(velocidad_inicial, gravedad)
    tiempo_vuelo = calcular_tiempo_vuelo(altura_inicial, velocidad_inicial, gravedad)
    
    # Mostrar resultados
    print("\n=== RESULTADOS ===")
    print(f"En la {cuerpo_celeste}:")
    print(f"Altura maxima alcanzada: {altura_maxima:.2f} m")
    print(f"Tiempo hasta altura maxima: {tiempo_maximo:.2f} s")
    
    # Manejar caso especial de no impacto
    if tiempo_vuelo == float('inf'):
        print("Tiempo total de vuelo: Infinito (el objeto nunca cae al suelo)")
    else:
        print(f"Tiempo total de vuelo: {tiempo_vuelo:.2f} s")
    
    # Consultar valores en tiempo especifico
    tiempo_consulta = obtener_entrada_numerica("\nIngrese un tiempo para calcular la velocidad y altura (s) [≥0]: ", 0)
    velocidad_consulta = calcular_velocidad_tiempo(velocidad_inicial, gravedad, tiempo_consulta)
    altura_consulta = calcular_altura_tiempo(altura_inicial, velocidad_inicial, gravedad, tiempo_consulta)
    
    print(f"En t = {tiempo_consulta} s:")
    print(f"  Velocidad: {velocidad_consulta:.2f} m/s")
    print(f"  Altura: {altura_consulta:.2f} m")
    
    # Comparacion adicional si es Tierra o Luna
    if opcion in ['1', '2']:
        comparar_tierra_luna(altura_inicial, velocidad_inicial)
    else:
        # Analisis para gravedad personalizada
        print("\n=== REFLEXION ===")
        print(f"Con una gravedad de {gravedad} m/s²:")
        if gravedad < GRAVEDAD_TIERRA:
            print("Al ser menor que la gravedad terrestre, el objeto alcanzara")
            print("mayores alturas y tardara mas tiempo en caer.")
        elif gravedad > GRAVEDAD_TIERRA:
            print("Al ser mayor que la gravedad terrestre, el objeto alcanzara")
            print("menores alturas y tardara menos tiempo en caer.")
        else:
            print("La gravedad es igual a la terrestre.")
    
    # Opcion de animacion
    animar = input("\n¿Desea ver una animacion del movimiento? (s/n): ").lower()
    if animar == 's':
        print("Generando animacion...")
        animar_tiro_vertical(altura_inicial, velocidad_inicial, gravedad)

# Punto de entrada del programa
if __name__ == "__main__":
    main()
