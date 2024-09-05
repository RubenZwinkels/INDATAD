import api_caller
import db_writer
import ssh_connector

host = "145.97.16.22"
username = "s1149334"
password = "s1149334"
def main():
    # db_writer.conn_db()
    video_ids = ssh_connector.get_video_ids(host, username, password)
    for id in video_ids:
        print(id)

if __name__ == "__main__":
    main()