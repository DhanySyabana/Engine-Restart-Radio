import os
import time
import docker
from settings.Config import FOLDERS_TO_CHECK, FOLDER_TO_CONTAINERS, CHECK_PARAMETERS

def restart_containers(containers):
    docker_api_url = 'unix://var/run/docker.sock'
    client = docker.DockerClient(base_url=docker_api_url)
    for name_container in containers:
        try:
            container = client.containers.get(name_container)
            container.restart()
            print(f"Container '{name_container}' berhasil di-restart.")
        except docker.errors.NotFound:
            print(f"Error: Container '{name_container}' tidak ditemukan.")
        except docker.errors.APIError as e:
            print(f"Error: Terjadi kesalahan API Docker - {e}")
        except Exception as e:
            print(f"Error: Terjadi kesalahan yang tidak terduga - {e}")

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
        for folder in alert_folders:
            print("-", folder)
            if folder in FOLDER_TO_CONTAINERS:
                print(f"Restarting Docker {folder} process...")
                restart_containers(FOLDER_TO_CONTAINERS[folder])
    else:
        print("All folders have sufficient MP4 files.")

if __name__ == "__main__":
    print("FILE CHECKER at", time.strftime("%Y-%m-%d %H:%M:%S"))
    check_mp4_files(CHECK_PARAMETERS["directory"], FOLDERS_TO_CHECK, CHECK_PARAMETERS["time_limit"], CHECK_PARAMETERS["min_files"])
    exit(0)