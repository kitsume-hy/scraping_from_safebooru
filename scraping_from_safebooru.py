import requests
import json
import re
import os
from bs4 import BeautifulSoup

def get_content_and_metainfo_from_image_url(image_url: str, save_dir: str, debug_mode: bool):
    """画像コンテンツurlから画像とメタデータを取得して保存する.

    Args:
        image_url (str): 取得元の画像URL
        save_dir (str): 保存先のディレクトリ

    Todo:
        - データが正常に取得できない場合のException回避. (現状は正常に取得できることを仮定している.)
    """

    if debug_mode:
        print( f"{image_url}から取得を開始します.")

    responce  = requests.get(image_url)
    soup      = BeautifulSoup(responce.text,features="lxml")

    #画像の取得
    image_content,image_name = save_image_from_image_url_soup(soup=soup)
    #タグの取得
    tags   = get_tags_from_image_url_soup(soup=soup)
    #ソースの取得
    source = get_source_from_image_url_soup(soup=soup)
    #tagとソースは同じdictにまとめる.
    tags["source"] = source

    #画像の保存
    if debug_mode:
        print( f"{image_name}を保存します.")
        
    with open(os.path.join(save_dir,image_name),"wb") as f:
        f.write(image_content)

    #拡張子無しのファイル名
    image_name_no_extension = os.path.splitext(image_name)[0]
    json_name = f"{image_name_no_extension}.json"

    with open(os.path.join(save_dir,json_name),"w") as f:
        json.dump(tags,f,indent=2)

def save_image_from_image_url_soup(soup: BeautifulSoup):
    """画像urlのsoupから画像urlを取得して保存する."""
    
    image_url_elem = soup.find_all('meta', attrs={'property': 'og:image', 'content': True})
    assert len(image_url_elem) == 1, "取得されたimage_url_elemが1つではありません."
    image_url_elem = image_url_elem[0]
    image_url = image_url_elem["content"]

    #画像の取得
    responce   = requests.get(image_url)
    image_name = os.path.basename( responce.url )

    image_content = responce.content

    return image_content,image_name

def get_source_from_image_url_soup(soup: BeautifulSoup):
    """画像urlのsoupからSourceのurlを取得する."""

    statistics_element = soup.find_all(id="stats")
    assert len( statistics_element  ) == 1, "取得されたstatisticsエレメントが1個ではありません."
    statistics_element = statistics_element[0] 

    #statisticsのlistを取得する.
    statistics_list_elements = statistics_element.find_all("li")

    #Sourceの部分のみ取得する.
    candidate_source_elem = [static_list_elem for static_list_elem in statistics_list_elements if "Source" in static_list_elem.text]
    assert len( candidate_source_elem ) == 1 , "sourceが記述されているエレメントが1つではありません."
    candidate_source_elem = candidate_source_elem[0]
    #html_source = re.search("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+",candidate_source_elem.text ).group()
    html_source = candidate_source_elem.text.replace("Source: ","")

    if html_source is None:
        raise TypeError("html_sourceが取得できませんでした.")
    return html_source

def get_tags_from_image_url_soup(soup: BeautifulSoup):
    """画像urlのsoupからtagを取得する."""
    
    # tagタイプごとにエレメントを取得する.
    tag_type_character_elements = soup.find_all(class_="tag-type-character tag")
    tag_type_artist_elements    = soup.find_all(class_="tag-type-artist tag")
    tag_type_general_elements   = soup.find_all(class_="tag-type-general tag")

    # tagの取得
    character_tags = [elem.find_all("a")[0].get_text() for elem in tag_type_character_elements ]
    artist_tags    = [elem.find_all("a")[0].get_text() for elem in tag_type_artist_elements  ]
    general_tags   = [elem.find_all("a")[0].get_text() for elem in tag_type_general_elements ]

    tags = {
        "character": character_tags,
        "artist": artist_tags,
        "general": general_tags
    }
    return tags