# Escribe tu supercódigo aquí :-)
# Iniciamos declarando las librerias necesarias
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer
import board
import busio
import adafruit_ds3231
import adafruit_sht31d
from digitalio import DigitalInOut, Direction, Pull
import analogio
import digitalio
import time
import simpleio

# Definimos las variables
texto = None
color = None
valor = None
hora_inicio_luz = None
hora_apagado_luz = None
reloj = None
luz = None
porcentaje_humedad_suelo = None
limite_humedad_suelo_min = None
limite_humedad_suelo_max = None
bomba_agua = None
temperatura_ambiente = None
limite_temp_ambiente_max = None
limite_temp_ambiente_min = None
fan_cooler = None
limite_tem_ambiente_min = None
sensor_temp_humed_ambiente = None
humedad_suelo_min = None
humedad_suelo_max = None
sensor_humedad_suelo = None
humedad_ambiente = None
sensor_nivel_agua = None

# Declaramos una funcion para controlar la luz
def gestionar_estado_luz(hora_inicio_luz, hora_apagado_luz, hora_actual, luz):
    global texto, color, valor, porcentaje_humedad_suelo, limite_humedad_suelo_min, limite_humedad_suelo_max, bomba_agua_1, bomba_agua_2, bomba_agua_3, temperatura_ambiente, limite_temp_ambiente_max, limite_temp_ambiente_min, fan_cooler, limite_tem_ambiente_min, sensor_temp_humed_ambiente, humedad_suelo_min, humedad_suelo_max, sensor_humedad_suelo, humedad_ambiente

    if hora_inicio_luz < hora_apagado_luz:
        if (hora_inicio_luz <= hora_actual) and (
            hora_actual < hora_apagado_luz
        ):
            luz.value = True
        else:
            luz.value = False
    else:
        if (hora_inicio_luz <= hora_actual) or (
            hora_actual < hora_apagado_luz
        ):
            luz.value = True
        else:
            luz.value = False

# Declaramos una funcion para controlar la bomba
def gestionar_estado_bomba_agua(
    porcentaje_humedad_suelo,
    limite_humedad_suelo_min,
    limite_humedad_suelo_max,
    bomba_agua,
):
    global texto, color, valor, hora_inicio_luz, hora_apagado_luz, reloj, luz, temperatura_ambiente, limite_temp_ambiente_max, limite_temp_ambiente_min, fan_cooler, limite_tem_ambiente_min, sensor_temp_humed_ambiente, humedad_suelo_min, humedad_suelo_max, sensor_humedad_suelo, humedad_ambiente
    if porcentaje_humedad_suelo <= limite_humedad_suelo_min:
        bomba_agua.value = True
    elif porcentaje_humedad_suelo >= limite_humedad_suelo_max:
        bomba_agua.value = False

# Declaramos una funcion para controlar los coolers de entrada y salida de aire
def gestionar_estado_cooler(
    temperatura_ambiente, limite_temp_ambiente_max, limite_temp_ambiente_min, fan_cooler
):
    global texto, color, valor, hora_inicio_luz, hora_apagado_luz, reloj, luz, porcentaje_humedad_suelo, limite_humedad_suelo_min, limite_humedad_suelo_max, bomba_agua_1, bomba_agua_2, bomba_agua_3, limite_tem_ambiente_min, sensor_temp_humed_ambiente, humedad_suelo_min, humedad_suelo_max, sensor_humedad_suelo, humedad_ambiente
    if temperatura_ambiente >= limite_temp_ambiente_max:
        fan_cooler.value = True
        pixel_framebuf_led.fill(0xFF0000)
    elif temperatura_ambiente <= limite_temp_ambiente_min:
        fan_cooler.value = False
        pixel_framebuf_led.fill(0xFFFF00)
    elif (temperatura_ambiente >= limite_temp_ambiente_min) and (
        temperatura_ambiente <= limite_temp_ambiente_max
    ):
        pixel_framebuf_led.fill(0x00FF00)
    pixel_framebuf_led.display()

