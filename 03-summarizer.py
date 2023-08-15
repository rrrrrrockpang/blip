import openai
import json
import tqdm
import pandas as pd
import pickle
import argparse
from utils import complete, connect_to_openai
import logging
import os
from helper import llmRequester

def summarize(articles, prompt):
    rows = []
    lr = llmRequester()
    for article in tqdm.tqdm(articles):
        text = article['text']
        if len(text) > 13000:
            continue 
        
        if 'no' in article['gpt3_filter_answer'].lower():
            continue

        # answer = complete("{} \n\n{}".format(text, prompt.replace("<domain>", article['sector'])))
        answer = lr.run_llama(prompt=prompt.replace("<domain>", article['sector']),
                              text=text)

        rows.append({
            'title': article['title'],
            'text': article['text'],
            'sector': article['sector'],
            'source': article['source'],
            'url': article['url'],
            'published_at': article['published_at'],
            'prediction': article['prediction'],
            'score': article['score'],
            'gpt3_filter_answer':  article['gpt3_filter_answer'],
            'gpt3_summary': answer
        })

    return rows


def main(input_data_path, token_keys_path, output_data_path):
    # load token keys
    # connect_to_openai(token_keys_path)

    # load articles
    with open(input_data_path, "rb") as f:
        articles = pickle.load(f)

    # filter articles by content
    # prompt = "To summarize in a short paragraph under 70 tokens, the main undesirable consequence of <domain> being discussed here:"
    prompt = '''
    You goal is to inspire users to be more aware of undesirable consequences of digital technologies, using insights from the below input text.
    Summarize the undesirable consequence of the technology from the paper for lay audience under 70 tokens.
    '''
    summarized_articles = summarize(articles, prompt)

    # save filtered articles
    with open(output_data_path, "wb") as f:
        pickle.dump(summarized_articles, f)

    print("Done!")
    print("Saved to {}".format(output_data_path))
    print("Number of articles: {}".format(len(summarized_articles)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_data_path', required=True)
    parser.add_argument('--token_keys', required=True)
    parser.add_argument('--output_data_path', required=True)
    
    args = parser.parse_args()

    if os.path.exists(args.output_data_path):
        logging.error("Summarizing... Output path already exists. Exiting...")
    else:
        main(args.input_data_path, args.token_keys, args.output_data_path)