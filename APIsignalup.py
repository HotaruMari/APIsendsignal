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
  
cursor = conn.cursor()
execute = cursor.execute

#Setup
API = FastAPI()

def converttosql(info):
    return 'SELECT * FROM signalmari ;'

#API Routes
@API.post('/sendMuestra')
async def sendMuestra(infodelsensor):
    data = converttosql(infodelsensor)
    respuesta = execute(data)
    conn.commit( )
    respuesta['data']=infodelsensor
    return respuesta

#api.com/sendMuestra, [
#   {'ch1':1.2,'ch2':},
#   {'ch1':1.2,'ch2':},
#   {'ch1':1.2,'ch2':},]