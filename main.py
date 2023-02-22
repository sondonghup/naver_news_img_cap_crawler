import requests
import argparse
import urllib.request
from bs4 import BeautifulSoup as bs
from user_agent import generate_user_agent
import os


def crawl(img_dir, cap_dir, img_dir_num, url, file_num):
    """
    img_dir : 이미지 디렉토리 ex) img_0
    cap_dir : 캡션 디렉토리 ex) cap
    img_dir_num : 사진 파일의 경우 용량 문제로 폴더를 분할 하기위해 정한 넘버 ex) img_0 img_1 img_2
    url : 뉴스 url
    file_num : 한 폴더 안에 이미지를 몇개 넣을 것 인지 ex) 10을 입력 하면 10개 마다 새 폴더가 생성됨
    """

    header = {"User-Agent": generate_user_agent()}
    html = requests.get(url, headers=header)
    html = bs(html.text, "html.parser")
    img_caps = html.find_all("span", {"class": "end_photo_org"})
    img_dir_name = f"{img_dir}_{img_dir_num}"
    if not os.path.exists(img_dir_name):
        os.mkdir(img_dir_name)

    for img_cap in img_caps:
        if len(os.listdir(img_dir_name)) < file_num:
            if img_cap.find("em", "img_desc") != None:
                image = img_cap.find("img")["data-src"]
                caption = img_cap.find("em", "img_desc").get_text()
                image_name = image.split("?")[0].split("/")[-1]
                urllib.request.urlretrieve(image, f"{img_dir_name}/{image_name}")
                with open(f"{cap_dir}/captions.tsv", "a", encoding="utf-8") as f:
                    f.write(f"{image_name}\t{caption}\n")
            else:
                continue
        else:
            img_dir_num += 1
            img_dir_name = f"{img_dir}_{img_dir_num}"
            if not os.path.exists(img_dir_name):
                os.mkdir(img_dir_name)

    return img_dir, img_dir_num


def naver_news(category, date):
    """
    category : 뉴스 카테고리
    date : 해당 날짜
    """
    header = {"User-Agent": generate_user_agent()}
    url = f"https://media.naver.com/newsflash/469/{category}?before={date}00010500000"
    html = requests.get(url=url, headers=header)
    news_list = html.json()["list"]

    url_list = []
    for news in news_list:
        url_list.append(news["linkUrl"])

    return url_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--imgdir", default="./img")
    parser.add_argument("-c", "--capdir", default="./cap")
    parser.add_argument("-s", "--start", default=20230220)
    parser.add_argument("-e", "--end", default=20230222)
    parser.add_argument("-n", "--num", default=5)  # 이미지 폴더에 들어갈 파일의 개수
    parser.add_argument("-g", "--category", default="Economy")  # 뉴스 카테고리
    """
    뉴스 카테고리
    경제 : Economy
    정치 : Politics
    사회 : Society
    생활 : LifeCulture
    세계 : World
    IT : It
    사설칼럼 : Opinion
    """
    args = parser.parse_args()

    img_dir_num = 0

    if not os.path.exists(args.capdir):
        os.mkdir(args.capdir)

    img_dir = args.imgdir
    cap_dir = args.capdir

    for date in range(args.start, args.end):
        url_list = naver_news(args.category, date)
        for url in url_list:
            img_dir, img_dir_num = crawl(img_dir, cap_dir, img_dir_num, url, args.num)
