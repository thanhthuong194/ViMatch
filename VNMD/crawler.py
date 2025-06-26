import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import logging
from config import BASE_URL, NUM_THREADS, ARTICLE_LINK_SELECTOR
from urllib.parse import urljoin
import time

# Cấu hình logging
logging.basicConfig(filename="log/crawler.log", level=logging.INFO)

def get_article_links(base_url):
    links = set()
    page_num = 10001

    while page_num <= 10005:  # Giới hạn số trang crawl
        page_url = f"{base_url}?page={page_num}"
        logging.info(f"Đang crawl trang: {page_url}")
        print(f"Đang crawl trang: {page_url}") # Thêm dòng này

        try:
            response = requests.get(page_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            article_elements = soup.select(ARTICLE_LINK_SELECTOR)
            print(f"Số lượng phần tử tìm thấy ở trang {page_num}: {len(article_elements)}") # Thêm dòng này

            if not article_elements:
                logging.info(f"Không còn bài viết ở trang {page_num}. Dừng lại.")
                print(f"Không còn bài viết ở trang {page_num}. Dừng lại.") # Thêm dòng này
                break

            for element in article_elements:
                href = element.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    links.add(full_url)
                    print(f"Đã thêm link: {full_url}") # Thêm dòng này

        except Exception as e:
            logging.error(f"Lỗi khi crawl trang {page_url}: {e}")
            print(f"Lỗi khi crawl trang {page_url}: {e}") # Thêm dòng này
            break

        logging.info(f"Đã xử lý trang {page_num}, tổng số link hiện tại: {len(links)}")
        print(f"Đã xử lý trang {page_num}, tổng số link hiện tại: {len(links)}") # Thêm dòng này
        page_num += 1
        time.sleep(1.5)  # Tránh bị chặn IP

    return list(links)

def fetch_article(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return {"url": url, "html_content": response.text}
    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi khi lấy bài báo {url}: {e}")
        return {"url": url, "html_content": None}

def fetch_all_articles():
    article_links = get_article_links(BASE_URL)
    if not article_links:
        logging.warning("Không có links bài viết nào được thu thập từ trang chủ.")
        return []

    logging.info(f"Đã tìm thấy {len(article_links)} links bài viết.")

    articles_data = []
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        results = executor.map(fetch_article, article_links)
        for result in results:
            if result["html_content"]:
                articles_data.append(result)
            else:
                logging.warning(f"Không thể tải nội dung từ URL: {result['url']}")

    return articles_data

if __name__ == '__main__':
    articles = fetch_all_articles()
    print(f"Số lượng bài viết đã thu thập (HTML content): {len(articles)}")
    if articles:
        print("Ví dụ URL bài viết đầu tiên:")
        print(articles[0]['url'])
