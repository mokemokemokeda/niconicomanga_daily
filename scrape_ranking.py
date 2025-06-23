import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from openpyxl import load_workbook

url = "https://manga.nicovideo.jp/ranking/point/daily/shonen"
res = requests.get(url)
res.encoding = res.apparent_encoding
soup = BeautifulSoup(res.text, "html.parser")

data = []
for i, item in enumerate(soup.select(".mg_category_ranking_inner"), 1):
    title_elem = item.select_one(".mg_title_area strong a")
    author_elem = item.select_one(".mg_author")
    latest_episode_elem = item.select_one(".latest_episode_title")

    data.append({
        "rank": i,
        "title": title_elem.get_text(strip=True) if title_elem else None,
        "author": author_elem.get_text(strip=True).replace('作者:', '') if author_elem else None,
        "latest_episode": latest_episode_elem.get_text(strip=True) if latest_episode_elem else None,
    })

df = pd.DataFrame(data)

file_path = "ranking_results.xlsx"
sheet_name = datetime.datetime.now().strftime("%Y-%m-%d")

try:
    # 既存Excelファイルの読み込み
    book = load_workbook(file_path)

    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        writer.book = book  # ここは省略してもOKかもしれません
        df.to_excel(writer, sheet_name=sheet_name, index=False)

except FileNotFoundError:
    # 新規ファイル作成
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