# Declaramos una funcion para mostrar texto por el display de Leds
def showText(text, colour):
    if len(str(text)) == 1:
        pixel_framebuf.text(str(text), 2, 0, colour)
        pixel_framebuf.display()
    else:
        for i in range(8, -6 * len(str(text)), -1):
            pixel_framebuf.fill(0)
            pixel_framebuf.text(str(text), i, 0, colour)
            pixel_framebuf.display()
            time.sleep(0.1)

# Declaramos una funcion para mostrar numeros por el display de Leds
def mostrarNumero(number, colour):
    if number in range(10) and type(number) == int:
        pixel_framebuf.text(str(number), 2, 0, colour)
        pixel_framebuf.display()
    else:
        for i in range(8, -6 * len(str(number)), -1):
            pixel_framebuf.fill(0)
            pixel_framebuf.text(str(number), i, 0, colour)
            pixel_framebuf.display()
            time.sleep(0.1)

# Declaramos una funcion para mostrar mensajes por el display de Leds
def mostrar_mensaje(texto, color, valor):
    global hora_inicio_luz, hora_apagado_luz, reloj, luz, porcentaje_humedad_suelo, limite_humedad_suelo_min, limite_humedad_suelo_max, bomba_agua_1, bomba_agua_2, bomba_agua_3, temperatura_ambiente, limite_temp_ambiente_max, limite_temp_ambiente_min, fan_cooler, limite_tem_ambiente_min, sensor_temp_humed_ambiente, humedad_suelo_min, humedad_suelo_max, sensor_humedad_suelo, humedad_ambiente
    showText(texto, color)
    mostrarNumero(valor, color)

# Declaramos una funcion para mostrar emojis por el display de Leds
def pintarEmoji(matriz, color):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 1:
                pixel_framebuf.pixel(j, i, color)
    pixel_framebuf.display()

# Declaramos una funcion para gestionar la animacion (emojis)
def gestionar_animacion(
    temperatura_ambiente, limite_temp_ambiente_min, limite_temp_ambiente_max
):
    if temperatura_ambiente > limite_temp_ambiente_max:  # frio azul ma = 10 min= 2 2
        pintarEmoji(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
            0x0000FF,
        )
    elif temperatura_ambiente < limite_temp_ambiente_min:  # Archi se pone triste :(
        pintarEmoji(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 1, 0],
            ],
            0xFF0000,
        )
    else:
        pintarEmoji(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
            0x00FF00,
        )

# Declaramos una funcion para enviar datos al Esp32
def envio_datos(porcentaje_humedad_suelo, humedad_ambiente, temperatura_ambiente):
    payload = bytes("S" + str(porcentaje_humedad_suelo), "utf-8")
    hc05.write(payload)
    time.sleep(0.1)
    payload = bytes("A" + str(humedad_ambiente), "utf-8")
    hc05.write(payload)
    time.sleep(0.1)
    payload = bytes("T" + str(temperatura_ambiente), "utf-8")
    hc05.write(payload)
    time.sleep(0.1)


# Entradas
sht_31 = adafruit_sht31d.SHT31D(busio.I2C(board.GP5, board.GP4))
sensor_humedad_suelo = analogio.AnalogIn(board.GP26) # Habilitamos el sensor de humedad de suelo
reloj = adafruit_ds3231.DS3231(busio.I2C(board.GP3, board.GP2))# Habilita esta linea para controlar el RTC
#reloj.datetime = time.struct_time((2024,8,9,15,16,30,0,-1,-1))# Con esta linea podes calibrar la fecha y hora de tu RTC por primera vez,
# luego se recomienda comentar esta linea

# Configuracion del display
pixel_pin = board.NEOPIXEL
pixel_width = 8
pixel_height = 8
pixel_num = 64
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.1, auto_write=False)
pixel_framebuf = PixelFramebuffer(pixels, pixel_width, pixel_height, alternating=False)
pixels_led = neopixel.NeoPixel(board.GP6, 20, brightness=1, auto_write=False)
pixel_framebuf_led = PixelFramebuffer(pixels_led, 20, 1, alternating=False)


# Envio de Datos a ESP32
hc05 = busio.UART(board.GP16, board.GP17, baudrate=115200)

