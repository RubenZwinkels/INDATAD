import paramiko
import os
from dotenv import load_dotenv

def get_video_ids():
    load_dotenv()
    host = os.environ['VIDEO_SERVER_HOST']
    username = os.environ['VIDEO_SERVER_USERNAME']
    password = os.environ['VIDEO_SERVER_PASSWORD']
    video_ids = []

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(host, username=username, password=password)

        print("Verbonden met de SSH-server.")

        command = "cd /data/video && ls"
        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode()
        video_ids = output.splitlines()

        errors = stderr.read().decode()
        if errors:
            print(f"Fouten tijdens uitvoering: {errors}")

        ssh.close()

    except paramiko.AuthenticationException:
        print("Authenticatiefout, controleer de inloggegevens.")
    except paramiko.SSHException as sshException:
        print(f"Fout met SSH-verbinding: {sshException}")
    except Exception as e:
        print(f"Algemene fout: {e}")

    finally:
        return video_ids
