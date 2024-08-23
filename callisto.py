import re
import requests
import time
import subprocess
import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('streamlink_logger')
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

CHANNEL_ID = os.getenv('CHANNEL_ID')
NID_AUT = os.getenv('NID_AUT')
NID_SES = os.getenv('NID_SES')

CHZZK_API = f'https://api.chzzk.naver.com/service/v3/channels/{CHANNEL_ID}/live-detail'

headers = {  
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            }

special_chars_remover = re.compile(r'[\\/:*?\"<>|]')

def check_naver_status():
    response = requests.get(CHZZK_API, headers=headers)
    if response.status_code == 200 and response.json().get('content', {}) != None:
        return response.json().get('content', {}).get('status')
    elif response.json().get('content', {}) == None:
        logger.info("This channel hasn't streamed in a long time.")
        return None
    else:
        logger.error(f"Error Status code: {response.status_code} Response: {response.text}")
        return None

def run_streamlink(CHANNEL_ID):
    try:
        logger.info(f"치지직 라이브 녹화를 시작합니다!")
        response = requests.get(CHZZK_API, headers=headers)
        title = response.json().get('content', {}).get('liveTitle')
        cleaned_live_title = special_chars_remover.sub('', title.rstrip())
        channel = response.json().get('content', {}).get('channel').get('channelName')
        current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        suffix = f"{current_time}_{channel}_{cleaned_live_title}"
        subprocess.call(['streamlink', '--ffmpeg-copyts', '--progress', 'no', f'https://chzzk.naver.com/live/{CHANNEL_ID}', 'best', '--http-cookie', f'NID_AUT={NID_AUT}', '--http-cookie', f'NID_SES={NID_SES}', '--output', f'/home/callisto/CHZZK-VOD/{suffix}.mp4'])
    except Exception as e:
        logger.error(f"Streamlink 실행 중 오류 발생: {e}")

def check_stream():
    while True:
        naver_status = check_naver_status()     
        if naver_status == 'OPEN':
            response = requests.get(CHZZK_API, headers=headers)
            title = response.json().get('content', {}).get('liveTitle')
            channel = response.json().get('content', {}).get('channel').get('channelName')
            logger.info(f'[치지직 라이브] {channel}님의 방송이 시작되었습니다!')
            logger.info(f'방송 제목: {title}')
            logger.info(f'https://chzzk.naver.com/live/{CHANNEL_ID}')
            run_streamlink(CHANNEL_ID)
            while check_naver_status() == 'OPEN':
                logger.info("Checking for close status")
                time.sleep(10)
        else:
            logger.info("OFFLINE! Checking again in 1 minute.")
            time.sleep(60)

if __name__ == "__main__":
    check_stream()
