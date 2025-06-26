import os

# https://tienphong.vn
# https://hanoimoi.vn/
# https://baohaiquanvietnam.vn/

BASE_URL = "https://hanoimoi.vn/doi-song"
LOG_FOLDER = "./log"
DATA_FOLDER = "./data"
NUM_THREADS = 4
ARTICLE_LINK_SELECTOR = 'h3.b-grid__title a'
# 'h3.story__heading a' => tienphong
# 'h3.b-grid__title a' => hanoimoi
# 'h3 a' => baohaiquanvietnam

SUMMARY_SELECTOR = '.sc-longform-header-meta'
# '.article__sapo' => tienphong
# '.sc-longform-header-meta' => hanoimoi
# 'div.que_news p strong' => baohaiquanvietnam

CONTENT_SELECTOR = '.entry'
# '.article__body' => tienphong
# '.entry' =>hanoimoi
# '.content_news' => baohaiquanvietnam

BUTTON_SELECTOR = '.btn-timeline-more' 
# '.btn-timeline-more' => tienphong


os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)