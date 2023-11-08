from getpass import getpass
import mysql.connector as mysql
import ftfy

def __mend_UTF8_channels(mysql):
    cursor = mysql.cursor()

    # Get all channels
    cursor.execute("SELECT * FROM channels")
    data = cursor.fetchall()

    cursor = mysql.cursor(prepared=True)
    for i in range(len(data)):
        new_text = ftfy.fix_text(str(data[i][1]))
        req = "UPDATE channels SET name = ? WHERE id = ?"
        cursor.execute(req, [new_text, data[i][0]])

def __mend_UTF8_films(mysql):
    cursor = mysql.cursor()

    # Get all channels
    cursor.execute("SELECT id, title, synopsis, icon FROM films")
    data = cursor.fetchall()

    cursor = mysql.cursor(prepared=True)
    req = "UPDATE films SET title = ?, synopsis = ?, icon = ? WHERE id = ?"
    for i in range(len(data)):
        insert_to = (
            ftfy.fix_text(str(data[i][1])),
            ftfy.fix_text(str(data[i][2])),
            ftfy.fix_text(str(data[i][3])),
            data[i][0]
        )
        cursor.execute(req, insert_to)

def repare_UTF8():
    host= input("Host: ")
    user = input("User: ")
    psw = getpass("Password: ")
    db = input("Database: ")

    co = mysql.connect(
        host=host,
        user=user,
        password=psw,
        database=db
    )
    if type(co) in [mysql.MySQLConnection, mysql.CMySQLConnection]:
        __mend_UTF8_channels(co)
        __mend_UTF8_films(co)
    else:
        print(type(co))

    co.close()


if __name__ == "__main__":
    repare_UTF8()