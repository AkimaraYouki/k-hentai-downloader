from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver  # selenium-wire로 네트워크 추적
import time
from selenium.webdriver.common.by import By
import re
import json
from selenium.webdriver.chrome.options import Options

# 인풋 부분
# URL 만 들어간다.

url = "3444597"
if url.isdigit():
    url = "https://k-hentai.org/r/" + str(url)
else:
    pass

gallery_id = url.split("/")[-1]

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

def get_gallery_inline(driver):
    page_source = driver.page_source
    match = re.search(r'const gallery\s*=\s*({.*?});', page_source, re.DOTALL)
    if not match:
        return None
    gallery_js = match.group(1)
    try:
        gallery_json = json.loads(gallery_js)
    except json.JSONDecodeError:
        gallery_js_fixed = re.sub(r'(\w+):', r'"\1":', gallery_js)
        gallery_js_fixed = gallery_js_fixed.replace("'", '"')
        gallery_json = json.loads(gallery_js_fixed)
    return gallery_json

def get_tags():
    p = gallery_info.get("tags", [])
    tag = []
    for i in range(len(p)):
        tag.append((p[i]['tag'])[1])
    return tag

def get_img_url():
    p = gallery_info.get("files", [])
    img_url = []
    for i in range(len(p)):
        img_url.append((p[i]['image']['url']))
    return img_url

def delay(n):
    for i in range(n):
        time.sleep(1)
        print(i+1)

driver.get(url)
gallery_info = get_gallery_inline(driver)

print("file info")
print("-------------------------")
print(str(url))
print(gallery_id)
print(gallery_info.get("title"))
print(gallery_info.get("filecount"))
print("-------------------------")
print(get_tags())
print("-------------------------")
print(get_img_url())
