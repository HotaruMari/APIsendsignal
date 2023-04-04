#Library import
from fastapi import FastAPI
#Config import
import mysql.connector
from pydantic import BaseModel
import json

class infosensor(BaseModel):
    infosensor: dict
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

def converttosql(infor):
    print(type(infor.infosensor))
    infor=infor.infosensor
    #infor = json.loads(infor.infosensor)
    i = 0
    sentenciainicial = 'INSERT INTO libreria_signal (ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8) VALUES ('
    for v,k in infor.items():
        i = i+1   
        if i<8:
            sentenciainicial = sentenciainicial + k +','
        elif i == 8:
            sentenciainicial = sentenciainicial + k +'),('
            i=0
    sentenciainicial = sentenciainicial[:-2] +';'
    return sentenciainicial

#API Routes
@app.post('/sendMuestra')
async def sendMuestra(informacion:infosensor):
    print(informacion)
    data = converttosql(informacion)
    execute(data)
    respuesta = dict()
    try:
        res = cursor.fetchall()
    
        for x in range(len(res)):
            respuesta[f'{x}']=res[x]

    except:
        pass
    conn.commit( )
    respuesta['data']=informacion
    return respuesta

@app.get('/getMuestra')
async def getMuestra():
    execute ("SELECT * FROM libreria_signal;")
    response = [x for x in cursor]
    return {"respuesta":response} 
@app.get("/")
async def home():
    return {"respuesta":"API funcionando"}