from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-large-vietnews-summarization")  
model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-large-vietnews-summarization")
model.to("cuda")

sentence = "Nền tảng âm nhạc trực tuyến 'MelodyStream' đã đạt 50 triệu người dùng trả phí. Doanh thu từ thuê bao tăng 25% trong năm 2024. 3 nghệ sĩ Việt Nam đã lọt vào top 10 bảng xếp hạng khu vực. Nền tảng đã chi 100 tỷ VNĐ cho bản quyền âm nhạc. Hơn 5.000 bài hát mới được thêm vào thư viện mỗi tháng."

text =  "vietnews: " + sentence + " </s>"
encoding = tokenizer(text, return_tensors="pt")
input_ids, attention_masks = encoding["input_ids"].to("cuda"), encoding["attention_mask"].to("cuda")
outputs = model.generate(
    input_ids=input_ids, attention_mask=attention_masks,
    max_length=256,
    early_stopping=True
)
for output in outputs:
    line = tokenizer.decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    print(line)