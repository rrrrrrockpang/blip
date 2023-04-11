import pickle
import json
import argparse
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline


def read_db(path):
    with open(path, "rb") as f:
        dic = pickle.load(f)
    return [value for key, value in dic.items()]


def load_title_classifier_model(model_path):
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
    return tokenizer, model


def evaluate(text, model, tokenizer):
    pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer)
    res = pipe(text)[0]
    if res['label'] == 'LABEL_0':
        res['label'] = "{}_{}".format(res['label'], 'irrelevant')
    else: 
        res['label'] = "{}_{}".format(res['label'], 'relevant')
    return res


def filter_relevance_by_title(article_ls, model, tokenizer):
    rows = []
    for article in tqdm(article_ls):
        res = evaluate(article['title'], model, tokenizer)
        if res['label'] == 'LABEL_0_irrelevant':
            continue
        rows.append({
            'title': article['title'],
            'text': article['text'],
            'sector': article['sector'],
            'source': article['source'],
            'url': article['url'],
            'published_at': article['published_at'],
            'prediction': res['label'],
            'score': res['score']
        })
    return rows


def main(articles, model_path, output_data_path):
    # load pre-trained model and roberta tokenizer
    print("Loading model and tokenizer...")
    tokenizer, model = load_title_classifier_model(model_path)

    print("Reading articles...")
    article_ls = read_db(articles)

    print("Filtering articles by titles...")
    # add namespace "prediction" ('LABEL_0_irrelevant' or 'LABEL_1_relevant')
    filtered_articles = filter_relevance_by_title(article_ls, model, tokenizer)
    
    print("Saving filtered articles...")
    with open(output_data_path, "wb") as f:
        pickle.dump(filtered_articles, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    print("Done with title classifier!")
    print("Filtered articles saved to {}".format(output_data_path))
    print("Total number of articles: {}".format(len(filtered_articles)))
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # possible add a set to store the articles that have been read
    parser.add_argument('--articles', required=True)
    parser.add_argument('--model_path', required=True)
    parser.add_argument('--output_data_path', required=True)
    args = parser.parse_args()

    main(args.articles, args.model_path, args.output_data_path)