# Botones
btnA = DigitalInOut(board.A)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP
btnD = DigitalInOut(board.D)
btnD.direction = Direction.INPUT
btnD.pull = Pull.UP
btnC = DigitalInOut(board.C)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Salidas
luz = digitalio.DigitalInOut(board.GP13)
luz.direction = digitalio.Direction.OUTPUT
bomba_agua = digitalio.DigitalInOut(board.GP14)
bomba_agua.direction = digitalio.Direction.OUTPUT
fan_cooler = digitalio.DigitalInOut(board.GP15)
fan_cooler.direction = digitalio.Direction.OUTPUT

# Constantes para el manejo de sensores
humedad_suelo_min = 48000 # Este valor se toma cuando el sensor esta en tierra seca (humedad% = 0%)
humedad_suelo_max = 19000 # Este valor se toma cuando el sensor esta en tierra humeda (humedad% = 100%)
limite_temp_ambiente_min = 18 # Valor minimo para activar los coolers
limite_temp_ambiente_max = 25 # Valor minimo para desactivar los coolers
limite_humedad_suelo_min = 40 # Valor minimo para activar la bomba
limite_humedad_suelo_max = 50 # Valor maximo para desactivar la bomba
hora_inicio_luz = 8 # hora para activar la luz
hora_apagado_luz = 16 # hora para desactivar la luz

# Declaramos la funcion principal y el Loop
def main():

    while True:

        # Adquision de datos. Usamos round() para redondear los valores adquiridos
        # DHT22
        try:
            temperatura_ambiente = round(sht_31.temperature, 2)
            humedad_ambiente = round(sht_31.relative_humidity, 2)

        except RuntimeError as e:
            print("Error reading data from sensors: ", e)

        # Sensor Capacitivo de humedad de suelo
        # Para calibrar este sensor se toman medidas cuando esta seco y cuando esta en agua
        # De esta manera concemos los valores minimos y maximos (respectivamente) entre los que va a a variar nuestro sensor
        # Ademas, debemos tener en cuenta que cuanto mas aumenta la humedad el numero de bits disminuye
        # por lo que debemos desarrollar una formula para tomar los datos.
        # La siguiente linea contiene la formula para la calibracion del sensor,
        # la formula es:
        # humedad% = (hmin - x) * 100 /  (hmax - hmin)
        # Donde:
        # hmin = es la humedad minima medida por el sensor en seco
        # hmax = es la humedad maxima medida por el sensor en agua
        # x = es el valor medido
        porcentaje_humedad_suelo = round((((humedad_suelo_min - sensor_humedad_suelo.value)/(humedad_suelo_min - humedad_suelo_max))* 100),1,)

        # RTC DS3231
        rtc = reloj.datetime #Tomamos los datos del RTC
        hora_actual = rtc.tm_hour #Tomamos la hora y la asignamos a una variable

        # Gestion de actuadores
        gestionar_estado_bomba_agua(porcentaje_humedad_suelo, limite_humedad_suelo_min, limite_humedad_suelo_max, bomba_agua)
        gestionar_estado_cooler(temperatura_ambiente, limite_temp_ambiente_max, limite_temp_ambiente_min, fan_cooler)
        gestionar_animacion(temperatura_ambiente, limite_temp_ambiente_min, limite_temp_ambiente_max)
        gestionar_estado_luz(hora_inicio_luz, hora_apagado_luz, hora_actual, luz)

        # Envio de datos desde Archi a Esp32
        payload = bytes("L" + str(1), "utf-8")
        hc05.write(payload)
        envio_datos(porcentaje_humedad_suelo, humedad_ambiente, temperatura_ambiente)
        time.sleep(1)

        # Activacion de botones para mostrar datos por pantalla de Archi
        if not btnA.value:
            mostrar_mensaje("H.S", 0x0000FF, porcentaje_humedad_suelo)
        if not btnD.value:
            mostrar_mensaje("H.A", 0xFF6600, humedad_ambiente)
        if not btnC.value:
            mostrar_mensaje("T.A", 0x33FF33, temperatura_ambiente)


main()
