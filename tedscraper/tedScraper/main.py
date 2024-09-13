import api_caller
import db_writer
import db_reader
import ssh_connector
import psycopg2
import time

#tijdelijk omdat server niet werkt
video_ids = [
    "-reddWy7dig",
    "7CBfCW67xT8&rco=1",
    "kNfKCM92OWM"
]

def update_video_data():
    excisting_videos = db_reader.get_video_ids()
    all_videos = ssh_connector.get_video_ids()
    for vid in all_videos:
        if vid in excisting_videos:
           print(f"video id: {vid} al bestaand in db")
        else:
            new_vid = api_caller.get_video_info(vid)
            db_writer.insert_video_data_into_db(new_vid)
            print(f"added video with id: {vid} to db")

def main():
    start_time = time.time()

    # db_writer.drop_tables()
    db_writer.create_table()

    db_reader.get_video_statistic("0G2U0R0hOCU")
    # update_video_data()

    print(f"Het script duurde {time.time() - start_time} seconden.")
if __name__ == "__main__":
    main()