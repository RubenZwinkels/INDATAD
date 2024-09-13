import api_caller
import db_writer
import db_reader
import ssh_connector
import psycopg2

host = "145.97.16.170"
username = "s1149334"
password = "s1149334"

#tijdelijk omdat server niet werkt
video_ids = [
    "-reddWy7dig",
    "7CBfCW67xT8&rco=1",
    "kNfKCM92OWM"
]

def main():
    # db_writer.drop_tables()
    db_writer.create_table()
    # data = api_caller.get_video_info(video_ids[0])
    # db_writer.insert_video_data_into_db(data)

    # video_ids2 = ssh_connector.get_video_ids(host, username, password)
    # for video_id in video_ids2:
    #     statistics = api_caller.get_video_info(video_id)
    #     db_writer.insert_video_data_into_db(statistics)

    fetched_video_ids = db_reader.get_video_ids()
    for id in fetched_video_ids:
        print(id)


if __name__ == "__main__":
    main()