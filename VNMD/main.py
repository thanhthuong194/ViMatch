
from crawler import fetch_all_articles
from cleaner import Cleaner
from saver import Saver
import logging
import os
from os.path import join
from config import LOG_FOLDER, DATA_FOLDER

# Cấu hình logging cho main.py
logging.basicConfig(filename='log/main.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Bắt đầu thu thập dữ liệu...")
    articles_html = fetch_all_articles()
    logging.info(f"Đã thu thập được {len(articles_html)} bài viết (HTML thô).")

    cleaner = Cleaner() # Khởi tạo đối tượng Cleaner
    saver = Saver(DATA_FOLDER) # Khởi tạo đối tượng Saver
    cleaned_data_list = [] # Danh sách chứa dữ liệu đã clean

    cleaned_articles_count = 0
    for article_item in articles_html:
        if article_item["html_content"]: # Kiểm tra html_content có bị None không
            cleaned_data = cleaner.clean_data(article_item["url"], article_item["html_content"])
            if cleaned_data:
                cleaned_data_list.append(cleaned_data)
                cleaned_articles_count += 1
            else:
                logging.warning(f"Không thể làm sạch dữ liệu cho bài viết từ URL: {article_item['url']}")
        else:
            logging.warning(f"Không có HTML content cho bài viết từ URL: {article_item['url']}")

    saver.save_data(cleaned_data_list)
    logging.info(f"Đã làm sạch và lưu {cleaned_articles_count} bài viết vào {saver.output_file}")
    print(f"Dữ liệu đã được lưu tại: {saver.output_file}")


if __name__ == "__main__":
    main()