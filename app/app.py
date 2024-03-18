import openai
import uvicorn
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from newspaper import Article
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
from helper import llmRequester
import logging
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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
    allow_credentials=True
)

model_path = "./model"
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
    domain: str
    aspect: str
    
class Message(BaseModel):
    name: str
    title: str
    message: str
    timestamp: str


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
    prompt = '''Does the article below discuss unintended or undesirable consequences of <domain> on society? Note specifically about <domain>. Answer only Yes or No.
"{text}"'''
    try:
        # answer = complete("{} \n\n{}".format(text, prompt.replace("<domain>", domain)))
        answer = lr.run_llama(prompt=prompt.replace("<domain>", domain), text=text)
    except:
        answer = "The article is too long to be processed by GPT-3."
    
    del lr
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

Summarize the undesirable consequence of the technology from the article for lay audience under 70 tokens.

"{text}"'''
    # answer = complete("{} \n\n{}".format(text, prompt.replace("<domain>", domain)))
    answer = lr.run_llama(prompt=prompt.replace("<domain>", domain), text=text)
    del lr
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
    del lr
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
        "aspect": aspect.lower().strip(),
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

from semantic_vector_store import SemanticVectorStore
SEMANTIC_VECTOR_STORE_PATH = "static/data/all_vectors"
OVERALL_CSV_PATH = "static/data/overall.csv"
# OVERALL_CSV_PATH = "../blip-react/src/dataset/dataset.csv"

svs = SemanticVectorStore(SEMANTIC_VECTOR_STORE_PATH, OVERALL_CSV_PATH)

@app.post("/search")
def search(search_request: SearchRequest):
    logging.info("searching for {}".format(search_request.query))
    try:
        # temp_search_df = svs.search(search_request.query)
        # with open("static/data/temp_search.csv", "w") as f:
        #     temp_search_df.to_csv(f, index=False)
        # return {"message": "success"}
        temp_search_titles = svs.search(
            search_request.query, 
            search_request.domain,
            search_request.aspect
            )
        return {
            "message": "success",
            "titles": temp_search_titles
        }
    except:
        return {"message": "error"}

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

# Replace the placeholder with your Atlas connection string
uri = "mongodb+srv://blip-admin:SnLY3HFEPADfJjaM@cluster0.7vdeyys.mongodb.net/"

# Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["iui2024"]
    
@app.post("/create")
async def create(message: Message):
    if not message:
        raise HTTPException(status_code=400, detail="No data provided")
    message_dict = message.dict()
    result = db["messages"].insert_one(message_dict)
    return {"message": "Data added successfully", "data_id": str(result.inserted_id)}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
