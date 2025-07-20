

# <p style="color: red;">NSFW WARNING</p> 

# K-Hentai Gallery Downloader

K-Hentai 사이트의 갤러리 ID를 입력하면 페이지 내 이미지 파일을 일괄 다운로드해 주는 파이썬 CLI 스크립트입니다.  
멀티스레드 병렬 다운로드로 속도 최적화가 되어 있으며, 여러 갤러리 일괄 처리도 지원합니다.

---

## Main Function

- `fetch_gallery_info_http(gallery_id)`  
  - HTTP 요청만으로 **갤러리 메타 정보**(파일 수, 제목, 태그 등) 추출  
- `GalleryDownloader` 클래스  
  - `get_tags()` : 태그 목록 반환  
  - `get_img_urls()` : 이미지 URL 리스트 반환  
  - `download(n, m, workers, img_type)` : 페이지 범위(`n`~`m`)를 지정해 병렬 다운로드  
- **CLI 모드**  
  - 단일 ID 또는 쉼표로 구분된 여러 ID 일괄 다운로드
  - 현재 시스템의 CPU 코어수의 3배의 멀티스레드 설정 (최대 30개, 차단방지)
  - 다운로드 소요 시간 측정 및 출력  


---

## Setup and Download

1. 파이썬 3.7 이상 설치
   - 설치 여부 확인:
     ```bash
     python --version
     ```
   - 설치가 안 되어 있으면 [python.org](https://www.python.org/downloads/)에서 다운로드 후 설치
2. 가상환경 생성 및 활성화 (권장)
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows
    
   pip install requests kivy # GUI it's optinal who wanna use GUI
   
   
   
## Usage

### Supported Input Formats
- **단일 숫자 ID**: `3445399`
- **전체 URL**: `https://k-hentai.org/r/3445399`
- **공백 구분 리스트**: `3445399 https://k-hentai.org/r/3445399`
- **콤마 구분 리스트**: `https://k-hentai.org/r/3445399,3446020`


### CLI Mode
1. 가상환경 활성화 (위 준비 단계 참고)
2. 스크립트 실행:
   ```bash
   python img_download.py
   ```
3. 프롬프트에 따라 갤러리 ID 입력:
    단일 ID 일땐 다운받을 페이지를 수동으로 지정해야합니다.
4. ID 형식 말고도 전체 갤러리 url도 입력 할 수 있습니다.
   ```text
   Enter gallery ID or list (comma separated): 3445399,3446020
   ```
4. 다운로드 범위 설정 (옵션):
   ```text
   Mode: all         # 전체 페이지 다운로드
   Mode: user_input  # 직접 범위 지정, all 이 이닌 모드에 대해서, 인풋 n ~ m
   page from: n      # 자연수
   page to: m        # if m>n, 자동으로 m = max_page
   ```
5. 다운로드 완료 후, 각 갤러리 ID명 폴더에 저장된 이미지를 확인


### Optional Parent Directory

다운로드 실행 시, 사용자 입력을 받아 추가로 부모 폴더를 생성할 수 있는 옵션을 제공합니다.

- **프롬프트**: 
  ```
  Make new dir (leave empty for not make dir):
  ```
- **동작**:
  - 아무 입력 없이 엔터를 누르면, 현재 디렉터리에 각 갤러리 ID 폴더만 생성하여 다운로드합니다.
  - 폴더명을 입력하고 엔터 누르면, 해당 이름으로 새로운 폴더를 생성(`mkdir`) 후 그 폴더로 이동(`cd`)하여, 내부에 각 갤러리 ID 폴더를 생성하고 이미지를 다운로드합니다.
- **예시**:
  ```text
  Make new dir (leave empty for not make dir): my_downloads
  ```
  다운로드는 다음과 같은 구조로 저장됩니다:
  ```
  my_downloads/
  ├── 3445399/
  └── 3446020/
  ```

 
### Error Handling Example

다운로드 중 특정 갤러리에서 메타 정보 파싱에 실패했을 때, 터미널에 다음과 같이 출력되고 사용자 입력을 받습니다:

```text
Error occurred on gallery 1477273: CANT NOT FIND GALLERY INFO
오류가 발생했습니다. 계속하시겠습니까? (y/n): y
Skipping gallery 1477273 and continuing.
```

- `y`를 입력하면 해당 갤러리를 건너뛰고 다음 갤러리를 계속 처리합니다.
- `n`을 입력하면 작업을 중단하고 프로그램이 종료됩니다.




<p>
  <img src="img_src/cb304b165663134eb98a2aa1b82556836cc0d17c.webp" alt="Gallery Preview" style="width:50%; height:auto;" />
</p>
