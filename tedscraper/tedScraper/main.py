import api_caller
import db_writer
import db_reader
import ssh_connector
import time

#tijdelijk omdat server niet werkt
video_ids = [
    "-reddWy7dig",
    "7CBfCW67xT8&rco=1",
    "kNfKCM92OWM"
]
def startup():
    db_writer.create_table()
    db_writer.insert_custom_date()

def update_video_data():
    excisting_videos = db_reader.get_video_ids()
    all_videos = ssh_connector.get_video_ids()
    if len(all_videos) == 0:
        raise Exception("kan geen benodigde videos ophalen (all_videos is leeg)")

    for vid in all_videos:
        if vid in excisting_videos:
            pass
        else:
            print(f"video data van video id: {vid} toevoegen")
            new_vid = api_caller.get_video_info(vid)
            db_writer.insert_video_data_into_db(new_vid)
        print(f"video statistiek van id: {vid} updaten")
        db_writer.update_video_statistic(vid)
    print("alle video statistieken geupdate \n \n")

def main():
    start_time = time.time()
    startup()
    update_video_data()

    print(f"Het script duurde {time.time() - start_time} seconden.")
if __name__ == "__main__":
    main()