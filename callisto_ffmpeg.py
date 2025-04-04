import os
import time
import subprocess
import logging

logger = logging.getLogger('timestamp_logger')
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

DIR = "/home/callisto/CHZZK-VOD/"

def fix_timestamp():
    while True:
        lock_files = sorted([f for f in os.listdir(DIR) if f.endswith('.lock')])  
        if lock_files:
            logger.info(f"감지된 lock 파일 목록: {', '.join(lock_files)}")
            for lock_file in lock_files:
                lock_file_path = os.path.join(DIR, lock_file)
                with open(lock_file_path, 'r') as f:
                    file_name = f.read().strip()
                ts_file = os.path.join(DIR, f"{file_name}.ts")
                mp4_file = os.path.join(DIR, f"{file_name}.mp4")

                if os.path.exists(ts_file):
                    logger.info(f"타임스탬프 수정 작업 시작: {ts_file} → {mp4_file}")
                    subprocess.call(['ffmpeg', '-i', ts_file, '-c', 'copy', '-map', '0', '-reset_timestamps', '1', mp4_file])
                    os.remove(ts_file)
                    logger.info(f"원본 파일 삭제 완료: {ts_file}")

                os.remove(lock_file_path)
                logger.info(f"타임스탬프 수정 완료, lock 파일 삭제됨: {lock_file_path}")
        else:
            logger.info("변환할 파일이 없습니다. 5분 후 다시 확인합니다.")

        time.sleep(300)

if __name__ == "__main__":
    fix_timestamp()