import torch
from transformers import RobertaTokenizer
import nltk

# Thêm dòng này để tải tài nguyên NLTK bị thiếu
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

# Tải mô hình đã được huấn luyện sẵn
model = torch.load('/home/thanhthuong/projects/MatchSum/MatchSum/phobert/2025-06-20-06-47-43-595777/epoch-3_step-3500_ROUGE-0.266652.pt', weights_only=False)

# Đặt mô hình vào chế độ đánh giá
model.eval()

# Tải tokenizer RoBERTa
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

def summarize(text, candidates):
    """Tóm tắt văn bản bằng mô hình MatchSum."""

    # Chuẩn bị dữ liệu đầu vào
    inputs = tokenizer.encode_plus(text, return_tensors='pt', add_special_tokens=True, truncation=True, max_length=512)
    text_ids = inputs['input_ids']

    # Mã hóa từng câu ứng viên
    candidate_ids = []
    max_len = 0
    for candidate in candidates:
        candidate_inputs = tokenizer.encode_plus(candidate, return_tensors='pt', add_special_tokens=True, truncation=True, max_length=512)
        candidate_ids.append(candidate_inputs['input_ids'])
        max_len = max(max_len, candidate_inputs['input_ids'].size(1))

    # Padding thủ công
    padded_candidate_ids = []
    for candidate_input_ids in candidate_ids:
        pad_len = max_len - candidate_input_ids.size(1)
        padded_input_ids = torch.cat([candidate_input_ids, torch.zeros((1, pad_len), dtype=torch.long)], dim=1)
        padded_candidate_ids.append(padded_input_ids)

    # Tạo tensor từ danh sách các input_ids đã được padding
    candidate_ids = torch.cat(padded_candidate_ids, dim=0).unsqueeze(0)  # Thêm batch dimension

    summary_inputs = tokenizer.encode_plus(text, return_tensors='pt', add_special_tokens=True, truncation=True, max_length=512)
    summary_ids = summary_inputs['input_ids']

    # Đưa dữ liệu vào mô hình
    with torch.no_grad():
        outputs = model(text_ids, candidate_ids, summary_ids)

    # Xử lý đầu ra
    candidate_scores = outputs['score'][0]
    top_candidate_indices = torch.argsort(candidate_scores, descending=True)[:3].tolist()
    top_candidate_indices.sort()
    summary_sentences = [candidates[i] for i in top_candidate_indices]
    summary = " ".join(summary_sentences)

    return summary

# Văn bản đầu vào ví dụ
text = "Nền tảng âm nhạc trực tuyến 'MelodyStream' đã đạt 50 triệu người dùng trả phí. Doanh thu từ thuê bao tăng 25% trong năm 2024. 3 nghệ sĩ Việt Nam đã lọt vào top 10 bảng xếp hạng khu vực. Nền tảng đã chi 100 tỷ VNĐ cho bản quyền âm nhạc. Hơn 5.000 bài hát mới được thêm vào thư viện mỗi tháng."
# Danh sách các câu ứng viên
candidates = nltk.sent_tokenize(text)

# Tóm tắt văn bản
summary = summarize(text, candidates)

# In bản tóm tắt
print("Bản tóm tắt:", summary)