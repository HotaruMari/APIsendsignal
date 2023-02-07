#Library import

from fastapi import FastAPI

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
    return 'INSERT INTO signalmari(CH1,CH2,CH3) VALUES (5.5,5.4,5.3),(45.0,41.2,46.3);'

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

@app.get('/getMuestra')
async def getMuestra():
    execute ("SELECT * FROM signalmari;")
    response = [x for x in cursor]
    return {"respuesta":response} #*llora en no programador*
@app.get("/")
async def home():
    return {"respuesta":"Hola mundo OwO"}


#apisendsignal.:up.railway.app/sendMuestra, [
#   {'ch1':1.2,'ch2':},zh
#   {'ch1':1.2,'ch2':},
#   {'ch1':1.2,'ch2':},]