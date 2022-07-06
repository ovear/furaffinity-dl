import json
from tqdm import tqdm
from pathvalidate import sanitize_filename
import Modules.config as config
import os
import requests
from bs4 import BeautifulSoup
import http.cookiejar as cookielib
from Modules.functions import system_message_handler, check_filter, download_complete

session = requests.session()
if config.cookies is not None:  # add cookies if present
    cookies = cookielib.MozillaCookieJar(config.cookies)
    cookies.load()
    session.cookies = cookies

def download(path):
    response = session.get(f"{config.BASE_URL}{path}")
    s = BeautifulSoup(response.text, "html.parser")

    # System messages
    if s.find(class_="notice-message") is not None:
        system_message_handler(s)

    image = s.find(class_="download").find("a").attrs.get("href")
    title = s.find(class_="submission-title").find("p").contents[0]
    title = sanitize_filename(title)
    dsc = s.find(class_="submission-description").text.strip().replace("\r\n", "\n")

    if config.json_description is True:
        dsc = []
    filename = image.split("/")[-1:][0]
    data = {
        "id": int(path.split("/")[-2:-1][0]),
        "filename": filename,
        "author": s.find(class_="submission-id-sub-container")
        .find("a")
        .find("strong")
        .text,
        "date": s.find(class_="popup_date").attrs.get("title"),
        "title": title,
        "description": dsc,
        "url": f"{config.BASE_URL}{path}",
        "tags": [],
        "category": s.find(class_="info").find(class_="category-name").text,
        "type": s.find(class_="info").find(class_="type-name").text,
        "species": s.find(class_="info").findAll("div")[2].find("span").text,
        "gender": s.find(class_="info").findAll("div")[3].find("span").text,
        "views": int(s.find(class_="views").find(class_="font-large").text),
        "favorites": int(s.find(class_="favorites").find(class_="font-large").text),
        "rating": s.find(class_="rating-box").text.strip(),
        "comments": [],
    }
    if config.submission_filter is True and check_filter(title) is True:
        print(
            f'{config.WARN_COLOR}"{title}" was filtered and will not be \
downloaded - {data.get("url")}{config.END}'
        )
        return True

    image_url = f"https:{image}"
    output = f"{config.output_folder}/{data.get('author')}"
    if config.category != "gallery":
        output = f"{config.output_folder}/{data.get('author')}/{config.category}"
    if config.folder is not None:
        output = f"{config.output_folder}/{data.get('author')}/{config.folder}"
    os.makedirs(output, exist_ok=True)
    filename = sanitize_filename(filename)
    output_path = f"{output}/{title} - {filename}"
    if config.rating is True:
        os.makedirs(f'{output}/{data.get("rating")}', exist_ok=True)
        output_path = f'{output}/{data.get("rating")}/{title} - {filename}'

    if config.dont_redownload is True and os.path.isfile(output_path):
        if config.check is True:
            print(
                f"{config.SUCCESS_COLOR}Downloaded all recent files of \"{data.get('author')}\"{config.END}"
            )
            raise download_complete
        print(
            f'{config.WARN_COLOR}Skipping "{title}" since it\'s already downloaded{config.END}'
        )
        return True
    else:
        download_file(
            image_url,
            output_path,
            f'{title} - \
[{data.get("rating")}]',
        )

    if config.metadata is True:
        create_metadata(output, data, s, title, filename)
    if config.download is not None:
        print(f'{config.SUCCESS_COLOR}File saved as "{output_path}" {config.END}')
    return True

def download_file(url, fname, desc):
    try:
        r = session.get(url, stream=True)
        if r.status_code != 200:
            print(
                f'{config.ERROR_COLOR}Got a HTTP {r.status_code} while downloading \
"{fname}". URL {url} ...skipping{config.END}'
            )
            return False
        total = int(r.headers.get("Content-Length", 0))
        with open(fname, "wb") as file, tqdm(
            desc=desc.ljust(40),
            total=total,
            miniters=100,
            unit="b",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in r.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    except KeyboardInterrupt:
        print(f"{config.SUCCESS_COLOR}Finished downloading{config.END}")
        os.remove(fname)
        exit()
    return True
    
def create_metadata(output, data, s, title, filename):
    if config.rating is True:
        os.makedirs(f'{output}/{data.get("rating")}/metadata', exist_ok=True)
        metadata = f'{output}/{data.get("rating")}/metadata/{title} - {filename}'
    else:
        os.makedirs(f"{output}/metadata", exist_ok=True)
        metadata = f"{output}/metadata/{title} - {filename}"

    # Extract description as list
    if config.json_description is True:
        for desc in s.find("div", class_="submission-description").stripped_strings:
            data["description"].append(desc)

    # Extact tags

    try:
        for tag in s.find(class_="tags-row").findAll(class_="tags"):
            data["tags"].append(tag.find("a").text)
    except AttributeError:
        print(f'{config.WARN_COLOR}"{title}" has no tags{config.END}')

    # Extract comments
    for comment in s.findAll(class_="comment_container"):
        temp_ele = comment.find(class_="comment-parent")
        parent_cid = None if temp_ele is None else int(temp_ele.attrs.get("href")[5:])
        # Comment is deleted or hidden
        if comment.find(class_="comment-link") is None:
            continue

        data["comments"].append(
            {
                "cid": int(comment.find(class_="comment-link").attrs.get("href")[5:]),
                "parent_cid": parent_cid,
                "content": comment.find(class_="comment_text").contents[0].strip(),
                "username": comment.find(class_="comment_username").text,
                "date": comment.find(class_="popup_date").attrs.get("title"),
            }
        )

    # Write a UTF-8 encoded JSON file for metadata
    with open(f"{metadata}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)