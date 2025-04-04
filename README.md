# **Callisto**
네이버 치지직(CHZZK) 플랫폼 스트리머의 라이브 영상을 자동으로 녹화합니다.

네이버 치지직 API에서 1분마다 방송 상태를 확인하여 라이브 영상 녹화를 시작합니다.

녹화 중에는 10초마다 방송 상태를 확인하여 자동으로 녹화를 중단합니다.

녹화가 끝난 후에는 `.ts` `.lock` 파일이 생성됩니다.

최초 녹화본은 실제 녹화된 시간이 아닌 스트리머가 방송한 전체 시간으로 표시되는 문제가 있습니다.

callisto-ffmpeg 컨테이너에서 5분마다 `.lock` 파일을 확인하여 이를 보정하는 작업을 시작합니다.

작업이 끝나면 `.ts` `.lock` 파일은 삭제되며 최종적으로 `.mp4` 가 저장됩니다.

## **Prerequisites**
- Streamlink 6.7.4
- FFmpeg
- Python 3.12.2

## **Environment Variables**
| ENV Name | Description |
| --- | --- |
| `CHANNEL_ID`| 치지직 채널 고유 ID |
| `NID_AUT` |  NID_AUT 쿠키값 |
| `NID_SES` | NID_SES 쿠키값 |

NID_AUT, NID_SES 값은 네이버 [치지직](https://chzzk.naver.com/) 로그인 후, F12 -> 상단탭 Application -> 좌측 Cookies -> NID_AUT, NID_SES 값을 복사하여 입력