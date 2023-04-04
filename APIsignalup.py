#Library import
#La verdad no idea de cual base de datos es pero fue la primera con la que se realizaron pruebas :D
from fastapi import FastAPI
import numpy as np
#Config import
import mysql.connector
# Guardar las credenciales de la base de datos a usar
cred = {
   'HOST': 'bmnjrjw8fttrvk80m4cp-mysql.services.clever-cloud.com',
  'DB':'bmnjrjw8fttrvk80m4cp',
  'USER':'ux5kkgzfupavbhwi',
  'PORT':'3306',
  'PASSWORD':'esjMYCcpSdyg0qPvMYtj'
}

conn = mysql.connector.connect(
    host=cred['HOST'],
    user=cred['USER'],
    password=cred['PASSWORD'],
    port=cred['PORT'])
  
cursor = conn.cursor(buffered=True)
execute = cursor.execute
execute("USE bmnjrjw8fttrvk80m4cp;")
#Setup
app = FastAPI()

def converttosql(info):
    datos=infor.infosensor
        #Iniciación de sentencia SQL
    sentenciainicial = 'INSERT INTO libreria_signal (ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8,ch9,ch10,ch11,ch12,ch13,ch14,ch15,ch16) VALUES '
    senal=[]
    keys=[]
    #Extracción de valores y llaves
    for key,value in datos.items():
        senal.append(value)
        keys.append(key)
    #Conversión a tipo array para mejor manejo
    senal = np.array(senal)
    keys = np.array(keys)
    #Arreglo para obtener la sentencia SQL
    orden = np.zeros(senal.shape)
    for i in range(len(keys)):
        lugarenlatabla=int(keys[i][2:])     #Lugar el arreglo para la sentencia SQL
        orden[lugarenlatabla]=senal[np.where(keys=="Ch"+str(lugarenlatabla))[0]]  #Lugar de los datos según el Json enviado
    # Arreglo de sentencia SQL
    for j in range(np.shape(orden)[1]):
        valores= "("
        for item in range(16):
            valores=valores+str(orden[item,j])+","
        valores=valores[:-1]+"),"
        sentenciainicial=sentenciainicial+valores

    sentenciainicial = sentenciainicial[:-1] +';'  #Sentencia SQL final'
    return sentenciainicial

#API Routes
@app.post('/sendMuestra')
async def sendMuestra(infodelsensor):
    data = converttosql(infodelsensor)
    execute(data)
    respuesta = dict()
    try:
        res = cursor.fetchall()
    
        for x in range(len(res)):
            respuesta[f'{x}']=res[x]

    except:
        pass
    conn.commit( )
    respuesta['data']=infodelsensor
    return respuesta


@app.get("/")
async def home():
    return {"respuesta":"Hola mundo OwO"}

