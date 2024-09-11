import api_caller
import db_writer
import ssh_connector

host = "145.97.16.22"
username = "s1149334"
password = "s1149334"

#tijdelijk omdat server niet werkt
video_ids = [
    "-reddWy7dig",
    "7CBfCW67xT8&rco=1",
    "kNfKCM92OWM"
]

def main():
    db_writer.create_table()

    data = api_caller.get_video_metadata(video_ids[0])
    db_writer.insert_video_into_db(data)

if __name__ == "__main__":
    main()