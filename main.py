from argparse import ArgumentParser
from noel.scrapping import parse_xml_distant
from noel.selecting import select_programs
from noel.ftp import make_connection, save_to_json, upload_json
from getpass import getpass

XML_TV_ENDPOINT = 'https://xmltv.ch/xmltv/xmltv-tnt.xml'
STOPWORD_ENDPOINT = 'https://countwordsfree.com/stopwords/french/txt'
LOCAL_FILE = "./temp/scrapped_data.json"
DISTANT_FILE = "www/noel/beta/api/film/scrapped_data.json"


def update_bdd(parser: ArgumentParser):
    host = input("Enter user@host : ")
    psw = getpass("Enter password : ")

    program = parse_xml_distant(XML_TV_ENDPOINT)
    films = select_programs(program, STOPWORD_ENDPOINT)
    save_to_json(LOCAL_FILE, films)
    con = make_connection(host, psw)
    upload_json(con, LOCAL_FILE, DISTANT_FILE)
    con.close()
    

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("cmd", choices=["update", "train"])
    args = parser.parse_known_args()[0]

    match args.cmd:
        case "update":
            update_bdd(parser)