from typing import List
import paramiko

from noel.types import Film

def save_to_json(local_file: str, films: List[Film]) -> None:
    with open(local_file, "w+") as output_file:
        output_file.write("[")
        for i in range(len(films)):
            output_file.write(films[i].toJson())
            if i != len(films)-1:
                output_file.write(",")
        output_file.write("]")

def make_connection(userhost: str, password: str) -> paramiko.SFTPClient:
    [user, host] = userhost.split("@")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=password)
    sftp = client.open_sftp()
    return sftp

def upload_json(con: paramiko.SFTPClient, local_file: str, distant_file: str) -> None:
    con.put(local_file, distant_file)