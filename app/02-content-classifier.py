import openai
import json
import tqdm
import pandas as pd
import pickle
import argparse
import os
from helper import llmRequester

def read_db(db_path):
    with open(db_path, "rb") as f:
        return pickle.load(f)


def load_token_keys(path):
    with open(path, "r") as f:
        return json.load(f)
    

def get_filter_prompt():
    return "Does the article discuss unintended or undesirable consequences of <domain> on society? Answer only Yes or No.\n\n\"{text}\""


def complete(prompt):
    completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=70,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=1
        )
    return completion.choices[0].text.strip()


def filter_by_content(articles, prompt):
    rows = []

    lr = llmRequester()
    for article in tqdm.tqdm(articles):
        if article['prediction'] == 'LABEL_0_irrelevant':
            continue

        text = article['text']
        if len(text) > 13000:
            continue 
        # answer = complete("{} \n\n{}".format(text, prompt.replace("<domain>", article['sector'])))
        answer = lr.run_llama(prompt=prompt.replace("<domain>", article['sector']), text=text)

        rows.append({
            'title': article['title'],
            'text': article['text'],
            'sector': article['sector'],
            'source': article['source'],
            'url': article['url'],
            'published_at': article['published_at'],
            'prediction': article['prediction'],
            'score': article['score'],
            'gpt3_filter_answer': answer
        })
    
    return rows



def main(input_data_path, token_keys_path, output_data_path):
    # read articles
    print("Reading articles from {}".format(input_data_path))
    articles = read_db(input_data_path)

    # load token keys
    # OPENAI_API_KEY = load_token_keys(token_keys_path)['OPENAI_API_KEY']
    # openai.api_key = OPENAI_API_KEY

    # second filter by content using GPT-3
    print("Filtering articles by content...")
    content_filtered_articles = filter_by_content(articles, get_filter_prompt())
    
    print("Saving filtered articles to {}".format(output_data_path))
    with open(output_data_path, "wb") as f:
        pickle.dump(content_filtered_articles, f, protocol=pickle.HIGHEST_PROTOCOL)

    print("Done with content classifier!")



if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.INFO)
    logging.info("### Running content classifier ###")

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_data_path', required=True)
    parser.add_argument('--token_keys', required=True)
    parser.add_argument('--output_data_path', required=True)
    
    args = parser.parse_args()

    if os.path.exists(args.output_data_path):
        logging.error("Content Classifying... Output path already exists. Exiting...")
    else:
        main(args.input_data_path, args.token_keys, args.output_data_path)