import argparse
import pickle
import json
import tqdm
from utils import complete, connect_to_openai
import logging 
import os
from helper import llmRequester

def classify_aspect(articles, prompt):
    rows = []
    lr = llmRequester()
    for article in tqdm.tqdm(articles):
        text = article['text']
        if len(text) > 19000:
            continue 
        # answer = complete("{} \n\n{}".format(text, prompt.replace("<title>", article['title']).replace("<summary>", article['gpt3_summary'])))
        print(prompt)
        answer = lr.run_llama(prompt = prompt, text=article["gpt3_summary"])
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
            'gpt3_summary': article['gpt3_summary'],
            'gpt3_aspect': answer
        })
    return rows

def main(input_data_path, token_keys_path, output_data_path):
    # load token keys
    # connect_to_openai(token_keys_path)

    # load articles
    with open(input_data_path, "rb") as f:
        articles = pickle.load(f)

    # filter articles by content
    prompt = '''List of possible domain: Health & Well-being, Security & Privacy, Equality & Justice, User Experience, Economy, Access to Information & Discourse, Environment & Sustainability, Politics, Power Dynamics, Social Norms & Relationship. 

Which one aspect of life does the following consequence affect? (Please only select one)
    
Summary of the consequence: "{text}"

One Aspect ((Please only select one from above):''' # + \
            # "Title: <title> \n" + "Summary: <summary> \n" + "Aspect: " 
    classified_articles = classify_aspect(articles, prompt)

    # print(classified_articles)
    # print(len(classified_articles))

    # save filtered articles
    with open(output_data_path, "wb") as f:
        pickle.dump(classified_articles, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_data_path', required=True)
    parser.add_argument('--token_keys', required=True)
    parser.add_argument('--output_data_path', required=True)
    
    args = parser.parse_args()

    if os.path.exists(args.output_data_path):
        logging.error("Categorizing... Output path already exists. Exiting...")
    else:
        main(args.input_data_path, args.token_keys, args.output_data_path)