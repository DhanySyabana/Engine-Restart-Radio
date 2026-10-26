FOLDERS_TO_CHECK = [
    "elshintajkt",
    "kisfm",
    "genfm",
    "iradio",
    "istana",
    "mostfm",
    "mnctrijaya",
    "passfmjkt",
    "radiodms",
    "rripro",
    "rripro1",
    "rripro2",
    "rripro4",
    "rripro1ende",
    "rripro1merauke",
    "rripro1palu",
    "rripro1samarinda",
    "rripro1ambon",
    "rripro1banten",
    "rripro1kupang",
    "rripro1nabire",
    "rripro1pontianak",
    "rripro1serui",
    "smartfm",
    "sonorajkt",
    "suarasurabaya",
]

FOLDER_TO_CONTAINERS = {
    "elshintajkt": ["engine_elshintajkt_v1"],
    "kisfm": ["engine_kisfm_v1"],
    "genfm": ["engine_genfm_v1"],
    "istana": ["engine_istana_v1"],
    "iradio": ["engine_iradio_v1"],
    "mnctrijaya": ["engine_mnctrijaya_v1"],
    "mostfm": ["engine_mostfm_v1"],
    "passfmjkt": ["engine_passfmjkt_v1"],
    "radiodms": ["engine_radiodms_v1"],
    "rripro1": ["engine_rripro1_v1"],
    "rripro2": ["engine_rripro2_v1"],
    "rripro4": ["engine_rripro4_v1"],
    "rripro1ende": ["engine_rripro1ende_v1"],
    "rripro1merauke": ["engine_rripro1merauke_v1"],
    "rripro1palu": ["engine_rripro1palu_v1"],
    "rripro1samarinda": ["engine_rripro1samarinda_v1"],
    "rripro1ambon": ["engine_rripro1ambon_v1"],
    "rripro1banten": ["engine_rripro1banten_v1"],
    "rripro1kupang": ["engine_rripro1kupang_v1"],
    "rripro1nabire": ["engine_rripro1nabire_v1"],
    "rripro1pontianak": ["engine_rripro1pontianak_v1"],
    "rripro1serui": ["engine_rripro1serui_v1"],
    "smartfm": ["engine_smartfm_v1"],
    "sonorajkt": ["engine_sonorajkt_v1"],
    "suarasurabaya": ["engine_suarasurabaya_v1"],
}

# Telegram Configuration
TELEGRAM_CONFIG = {
    "TOKEN": "8213920361:AAEMpyChKoMGb_FHw5QNVI9xdySfjP-yrtk",
    "CHAT_ID": "-1002147735635",
    "TOPIC_ID": 3042
}

# MongoDB Configuration
MONGO_CONFIG = {
    "uri": "mongodb://localhost:27017",
    "database": "dl_streamings",
    "collection_streams": "streams"
}

# File checking parameters
CHECK_PARAMETERS = {
    # "directory": "/home/kuradmin/storage/radio_list",
    "directory": r"D:\Medmon\Raw-data\RADIO",
    "time_limit": 1800,  # 30 minutes in seconds
    "min_files": 2,
    "max_age_days": 2,
    "log_level": "INFO"
}
