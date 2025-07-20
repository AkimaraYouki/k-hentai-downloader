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
# from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()
#     page.goto("https://k-hentai.org/?search=fav%3A27549")
#     # page.fill("[name=username]", "YOUR_ID")
#     # page.fill("[name=password]", "YOUR_PW")
#     # page.click("button[type=submit]")
#     page.wait_for_function()
#     # favorites_html = page.content()
#     browser.close()\

# n = int(input('page from: '))
# m = int(input('page to: '))
# info = 42
#
# while True:
#     if n < 1 or m < 1:
#         print("only natural number can be entered")
#     elif n > m:
#         print("page from can't exceed page to")
#     elif m > info:
#         print("page to can't exceed the total page")
#         print("page to set to end of gallery")
#         m = info
#         break
#     else:
#         break
#     n = int(input('page from: '))
#     m = int(input('page to: '))
#
# print(' ')
# print(f'page from: {n}')
# print(f'page to: {m}')

list = '''https://k-hentai.org/r/3444597#39https://k-hentai.org/r/3444396#5https://k-hentai.org/r/3441679#1https://k-hentai.org/r/3441671#1https://k-hentai.org/r/3441663#1https://k-hentai.org/r/3439932#1https://k-hentai.org/r/3431675#11https://k-hentai.org/r/3437523#1https://k-hentai.org/r/3425841#1https://k-hentai.org/r/3421633#1https://k-hentai.org/r/3415973#1https://k-hentai.org/r/3410183#1https://k-hentai.org/r/3409403#1https://k-hentai.org/r/3408955#1https://k-hentai.org/r/3407102#1https://k-hentai.org/r/3407111#1https://k-hentai.org/r/3389643#6https://k-hentai.org/r/3389334#1https://k-hentai.org/r/3381540#1https://k-hentai.org/r/3360282#1https://k-hentai.org/r/3373349#1https://k-hentai.org/r/3361898#1'''
l1 = []
for i in list.split("#"):
    l1.append(i.split('/')[-1]+' ')
print("".join(l1))

