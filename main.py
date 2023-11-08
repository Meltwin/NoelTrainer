from argparse import ArgumentParser
from noel.scrapping import parse_xml_distant
from noel.selecting import select_programs
from noel.ftp import make_connection, save_to_json, upload_json
from noel.mending import repare_UTF8
from getpass import getpass
from requests import get
import json

XML_TV_ENDPOINT = 'https://xmltv.ch/xmltv/xmltv-tnt.xml'
STOPWORD_ENDPOINT = 'https://countwordsfree.com/stopwords/french/txt'
CUSTOM_STOPWORD_ENDPOINT = 'https://noel.zelbu.fr/api/config/stopwords.php'
LOCAL_FILE = "./temp/scrapped_data.json"
DISTANT_FILE = "www/noel/api/film/scrapped_data.json"
DB_UPDATER = "https://noel.zelbu.fr/api/film/updateDB.php"


def update_bdd():
    # Scrap the data from online
    program = parse_xml_distant(XML_TV_ENDPOINT)
    films = select_programs(program, STOPWORD_ENDPOINT, CUSTOM_STOPWORD_ENDPOINT)
    save_to_json(LOCAL_FILE, films)

    # Upload and update db
    host = input("Enter user@host : ")
    psw = getpass("Enter password : ")
    con = make_connection(host, psw)
    upload_json(con, LOCAL_FILE, DISTANT_FILE)
    con.close()

    # Update DB
    data = get(DB_UPDATER).content
    try:
        data = json.loads(data)
    except:
        ...
    finally:
        print(data)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("cmd", choices=["update", "train", "repareutf"])
    args = parser.parse_known_args()[0]

    match args.cmd:
        case "update":
            update_bdd()
        case "repareutf":
            repare_UTF8()