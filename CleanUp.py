import time
import logging
from datetime import datetime, timezone
from pathlib import Path
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from settings.Config import FOLDERS_TO_CHECK, CHECK_PARAMETERS, MONGO_CONFIG

# --- Konfigurasi dari Config.py ---
BASE_STREAM_PATH = CHECK_PARAMETERS["directory"]
MAX_AGE_DAYS = int(CHECK_PARAMETERS["max_age_days"])
LOG_LEVEL = CHECK_PARAMETERS["log_level"]
STREAM_CHANNELS = FOLDERS_TO_CHECK

# --- Setup logging ---
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def get_mongo_collection():
    client = MongoClient(MONGO_CONFIG["uri"])
    db = client[MONGO_CONFIG["database"]]
    streams_col = db[MONGO_CONFIG["collection_streams"]]
    return client, streams_col


def log_deleted_file_to_db(collection, mp3_file: Path):
    update_fields = {
        "file_deleted": True,
        "file_deleted_at": datetime.now(timezone.utc),
        "file_deleted_by": "Cron CleanUp.py"
    }
    try:
        result = collection.update_one(
            {"filename": mp3_file.name},   # cocokkan berdasarkan nama file
            {"$set": update_fields}
        )
        if result.matched_count == 0:
            logger.warning(f"  [DB WARN] Dokumen tidak ditemukan di DB untuk file: {mp3_file.name}")
        else:
            logger.info(f"  [DB OK] Updated: {mp3_file.name} (matched: {result.matched_count})")
    except PyMongoError as e:
        logger.error(f"  [DB ERROR] Gagal update MongoDB: {e}")


def parse_date_from_filename(filename: str) -> float | None:
    """
    Ekstrak timestamp dari nama file format: {channel}_{MM-DD-HH-MM-SS}.mp3
    Contoh: iradio_10-10-01-20-00.mp3 → 10 Oktober jam 01:20:00
    Return: unix timestamp, atau None jika gagal parse.
    """
    try:
        stem = Path(filename).stem          # 'iradio_10-10-01-20-00'
        date_part = stem.split("_", 1)[1]   # '10-10-01-20-00'
        now = datetime.now()
        # Format: MM-DD-HH-MM-SS
        parsed = datetime.strptime(date_part, "%m-%d-%H-%M-%S")
        parsed = parsed.replace(year=now.year)  # pakai tahun sekarang
        # Kalau bulan hasil parse sudah lewat, berarti masih tahun ini
        return parsed.timestamp()
    except Exception:
        return None


def delete_old_mp3_files(directory: str, max_age_days: int, collection) -> int:
    target_dir = Path(directory)

    if not target_dir.exists():
        logger.warning(f"  [SKIP] Direktori tidak ditemukan: {directory}")
        return 0

    if not target_dir.is_dir():
        logger.warning(f"  [SKIP] Path bukan direktori: {directory}")
        return 0

    cutoff_time = time.time() - (max_age_days * 86400)  # 86400 detik = 1 hari
    deleted_count = 0

    for mp3_file in target_dir.rglob("*.mp3"):
        if mp3_file.is_file():
            # Utamakan tanggal dari nama file, fallback ke mtime
            file_timestamp = parse_date_from_filename(mp3_file.name)
            if file_timestamp is None:
                file_timestamp = mp3_file.stat().st_mtime
                logger.debug(f"  [DATE] Pakai mtime untuk: {mp3_file.name}")
            else:
                logger.debug(f"  [DATE] Pakai nama file untuk: {mp3_file.name}")

            if file_timestamp < cutoff_time:
                try:
                    mp3_file.unlink()
                    logger.info(f"  Dihapus: {mp3_file.name}")
                    log_deleted_file_to_db(collection, mp3_file)
                    deleted_count += 1
                except OSError as e:
                    logger.error(f"  Gagal menghapus {mp3_file}: {e}")

    return deleted_count


def main():
    logger.info("=" * 60)
    logger.info("  Cleanup File .mp3 - Multi Channel Radio")
    logger.info(f"  Base path       : {BASE_STREAM_PATH}")
    logger.info(f"  Batas umur file : {MAX_AGE_DAYS} hari")
    logger.info(f"  Total channel   : {len(STREAM_CHANNELS)}")
    logger.info("=" * 60)

    grand_total = 0
    mongo_client, collection = get_mongo_collection()

    try:
        for channel in STREAM_CHANNELS:
            full_path = str(Path(BASE_STREAM_PATH) / channel)
            logger.info(f"[{channel}] -> {full_path}")
            deleted = delete_old_mp3_files(full_path, MAX_AGE_DAYS, collection)
            logger.info(f"  File dihapus: {deleted}")
            grand_total += deleted
    finally:
        mongo_client.close()

    logger.info(f"  Total semua file dihapus : {grand_total}")
    logger.info("  Delete successfully")


if __name__ == "__main__":
    main()
