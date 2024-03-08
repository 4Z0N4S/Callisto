# **Callisto**
네이버 치지직(CHZZK) 플랫폼 스트리머의 라이브 영상을 자동으로 녹화합니다.

네이버 치지직 API에서 5분마다 방송 상태를 확인하여 라이브 영상 녹화를 시작합니다.

녹화 중에는 30초마다 방송 상태를 확인하여 자동으로 녹화를 중단합니다.

## **Prerequisites**
- Streamlink
- [CHZZK Streamlink Plugin](https://github.com/park-onezero/streamlink-plugin-chzzk)
- FFmpeg
- Python 3.12.2

## **Environment Variables**
| ENV Name | Description |
| --- | --- |
| `CHANNEL_ID`| 치지직 채널 고유 ID |
| `NID_AUT` |  NID_AUT 쿠키값 |
| `NID_SES` | NID_SES 쿠키값 |

NID_AUT, NID_SES 값은 네이버 [치지직](https://chzzk.naver.com/) 로그인 후, F12 -> 상단탭 Application -> 좌측 Cookies -> NID_AUT, NID_SES 값을 복사하여 입력