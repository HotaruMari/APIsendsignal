#Library import

from fastapi import FastAPI

#Config import
import mysql.connector
# Guardar las credenciales de la base de datos a usar
cred = {
   'HOST': 'bcvgbge8uxdbbzavvzc7-mysql.services.clever-cloud.com',
  'DB':'bcvgbge8uxdbbzavvzc7',
  'USER':'un8f9kjlapfjjrlx',
  'PORT':'3306',

  'PASSWORD':'GImp876ix8ru2YzkCtFg'
}

conn = mysql.connector.connect(
    host=cred['HOST'],
    user=cred['USER'],
    password=cred['PASSWORD'],
    port=cred['PORT'])
  
cursor = conn.cursor(buffered=True)
execute = cursor.execute
execute("USE bcvgbge8uxdbbzavvzc7;")
#Setup
app = FastAPI()

def converttosql(info):
    #Mandar un jason de 8 keys 
    return 'INSERT INTO libreria_signal (ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8) VALUES (5.5,5.4,5.3,45.0,41.2,46.3,1,2);'

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
    return {"respuesta":response} 
@app.get("/")
async def home():
    return {"respuesta":"Hola mundo OwO"}


#apisendsignal.:up.railway.app/sendMuestra, [
#   {'ch1':1.2,'ch2':},zh
#   {'ch1':1.2,'ch2':},
#   {'ch1':1.2,'ch2':},]