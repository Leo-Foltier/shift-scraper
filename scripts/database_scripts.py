import mysql.connector

def database_connect(settings): #Connects to database

    db = mysql.connector.connect(
        host = settings['dbhost'],
        user = settings['dbusername'],
        passwd = settings['dbpassword'],
        database = settings['dbschema']
        )

    my_cursor = db.cursor()
    return(my_cursor,db)

def check_exists(week_beginning,settings): #Checks if week already exists in database

    db_cursor,db = database_connect(settings)

    db_cursor.execute("SELECT * FROM tips WHERE week_beginning = %s;",[week_beginning])

    for exists in db_cursor:

        if exists != None:

            return True

        return False

def modify_tips(created,week_beginning,week_tips,settings): #Modifies tips in database for that week

    db_cursor,db = database_connect(settings)

    if created == True:
        db_cursor.execute("UPDATE tips SET tips = %s WHERE week_beginning = %s",[week_tips,week_beginning])
    else:
        db_cursor.execute("INSERT INTO tips VALUES (%s,%s)",[week_beginning,week_tips])

    db.commit()
    db.close()

def modify_hours(created,week_beginning,sm_hours,w_hours,settings): #Modifies hours in database for that week

    db_cursor,db = database_connect(settings)

    if created == True:
        db_cursor.execute("UPDATE hours SET sm_hours = %s, w_hours = %s WHERE week_beginning = %s",[sm_hours,w_hours,week_beginning])
    else:
        db_cursor.execute("INSERT INTO hours VALUES (%s,%s,%s)",[week_beginning,sm_hours,w_hours])

    db.commit()
    db.close()

def modify_schedule(created,week_beginning,day_,sm_start,sm_end,w_start,w_end,holiday,settings): #Modifies schedule in database for that day in week

    db_cursor,db = database_connect(settings)

    if created == True:
        db_cursor.execute("UPDATE schedule SET sm_start = %s, sm_end = %s, w_start = %s, w_end = %s, holiday = %s WHERE week_beginning = %s AND day = %s",[sm_start,sm_end,w_start,w_end,holiday,week_beginning,day_])

    else:
        db_cursor.execute("INSERT INTO schedule VALUES (%s,%s,%s,%s,%s,%s,%s)",[week_beginning,day_,sm_start,sm_end,w_start,w_end,holiday])
    
    db.commit()
    db.close()