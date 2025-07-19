
import re
import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class GalleryDownloader:
    def __init__(self, gallery_id):
        gid = str(gallery_id).split("/")[-1]
        self.gallery_id = gid
        self.info = fetch_gallery_info_http(gid)

    def get_tags(self):
        # Return list of tag names
        return [tag_entry['tag'][1] for tag_entry in self.info.get('tags', [])]

    def get_img_urls(self):
        # Return list of image URLs
        return [file_entry['image']['url'] for file_entry in self.info.get('files', [])]

    def download(self, n, m, workers=None, img_type=None):
        # Perform the download with default worker count if not provided
        urls = self.get_img_urls()
        if workers is None:
            import os
            workers = os.cpu_count() * 5
        download_images_parallel(urls, self.gallery_id, n, m, workers, img_type=img_type)

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

class Main_Activity():
    def Download(self, url, mode, ext_type):

        # url = "3446017"

        if url.isdigit():
            url = "https://k-hentai.org/r/" + str(url)

        elif url in "," or url in " ":
            gallerys = url.split(",")
            for i in gallerys:
                pass


        else:
            pass

        gallery_id = url.split("/")[-1]
        # Initialize downloader instance
        downloader = GalleryDownloader(gallery_id)

        info = downloader.info

        print("-------------------------")
        print("FILE INFO")
        print("-------------------------")
        print(f'URL: ｢{str(url)}｣')
        print(f'GALLERY ID: ｢{gallery_id}｣')
        print(f'TITLE: ｢{info["title"]}｣')
        print(f'PAGES: ｢{info["filecount"]}｣')
        print("-------------------------")
        print(f'TAGS: ｢{", ".join(downloader.get_tags())}｣')
        print("-------------------------")
        print("BEFORE DOWNLOAD . . . ")
        print("-------------------------")


        if mode == "all":
            n = 1
            m = info["filecount"]
        else:

            n = int(input('page from: '))
            m = int(input('page to: '))

            if m > info["filecount"]:
                m = info["filecount"]
                print("page to can't exceed the total page")
                print("page to set to end of gallery")

        workers = os.cpu_count() * 5
        print(f'TCP THREADS: ｢{workers}｣')
        start_time = time.time()
        # Download pages
        downloader.download(n, m, workers, img_type=ext_type)
        end_time = time.time()
        print(f"DOWNLOAD COMPLETE IN {end_time - start_time:.2f} SECONDS")

if __name__ == "__main__":



    Main_Activity().Download("3446631", 'all', 'jpg')


