import site
import time
from selenium.common.exceptions import SessionNotCreatedException

# K-hentai . org 의 북마크 익스포트 형식
# bookmark = [{"name":"ㄷㄱㅈㄷㄱ","private":1,"created":1752910021964,"updated":1752910046812,"galleries":[{"id":3446484,"time":1752910035865},{"id":3446480,"time":1752910046812}]}]
# print(bookmark[0]["galleries"])
#
# list = []
# for i in bookmark[0]["galleries"]:
#     print(i["id"])
#     list.append(i["id"])
# print(','.join(map(str, list)))


# list_1 = []
# for i in download.split("\n"):
#     list_1.append(i.split(" ")[0])
# print(",".join(list_1))


# <script>
# const favorites = [{"id":27549,"name":"\u3137\u3131\u3148\u3137\u3131","private":1,"gallery_count":4,"created":1752910021964,"updated":1752918669727,"galleries":[{"id":3446484,"time":1752910035865},{"id":3446480,"time":1752910046812},{"id":3446856,"time":1752916219516},{"id":3334085,"time":1752918669727}]}];
# const favoriteThumbnails = [{"id":27549,"gallery_id":3334085,"gallery_thumb_extension":"webp"}];
# </script>

# favorites = [{"id":27549,"name":"\u3137\u3131\u3148\u3137\u3131","private":1,"gallery_count":4,"created":1752910021964,"updated":1752918669727,"galleries":[{"id":3446484,"time":1752910035865},{"id":3446480,"time":1752910046812},{"id":3446856,"time":1752916219516},{"id":3334085,"time":1752918669727}]}]
# print(favorites[0]["id"])
# print(favorites[0]["galleries"][0]["id"])

# https://k-hentai.org/?search=fav%3A27549
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://k-hentai.org/?search=fav%3A27549")
    # page.fill("[name=username]", "YOUR_ID")
    # page.fill("[name=password]", "YOUR_PW")
    # page.click("button[type=submit]")
    page.wait_for_function()
    # favorites_html = page.content()
    browser.close()