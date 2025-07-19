
import re
import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time




#https://k-hentai.org/?search=fav%3A27549

# fav_user_id = '27549'
#
# def fetch_gallery_info_http(def_fav_user_id):
#     def_url = f"https://k-hentai.org/?search=fav%3Aasd"
#
#     print(def_url)
#
#     html = requests.get(def_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5).text
#
#
#     print(html)
#
#     # def_m = re.search(r'const gallery\s*=\s*({.*?});', html, re.DOTALL)
#     # if not def_m:
#     #     raise RuntimeError("CANT NOT FIND GALLERY INFO")
#     # obj = def_m.group(1)
#     #
#     # try:
#     #     return json.loads(obj)
#     # except json.JSONDecodeError:
#     #     fixed = re.sub(r'(\w+):', r'"\1":', obj).replace("'", '"')
#     #     return json.loads(fixed)
#
#
#
# info = fetch_gallery_info_http(fav_user_id)







