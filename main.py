from data_collection import api_caller, db_reader, db_writer, ssh_connector
import time
from popularity import popularity_analyser
from datetime import date
def startup():
    db_writer.create_table()
    db_writer.insert_custom_date()

def update_video_data():
    excisting_videos = db_reader.get_video_ids()
    all_videos = ssh_connector.get_video_ids()
    if len(all_videos) == 0:
        raise Exception("kan geen benodigde videos ophalen (all_videos is leeg)")

    vid_counter = 0
    for vid in all_videos:
        vid_counter += 1
        if vid in excisting_videos:
            #temp
            # db_writer.get_and_insert_sentiment(vid)
            pass
        else:
            print(f"video data van video id: {vid} toevoegen")
            new_vid = api_caller.get_video_info(vid)
            db_writer.insert_video_data_into_db(new_vid)
            db_reader.get_transcription_by_video_id(vid)
            db_writer.get_and_insert_sentiment(vid)
        print(f"video statistiek van id: {vid} updaten ({vid_counter}/{len(all_videos)})")
        db_writer.update_video_statistic(vid)
        video_data = db_reader.get_recent_video_statistic(vid)
        db_writer.insert_popularity(video_data, db_reader.get_id_by_date(date.today()))
        print("")
    print("alle video statistieken geupdate \n")

def main():
    start_time = time.time()
    startup()
    update_video_data()

    print(f"Het script duurde {time.time() - start_time} seconden.")
    db_writer.insert_deploy(time.time() - start_time)

if __name__ == "__main__":
    main()