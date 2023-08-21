import openai
import uvicorn
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from newspaper import Article
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
from helper import llmRequester
import os

app = FastAPI()

@app.get("/hello")
async def root():
    return {"message": "Hello World"}

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = "/home/rock/unintended-consequence/model"
token_keys_path = "keys.json"

class ArticleRequest(BaseModel):
    url: str
    domain: str

class ArticleResponse(BaseModel):
    title: str
    text: str
    publish_date: str

class SearchRequest(BaseModel):
    query: str


def load_token_keys(path):
    with open(path, "r") as f:
        return json.load(f)

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


def run_title_classifier(title):
    # load pre-trained model and roberta tokenizer
    print("Loading model and tokenizer...")
    tokenizer, model = load_title_classifier_model(model_path)

    res = evaluate(title, model, tokenizer)
    if res['label'] == 'LABEL_0_irrelevant':
        return False
    else:
        return True


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


def run_content_classifier(text, domain):
    # OPENAI_API_KEY = load_token_keys(token_keys_path)['OPENAI_API_KEY']
    # openai.api_key = OPENAI_API_KEY
    lr = llmRequester()
    prompt = "Does the article above discuss unintended or undesirable consequences of <domain> on society? Note specifically about <domain>. Answer only Yes or No."
    try:
        # answer = complete("{} \n\n{}".format(text, prompt.replace("<domain>", domain)))
        lr.run_llama(prompt=prompt.replace("<domain>", domain), text=text)
    except:
        answer = "The article is too long to be processed by GPT-3."
    
    if 'no' in answer.lower():
        return False
    else:
        return True


def run_summarizer(text, domain):
    # OPENAI_API_KEY = load_token_keys(token_keys_path)['OPENAI_API_KEY']
    # openai.api_key = OPENAI_API_KEY
    lr = llmRequester()
    # prompt = "To summarize in a short paragraph under 70 tokens, the main undesirable consequence of <domain> being discussed here:"
    prompt = '''You goal is to inspire users to be more aware of undesirable consequences of <domain>, using insights from the below input text.
Summarize the undesirable consequence of the technology from the article for lay audience under 70 tokens.'''
    # answer = complete("{} \n\n{}".format(text, prompt.replace("<domain>", domain)))
    answer = lr.run_llama(prompt=prompt.replace("<domain>", domain), text=text)
    return answer

    
def run_aspect_classifier(title, summary, domain):
    # OPENAI_API_KEY = load_token_keys(token_keys_path)['OPENAI_API_KEY']
    # openai.api_key = OPENAI_API_KEY
    lr = llmRequester()
    prompt = '''List of possible domain: Health & Well-being, Security & Privacy, Equality & Justice, User Experience, Economy, Access to Information & Discourse, Environment & Sustainability, Politics, Power Dynamics, Social Norms & Relationship. 

Which one aspect of life does the following consequence affect? (Please only select one)
    
Summary of the consequence: "{text}"

One Aspect ((Please only select one from above):'''
    # prompt = "List of possible aspects: Health & Well-being, Security & Privacy, Equality & Justice, User Experience, Economy, Access to Information & Discourse, Environment & Sustainability, Politics, Power Dynamics, Social Norms & Relationship. \n" + \
    #         "Which one aspect of life does the following consequence affect? (Please only select one) \n" + \
    #         "Title: <title> \n" + "Summary: <summary> \n" + "Aspect: "
    # answer = complete("{}".format(prompt.replace("<title>", title).replace("<summary>", summary)))
    answer = lr.run_llama(prompt=prompt, text=summary)
    return answer

@app.post("/request")
def process(article: ArticleRequest):
    fetched_article = fetch_article(article.url)
    
    is_title_relevant = run_title_classifier(fetched_article['title'])
    is_content_relevant = run_content_classifier(fetched_article['text'], article.domain)
    summary = run_summarizer(fetched_article['text'], article.domain)
    aspect = run_aspect_classifier(fetched_article['title'], summary, article.domain)
    
    return {
        "title_relevant": is_title_relevant,
        "content_relevant": is_content_relevant,
        "summary": summary,
        "aspect": aspect,
        "title": fetched_article['title'],
    }

def fetch_article(url):
    a = Article(url)
    a.download()
    a.parse()

    return {
        "title": a.title,
        "text": a.text,
        "publish_date": str(a.publish_date)
    }
    # return ArticleResponse(title=a.title, text=a.text, publish_date=str(a.publish_date))

# semantic search
from transformers import AutoTokenizer, AutoModel
import torch
from datasets import Dataset 
import pandas as pd

model_ckpt = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
model = AutoModel.from_pretrained(model_ckpt)

device = torch.device("cpu")
model.to(device)

def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]

def get_embeddings(text_list):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="pt"
    )
    encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
    model_output = model(**encoded_input)
    return cls_pooling(model_output)

from datasets import load_from_disk
def build_vector_store():
    vector_path = "static/data/vectors"
    if os.path.exists(vector_path):
        embeddings_dataset = load_from_disk(vector_path)
        embeddings_dataset.add_faiss_index(column="embeddings")
        return embeddings_dataset

    with open("static/data/aspect.json", "r") as f:
        aspects = json.load(f)
        lst = []
        for aspect in aspects:
            lst.append("Title: {}\n\nAbstract: {}".format(
                    aspect['title'], aspect['abstract']))

    rows = [{"text": i} for i in lst]

    df = Dataset.from_pandas(pd.DataFrame(rows))
    embeddings_dataset = df.map(
        lambda x: {"embeddings": get_embeddings(x["text"]).detach().cpu().numpy()[0]}
    )
    
    if not os.path.exists(vector_path):
        embeddings_dataset.save_to_disk(vector_path)
    embeddings_dataset.add_faiss_index(column="embeddings")
    return embeddings_dataset

embeddings_dataset = build_vector_store()
os.environ['KMP_DUPLICATE_LIB_OK']='True'
@app.post("/search")
def search(searchRequest: SearchRequest):
    question_embedding = get_embeddings([searchRequest.query]).cpu().detach().numpy()
    print("....")
    scores, samples = embeddings_dataset.get_nearest_examples(
        "embeddings", question_embedding, k=10
    )
    print("?")
    samples_df = pd.DataFrame.from_dict(samples)
    samples_df["scores"] = scores
    print("??")
    samples_df.sort_values("scores", ascending=False, inplace=True)
    print("???")
    
    for _, row in samples_df.iterrows():
        print("__________ {} __________".format(_))
        print(row.text)
        print()

from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

scheduler = BackgroundScheduler()
def call_script():
    subprocess.run(['/bin/bash', './run.sh'])
call_script()
# scheduler.add_job(call_script, 'cron', hour=0, minute=1)
# scheduler.add_job(call_script, 'interval', seconds=300)
scheduler.start()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def display(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)