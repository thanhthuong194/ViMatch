import os
from os.path import exists, join
import re
import json
import argparse
import numpy as np

from rouge_score import rouge_scorer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from underthesea import sent_tokenize, word_tokenize

org_data, ids = [], []

def load_jsonl(path):
    data = []
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))

    return data

def filter_short_lines(data, text_sentences, summary_chars):
    filter_short_data = []
    for line in data:
        texts = ' '.join(line['text'])
        summaries = line['summary']

        sentences = sent_tokenize(texts)
        tokenized_sentences = []
        for sentence in sentences:
            tokenized = word_tokenize(sentence, format='text')
            tokenized_sentences.append(tokenized)

        if len(sentences) >= text_sentences and len(summaries[0]) >= summary_chars:
            summary_sentences = sent_tokenize(summaries[0])
            tokenized_summaries = []
            for ssentence in summary_sentences:
                tokenized = word_tokenize(ssentence, format='text')
                tokenized_summaries.append(tokenized)

            new_line = {'text': tokenized_sentences, 'summary': tokenized_summaries}
            filter_short_data.append(new_line)

    return filter_short_data

def select_six_sentences(data, method, path):
    indices = []
    if method == 'rouge':
        for line in data:
            sentences = line['text']
            gold_sum = ' '.join(line['summary'])

            scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

            scores = []

            for sentence in sentences:
                score = scorer.score(sentence, gold_sum)
                rouge_l_f1 = score["rougeL"].fmeasure
                scores.append(rouge_l_f1)

            indices = np.argsort(scores)[-6:][::-1]
            ids = {}
            ids["sent_id"] = indices.tolist()
            with open(path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(ids) + '\n')

    else:
        for line in data:
            sentences = line['text']
            summary = ' '.join(line['summary'])

            scores = []
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(sentences + [summary])
            scores = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1]).flatten()

            indices = np.argsort(scores)[-6:][::-1]
            ids = {}
            ids["sent_id"] = indices.tolist()
            with open(path, 'a', encoding = 'utf-8') as f:
                f.write(json.dumps(ids) + '\n')

def process_data(args):
    global org_data, ids
    org_data = load_jsonl(args.data_path)

    fileter_short_data = filter_short_lines(org_data, args.text_sentences, args.summary_chars)
    select_six_sentences(fileter_short_data, args.method, args.index_path)
    with open(args.write_path, 'a', encoding='utf-8') as f:
        for line in fileter_short_data:
            f.write(json.dumps(line, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocess data')

    parser.add_argument('--data_path', type=str, required=True, help='path to the original dataset')
    parser.add_argument('--text_sentences', type=int, default=9, help='Minimum number of sentences required in text')
    parser.add_argument('--summary_chars', type=int, default=250, help='Minimum number of characters required in summary')
    parser.add_argument('--method', type=str, required=True, help='method to select 6 sentences')
    parser.add_argument('--index_path', type=str, required=True, help='indices of the remaining sentences of the truncated document')
    parser.add_argument('--write_path', type=str, required=True,help='path to store the processed dataset')

    args = parser.parse_known_args()[0]
    assert exists(args.data_path)

    process_data(args)