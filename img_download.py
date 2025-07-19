"""
KHentai gallery downloader module.
Provides classes and functions to fetch gallery metadata,
extract image URLs, and download images in parallel with error handling.
"""
import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys

# Encapsulates operations for a single gallery:
# - Fetch metadata (info)
# - Provide tags and image URL lists
# - Download selected pages

class GalleryDownloader:

    def __init__(self, gallery_id):
        # Normalize gallery_id to its numeric component
        gid = str(gallery_id).split("/")[-1]
        self.gallery_id = gid
        self.info = fetch_gallery_info_http(gid)

    # Return a list of tag names from gallery metadata
    def get_tags(self):
        # Return list of tag names
        return [tag_entry['tag'][1] for tag_entry in self.info.get('tags', [])]

    # Return a list of full image URLs for this gallery
    def get_img_urls(self):

        return [file_entry['image']['url'] for file_entry in self.info.get('files', [])]

    # Download images from page n to m using a thread pool
    def download(self, n, m, workers=None, img_type=None):

        urls = self.get_img_urls()
        if workers is None:
            import os
            workers = os.cpu_count() * 5
        download_images_parallel(urls, self.gallery_id, n, m, workers, img_type=img_type)

# Fetch the gallery page HTML via HTTP and extract the JSON object for metadata
def fetch_gallery_info_http(def_gallery_id):
    # Send HTTP GET request to fetch page HTML
    def_url = f"https://k-hentai.org/r/{def_gallery_id}"
    html = requests.get(def_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5).text

    def_m = re.search(r'const gallery\s*=\s*({.*?});', html, re.DOTALL)
    if not def_m:
        raise RuntimeError("CANT NOT FIND GALLERY INFO")
    obj = def_m.group(1)

    try:
        # Try direct JSON parse
        return json.loads(obj)
    except json.JSONDecodeError:
        fixed = re.sub(r'(\w+):', r'"\1":', obj).replace("'", '"')
        return json.loads(fixed)

# Helper to download a single image given URL, folder, index, and extension
def download_one(args):
    def_url, folder, idx, ext = args
    path = os.path.join(folder, f"{folder}_{idx}.{ext}")
    resp = requests.get(def_url, stream=True, timeout=10)
    resp.raise_for_status()
    with open(path, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)
    return path

# Download a slice of URLs in parallel using ThreadPoolExecutor
def download_images_parallel(urls, folder, def_n, def_m, def_workers=8, img_type=None):
    # Ensure target folder exists
    os.makedirs(folder, exist_ok=True)
    target_urls = urls[def_n - 1:def_m]
    total = len(target_urls)
    print(f" TO {folder} FOLDER, DOWNLOAD {total} IMAGE (TCP THREADS={def_workers})")
    print("-------------------------")

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

# Main controller handling CLI input and orchestrating per-gallery downloads
class Main_Activity():
    def Download(self, url, mode, ext_type):
        # Normalize URL or ID input to full URL
        if url.isdigit():
            url = f"https://k-hentai.org/r/{url}"
        elif not url.startswith("http"):

            url = f"https://k-hentai.org/r/{url}"


        # Handle comma-separated list of gallery IDs
        if "," in url:
            gallery_ids = [u.strip() for u in url.split(",") if u.strip()]
            for gid in gallery_ids:
                self.Download(gid, mode, ext_type)
            return

        # Strip URL fragment if present (e.g., "#1")
        gallery_id = url.split("/")[-1].split("#")[0]

        downloader = GalleryDownloader(gallery_id)

        info = downloader.info

        # Print gallery metadata: URL, ID, title, pages, tags
        print("-------------------------")
        print("FILE INFO")
        print("-------------------------")
        print(f'GALLERY ID: ｢{gallery_id}｣')
        print(f'TITLE: ｢{info["title"]}｣')
        print(f'PAGES: ｢{info["filecount"]}｣')
        print(f'TAGS: ｢{", ".join(downloader.get_tags())}｣')
        print("-------------------------")
        print("BEFORE DOWNLOAD . . . ")



        # If mode is user_input, prompt for page range
        if mode == "all":
            n = 1
            m = info["filecount"]
        else:
            n = int(input('page from: '))
            m = int(input('page to: '))


            while True:
                if n < 1 or m < 1:
                    print("only natural number can be entered")
                elif n > m:
                    print("page from can't exceed page to")
                elif m > info["filecount"]:
                    print("page to can't exceed the total page")
                    print("page to set to end of gallery")
                    m = info["filecount"]
                    break
                else:
                    break
                n = int(input('page from: '))
                m = int(input('page to: '))

            print(' ')
            print(f'page from: {n}')
            print(f'page to: {m}')


        # Determine the number of worker threads based on CPU count
        workers = os.cpu_count() * 5
        print(f'TCP THREADS: ｢{workers}｣')
        print("-------------------------")
        # Measure download duration for this gallery
        start_time = time.time()
        # Download pages
        downloader.download(n, m, workers, img_type=ext_type)
        end_time = time.time()
        print(f"DOWNLOAD COMPLETE IN {end_time - start_time:.2f} SECONDS")


# Prompt user on error: abort or skip failed gallery
def handle_error(gallery_id, exception):
    print(f"Error occurred on gallery {gallery_id}: {exception}")
    choice = input("Error occurred on gallery RESUME? (y/n): ").strip().lower()
    if choice != 'y':
        print("Program stoped.")
        sys.exit(1)
    else:
        print(f"Skipping gallery {gallery_id} and continuing.")

# Entry point: parse input, support single or multiple gallery IDs
if __name__ == "__main__":
    import re
    target = input("input gallery id or gallery id list:")
    make_dir = input("Make new dir (leave empty for not make dir): ").strip()
    if make_dir:
        os.makedirs(make_dir, exist_ok=True)
        os.chdir(make_dir)
        print(f'MADE DIR NAMED ｢{make_dir}｣')
    else:
        print('dir set to current dir')

    raw_ids = re.split(r"[,\s]+", target.strip())
    gallery_ids = [gid for gid in raw_ids if gid]

    # Start timing multiple gallery downloads
    if len(gallery_ids) > 1:
        start_time = time.time()
        for gid in gallery_ids:
            try:
                Main_Activity().Download(gid, 'all', 'jpg')
            except Exception as e:
                handle_error(gid, e)
        end_time = time.time()
        print(f"TOTAL DURATION OF MULTIPLE DOWNLOAD COMPLETE IN {end_time - start_time:.2f} SECONDS")
    # Single gallery download with error handling
    else:

        try:
            Main_Activity().Download(gallery_ids[0], 'user_input', 'jpg')
        except Exception as e:
            handle_error(gallery_ids[0], e)
