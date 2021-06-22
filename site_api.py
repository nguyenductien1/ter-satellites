from fastapi import FastAPI #import class FastAPI() from library fastapi
from pydantic import BaseModel
import main_user
import user_database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() #constructor and  app

origins = [
    "http://localhost",
    "http://localhost:80",
    "https://nguyenductien.online",
    "http://nguyenductien.online",
    "https://localhost",
    "https://localhost:80"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InfosCalculIndice(BaseModel):
    nomTuile:str
    dateAcquisition:str
    heureAcquisition:str
    nomIndice:str
    lonMin: float
    lonMax: float
    latMin: float
    latMax: float
    interp: str
    imgFormat: str
    lmin: float
    lmax: float
    imgWidth: float
    imgHeight: float
    username: str
class InfosLogin(BaseModel):
    username: str
    password: str
class InfosTuile(BaseModel):
    tuile:str
class InfosHistory(BaseModel):
    username:str
    date: str

@app.post("/calcul-indice")
async def calcul_indice(infos: InfosCalculIndice):
    img = main_user.calcul_api(infos.nomTuile, infos.dateAcquisition,infos.nomIndice,infos.lonMin,
    infos.lonMax,infos.latMin,infos.latMax,infos.interp, infos.imgFormat, infos.lmin, infos.lmax, infos.imgWidth, infos.imgHeight, infos.username)
    return {"img":img}
@app.post("/login")
async def login(infos: InfosLogin):
    status = user_database.login(infos.username, infos.password)
    userID = user_database.getIDbyUserName(infos.username)
    return {"stt":status, "userID":userID}
@app.post("/register")
async def register(infos: InfosLogin):
    stt = user_database.createUser(infos.username, infos.password)
    return {"stt":stt}
@app.get("/get-tuile")
async def getTuile():
    tuiles = user_database.getAllTuiles()
    return tuiles
@app.post("/get-dates-tuile")
async def getDateTuile(infos: InfosTuile):
    result = user_database.getDateByTuile(infos.tuile)
    return result

@app.post("/get-tuile-infos")
async def getTuileInfos(infos: InfosTuile):
    result = user_database.getTuileInfo(infos.tuile)
    return {"id_tuile":result[0], "lonMin":result[1], "lonMax":result[2], "latMin":result[3], "latMax":result[4]}

@app.post("/get-files-history")
async def getFileHistory(infos: InfosHistory):
    userID = user_database.getIDbyUserName(infos.username)
    result = user_database.getFilesByDate(infos.date, userID)
    listTiff = []
    listCSV = []
    listJSON = []
    for i in range(0, len(result)):
        linkNoSpace = result[i][1].replace(" ", "")
        if result[i][1].replace(" ", "")[-3:] == 'tif':
            listTiff.append(result[i])
        elif result[i][1].replace(" ", "")[-3:] == 'csv':
            listCSV.append(result[i])
        elif result[i][1].replace(" ", "")[-4:] == 'json':
            listJSON.append(result[i])
            
    return_result = {"tif":listTiff, "csv":listCSV, "json":listJSON}

    return return_result