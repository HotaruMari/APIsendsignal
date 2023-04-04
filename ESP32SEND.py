import urequests as requests
import network
import json

def do_connect():
    wlan = network.WLAN(network.STA_IF) # Se crea el puerto de conexion
    wlan.active(True)   # Se activa el puerto de conexion
    if not wlan.isconnected(): #Si la conexion se establece
        print('connecting to network...')
        wlan.connect('Marisenal', 'Mariesgenial')  #Nombre de la red / Contraseña de la red
        while not wlan.isconnected(): #Esperando conexion
            pass
    print('network config:', wlan.ifconfig()) # Se obtiene las direcciones de la red (IP/netmask/gw/DNS)


do_connect() #Conectarse a internet
url = 'https://apiomarsignal.fly.dev/sendMuestra' #URL de la API
#Formato Json requerido
myjson = {
    #Despues de los dos puntos es donde va el Json a enviar
  "infosensor": {"ch1":"78","ch2":"8882","ch3":"333333","ch4":"69","ch5":"555","ch6":"6","ch7":"7","ch8":"8","ch11":"78","ch12":"8882","ch13":"333333","ch14":"69","ch15":"555","ch16":"6","ch17":"7777777777777777777","ch81":"8"}}

myjson = json.dumps(myjson)
while True: 
    requests.post(url, data = myjson) #Mostrar la respuesta del servidor  