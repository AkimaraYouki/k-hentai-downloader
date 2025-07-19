
import re
import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

url = "3446017"

if url.isdigit():
    url = "https://k-hentai.org/r/" + str(url)

else:
    pass

gallery_id = url.split("/")[-1]

def fetch_gallery_info_http(def_gallery_id):
    def_url = f"https://k-hentai.org/r/{def_gallery_id}"
    html = requests.get(def_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5).text

    def_m = re.search(r'const gallery\s*=\s*({.*?});', html, re.DOTALL)
    if not def_m:
        raise RuntimeError("CANT NOT FIND GALLERY INFO")
    obj = def_m.group(1)

    try:
        return json.loads(obj)
    except json.JSONDecodeError:
        fixed = re.sub(r'(\w+):', r'"\1":', obj).replace("'", '"')
        return json.loads(fixed)

def get_tags():
    p = info["tags"]
    tag = []
    for i in range(len(p)):
        tag.append((p[i]['tag'])[1])
    return tag

def get_img_url():
    p = info["files"]
    img_url = []
    for i in range(len(p)):
        img_url.append((p[i]['image']['url']))
    return img_url

info = fetch_gallery_info_http(gallery_id)

def download_one(args):
    def_url, folder, idx, ext = args
    path = os.path.join(folder, f"{folder}_{idx}.{ext}")
    resp = requests.get(def_url, stream=True, timeout=10)
    resp.raise_for_status()
    with open(path, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)
    return path

def download_images_parallel(urls, folder, def_n, def_m, def_workers=8, img_type=None):
    os.makedirs(folder, exist_ok=True)
    target_urls = urls[def_n - 1:def_m]
    total = len(target_urls)
    print(f" TO {folder} FOLDER, DOWNLOAD {total} IMAGE (TCP THREADS={def_workers})")

    tasks = []
    with ThreadPoolExecutor(max_workers=def_workers) as exe:
        for idx, def_url in enumerate(target_urls, start=def_n):
            if img_type:
                ext = img_type
            else:
                ext = def_url.split("?")[0].split(".")[-1]
            tasks.append(exe.submit(download_one, (def_url, folder, idx, ext)))

        for future in as_completed(tasks):
            print("SAVED BY:", future.result())
    print("DONE")

print("-------------------------")
print("FILE INFO")
print("-------------------------")
print(f'URL: ｢{str(url)}｣')
print(f'GALLERY ID: ｢{gallery_id}｣')
print(f'TITLE: ｢{info["title"]}｣')
print(f'PAGES: ｢{info["filecount"]}｣')
print("-------------------------")
print(f'TAGS: ｢{", ".join(get_tags())}｣')
print("-------------------------")
print("BEFORE DOWNLOAD . . . ")
print("-------------------------")

n = int(input('page from: '))
m = int(input('page to: '))
if m > info["filecount"]:
    m = info["filecount"]
    print("page to can't exceed the total page")
    print("page to set to end of gallery")

ext_type = input('file extension (e.g. jpg, webp): ')

workers = os.cpu_count() * 5
print(f'TCP THREADS: ｢{workers}｣')
start_time = time.time()
download_images_parallel(get_img_url(), str(gallery_id), n, m, workers, img_type=ext_type)
end_time = time.time()
print(f"DOWNLOAD COMPLETE IN {end_time - start_time:.2f} SECONDS")




