from bs4 import BeautifulSoup
import logging
from config import SUMMARY_SELECTOR, CONTENT_SELECTOR

logging.basicConfig(filename="log/cleaner.log", level=logging.INFO)

class Cleaner:
    def clean_data(self, url, html_content):
        if not html_content:
            return None
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Selector cho summary
            summary_element = soup.select_one(SUMMARY_SELECTOR)
            summary_text = summary_element.text.strip() if summary_element else ""

            text_content_list = []
            seen_text = set()

            # Duyệt qua các phần tử con trực tiếp
            content_element = soup.select_one(CONTENT_SELECTOR)
            if content_element:
                for p_tag in content_element.find_all('p', recursive=False):
                    paragraph_text = p_tag.text.strip()
                    if paragraph_text and paragraph_text not in seen_text:
                        text_content_list.append(paragraph_text)
                        seen_text.add(paragraph_text)

            if not text_content_list or not summary_text:
                return None
            
            return {
                "text": text_content_list,
                "summary": [summary_text]
            }

        except Exception as e:
            logging.error(f"Lỗi khi clean dữ liệu từ URL {url}: {e}")
            return None