import paramiko

host = "145.97.16.170"
username = "s1149334"
password = "s1149334"

def get_video_ids():
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
