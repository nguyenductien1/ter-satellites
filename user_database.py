import psycopg2
import hashlib

#This function is used to convert password string to hashcode, this can be used for login and register 
def hash_password(password):
    password = password.encode('utf-8')
    password_hash = hashlib.md5(password)
    return str(password_hash.hexdigest())

#Check user Existing when resgister
def checkUserExisting(username):
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    query = "select count(user_name) from user_ext where user_ext.user_name = "+"'"+username+"'"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] 

#Create a new user
def createUser(username, password):
    username = username
    password = hash_password(password)
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")

    result = 0
    if checkUserExisting(username)>=1:
        result = -1
    if checkUserExisting(username)==0:
        query = """INSERT INTO user_ext(user_name, pass_word) VALUES (%s, %s);"""
        value_insert = (str(username), str(password))
        cursor = connection.cursor()
        cursor.execute(query, value_insert)
        connection.commit()
        result = 1
    return result

#For login, if return 1 login with success, -1 fail   
def login(username, password):
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    password = hash_password(password)
    query = ("select count(user_name) from user_ext where user_ext.user_name = "+"'"+username+"'" +
                " and pass_word = " +"'"+password+"'")
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    if result[0] == 1:
        return 1
    if result[0] == 0:
        return -1
def getIDbyUserName(username):
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    query = ("select id from user_ext where user_ext.user_name = "+"'"+username+"'")
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0]


#Push infos of tuile to database
def insertTuileInfo(lonMin,lonMax, latMin, latMax, name):
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    query = """INSERT INTO tuile(lon_min, lon_max, lat_min, lat_max, name) VALUES (%s, %s, %s, %s, %s);"""
    value_insert = (lonMin,lonMax, latMin, latMax, name)
    cursor = connection.cursor()
    cursor.execute(query, value_insert)
    connection.commit()

#get infos of tuile from database
def getTuileInfo(nomTuile):
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    query = "select id_tuile,lon_min, lon_max, lat_min, lat_max from tuile where tuile.name  = '"+nomTuile+"';"
    value_insert = nomTuile
    cursor = connection.cursor()
    cursor.execute(query, value_insert)
    result = cursor.fetchone()
    return result

#Push infos about sensing date to database    
def insertTuileSensingDate(date,id_tuile):
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    query = """INSERT INTO sensing_date(date, id_tuile) VALUES (%s, %s);"""
    value_insert = (date,id_tuile)
    cursor = connection.cursor()
    cursor.execute(query, value_insert)
    connection.commit()

#Get all Tuiles for list of tuiles in front end
def getAllTuiles():
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    query = "select name from tuile;"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#Get all date of a tuile 
def getDateByTuile(tuile):
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    query = "select date from tuile, sensing_date where tuile.id_tuile = sensing_date.id_tuile and tuile.name = '"+tuile+"';"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result   

#Put file link to database
def putInfosFiles(date, fileTiff, fileCSV, fileJSON, UserID):
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    query = ("""INSERT INTO user_file(id_user, link_file, date_created) 
            VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s) ;""")
    value_insert = (UserID,fileTiff,date,UserID,fileJSON,date,UserID,fileCSV,date)
    cursor = connection.cursor()
    cursor.execute(query, value_insert)
    connection.commit()

def getFilesByDate(date, userID):
    connection = psycopg2.connect(database="ter", user="dtn", password="pwpw")
    query = "select id_file, link_file from user_file where user_file.id_user ="+ str(userID)+ " and user_file.date_created = '"+date+"';"
    print(query)
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result
