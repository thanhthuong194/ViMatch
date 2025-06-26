import json
import os
from os.path import join, exists
from config import DATA_FOLDER
import logging

logging.basicConfig(filename=join(DATA_FOLDER, "saver.log"), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Saver:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.output_file = join(data_dir, 'data.jsonl')
        self.existing_hashes = set()  
        self._load_existing_hashes() 

    def _load_existing_hashes(self):
        """Đọc file và tải hash của dữ liệu đã có vào set."""
        if exists(self.output_file):
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            existing_item = json.loads(line)
                            item_hash = self._hash_data_item(existing_item) # Hash data item
                            self.existing_hashes.add(item_hash) # Thêm hash vào set
                        except json.JSONDecodeError:
                            logging.warning(f"Không thể giải mã dòng JSON: {line.strip()}, bỏ qua dòng này.")
            except Exception as e:
                logging.error(f"Lỗi khi đọc dữ liệu hiện có từ file để tải hash: {e}")

    def _hash_data_item(self, data_item):
        """Tạo hash đại diện cho data_item. Cần chuẩn hóa JSON trước khi hash."""
        # Chuẩn hóa JSON để đảm bảo hash nhất quán 
        json_string = json.dumps(data_item, sort_keys=True, ensure_ascii=False)
        return hash(json_string) 

    def save_data(self, data_list):
        count_saved = 0
        try:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                for data_item in data_list:
                    if data_item:
                        item_hash = self._hash_data_item(data_item) 
                        if item_hash not in self.existing_hashes:
                            json.dump(data_item, f, ensure_ascii=False)
                            f.write('\n')
                            self.existing_hashes.add(item_hash)
                            count_saved += 1
                logging.info(f"Đã lưu {count_saved} bản ghi mới vào {self.output_file}, bỏ qua {len(data_list) - count_saved} bản ghi trùng lặp.")
        except Exception as e:
            logging.error(f"Lỗi khi lưu dữ liệu vào file: {e}")