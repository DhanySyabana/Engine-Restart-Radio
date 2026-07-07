import os
import time
import requests
import logging
from settings.Config import FOLDERS_TO_CHECK, FOLDER_TO_CONTAINERS, TELEGRAM_CONFIG, CHECK_PARAMETERS

def send_telegram_alert(alert_folders, time_limit, min_files):
    if not alert_folders:
        print("Tidak ada folder yang butuh alert Telegram.")
        return
    
    text ="⚠️  ⚠️  ⚠️ SERVER RADIO 2 ⚠️  ⚠️ ⚠️  ⚠️"
    text += "\n List Channel Streaming OFF :\n"

    for idx, folder in enumerate(alert_folders, 1):
        text += f"\n{idx}. {folder}"

    text += f"\n🗓️: {time.strftime('%d %B %Y %H:%M:%S')}"
    text += f"\n\n#######################"
    
    apiURL = f'https://api.telegram.org/bot{TELEGRAM_CONFIG["TOKEN"]}/sendMessage'
    try:
        response = requests.post(apiURL, json={
            'chat_id': TELEGRAM_CONFIG["CHAT_ID"],
            'message_thread_id': TELEGRAM_CONFIG["TOPIC_ID"],
            'text': text
        })
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Telegram alert: {e}")
    else:
        logging.info(f"Telegram alert sent: {response.text}")


def check_mp4_files(directory, folders_to_check, time_limit=1800, min_files=2):
    current_time = time.time()
    alert_folders = []
    
    for folder in folders_to_check:
        folder_path = os.path.join(directory, folder)
        print("Checking", folder_path)
        if not os.path.isdir(folder_path):
            continue
        
        mp4_files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]
        recent_files = [f for f in mp4_files if current_time - os.path.getmtime(os.path.join(folder_path, f)) <= time_limit]
        print("Recent files:", len(recent_files))
        if len(recent_files) < min_files:
            alert_folders.append(folder)
    
    if alert_folders:
        print("ALERT! The following folders have less than", min_files, "MP4 files in the last", time_limit//60, "minutes:")
        # for folder in alert_folders:
        #     print("-", folder)
        send_telegram_alert(alert_folders, time_limit, min_files)
    else:
        print("All folders have sufficient MP4 files.")

if __name__ == "__main__":
    print("FILE CHECKER at", time.strftime("%Y-%m-%d %H:%M:%S"))
    check_mp4_files(CHECK_PARAMETERS["directory"], FOLDERS_TO_CHECK, CHECK_PARAMETERS["time_limit"], CHECK_PARAMETERS["min_files"])
    exit(0)
