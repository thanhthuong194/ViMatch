import json
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import evaluate
import torch

# === 1) Đọc file JSONL, nối list câu thành chuỗi ===
input_file = "/home/thanhthuong/projects/MatchSum/MatchSum/ViMatch/test_rouge_phobert.jsonl"
texts = []
references = []
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        record = json.loads(line)
        text_list = record.get("text", "")
        summary_list = record.get("summary", "")

        # Nếu là list thì nối, nếu đã chuỗi thì dùng nguyên
        if isinstance(text_list, list):
            text_str = " ".join(text_list)
        else:
            text_str = text_list

        if isinstance(summary_list, list):
            summary_str = " ".join(summary_list)
        else:
            summary_str = summary_list

        texts.append(text_str)
        references.append(summary_str)

print(f"→ Đọc được {len(texts)} bài test và {len(references)} tóm tắt tham chiếu")

# === 2) Load model và tokenizer ===
model_name = "VietAI/vit5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
model.to(device)
model.eval()

# === 3) Sinh tóm tắt theo batch ===
batch_size = 8  # điều chỉnh tuỳ GPU

predictions = []
for i in tqdm(range(0, len(texts), batch_size), desc="Generating summaries in batches"):
    batch_texts = texts[i:i+batch_size]
    inputs = tokenizer(
        batch_texts,
        return_tensors="pt",
        truncation=True,
        padding="longest",
        max_length=1024
    ).to(device)

    with torch.no_grad():
        summary_ids = model.generate(
            **inputs,
            num_beams=4,
            max_length=150,
            early_stopping=True
        )
    batch_summaries = tokenizer.batch_decode(summary_ids, skip_special_tokens=True)
    predictions.extend(batch_summaries)

# === 4) Tính ROUGE ===
rouge = evaluate.load("rouge")
results = rouge.compute(predictions=predictions, references=references)

print("\n=== ROUGE Scores ===")
print(f"ROUGE-1: {results['rouge1']:.4f}")
print(f"ROUGE-2: {results['rouge2']:.4f}")
print(f"ROUGE-L: {results['rougeL']:.4f}")
