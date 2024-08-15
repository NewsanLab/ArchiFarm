// Librerias
#include <WiFi.h>
//#include <ESP8266WiFi.h>

// Configuración de la red WiFi
const char *ssid = "";// Ingresa el nombre de tu red Wi-Fi
const char *password = "";// Ingresa la contrasena de tu Wi-Fi

// Configuración ThingSpeak
const char *thingSpeakAddress = "api.thingspeak.com";
const String writeAPIKey = "";//Ingresa la API de tu canal en Thinkspeak

const char *DEVICE_LABEL = "Esp32";// ingresa el nombre de tu Dispositivo Esp32
String temperature = "temperatura";// Ingresa el nombre de la variable que quieres publicar en Thinkspeak
String humidity = "humedad-ambiente";// Ingresa el nombre de la variable que quieres publicar en Thinkspeak
String soil_humidity = "humedad-suelo";// Ingresa el nombre de la variable que quieres publicar en Thinkspeak

void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++)
  {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void setup()
{

  // Ingresa tu codigo que solo correra una vez al iniciar
  Serial.begin(115200);

  // Inicia la conexcion a internet
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop()
{
  if (Serial.available() > 0) {
      String topic = "";
      // Se reciben los datos desde Archi
      while (Serial.available() > 0){
        char dato = Serial.read();
        topic = topic + dato;
      }
      // Se procesa los datos recibidos
      if (topic[0] == 'T'){
        temperature = topic.substring(1);// Ingresa tu variable y el valor medido
        // Envío de datos a ThingSpeak
        String data = "field2=" + String(temperature);
        if (sendDataToThingSpeak(data)) {
         Serial.println("Dato enviado a ThingSpeak!");
         }   
        else{
          Serial.println("Fallo el envio de Dato a ThingSpeak");} 
      }

      if (topic[0] == 'A'){
        humidity = topic.substring(1);// Ingresa tu variable y el valor medido
        // Envío de datos a ThingSpeak
        String data = "field1=" + String(humidity);
        if (sendDataToThingSpeak(data)) {
         Serial.println("Dato enviado a ThingSpeak!");
         }   
        else{
          Serial.println("Fallo el envio de Dato a ThingSpeak");}      
        }

      if (topic[0] == 'S'){
        soil_humidity = topic.substring(1);// Ingresa tu variable y el valor medido
        // Envío de datos a ThingSpeak
        String data = "field3=" + String(soil_humidity);
        if (sendDataToThingSpeak(data)) {
         Serial.println("Dato enviado a ThingSpeak!");
         }   
        else{
          Serial.println("Fallo el envio de Dato a ThingSpeak");}       
      }
    }

    delay(1000);
  }

 bool sendDataToThingSpeak(String data) {
  WiFiClient client;
  if (!client.connect(thingSpeakAddress, 80)) {
    return false;
  }

  String request = "POST /update HTTP/1.1\n";
  request += "Host: " + String(thingSpeakAddress) + "\n";
  request += "Connection: close\n";
  request += "X-THINGSPEAKAPIKEY: " + writeAPIKey + "\n";
  request += "Content-Type: application/x-www-form-urlencoded\n";
  request += "Content-Length: " + String(data.length()) + "\n\n";
  request += data;

  client.print(request);

  delay(1000);

  client.stop();
  return true;
}
