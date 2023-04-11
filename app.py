import openai
import uvicorn
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from newspaper import Article
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

app = FastAPI()
# app.mount("/", StaticFiles(directory="website"), name="website")

@app.get("/")
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
    OPENAI_API_KEY = load_token_keys(token_keys_path)['OPENAI_API_KEY']
    openai.api_key = OPENAI_API_KEY
    prompt = "Does the article above discuss unintended or undesirable consequences of <domain> on society? Note specifically about <domain>. Answer only Yes or No."
    try:
        answer = complete("{} \n\n{}".format(text, prompt.replace("<domain>", domain)))
    except:
        answer = "The article is too long to be processed by GPT-3."
    
    if 'no' in answer.lower():
        return False
    else:
        return True


def run_summarizer(text, domain):
    OPENAI_API_KEY = load_token_keys(token_keys_path)['OPENAI_API_KEY']
    openai.api_key = OPENAI_API_KEY
    prompt = "To summarize in a short paragraph under 70 tokens, the main undesirable consequence of <domain> being discussed here:"
    answer = complete("{} \n\n{}".format(text, prompt.replace("<domain>", domain)))
    return answer

    
def run_aspect_classifier(title, summary, domain):
    OPENAI_API_KEY = load_token_keys(token_keys_path)['OPENAI_API_KEY']
    openai.api_key = OPENAI_API_KEY
    prompt = "List of possible aspects: Health & Well-being, Security & Privacy, Equality & Justice, User Experience, Economy, Access to Information & Discourse, Environment & Sustainability, Politics, Power Dynamics, Social Norms & Relationship. \n" + \
            "Which one aspect of life does the following consequence affect? (Please only select one) \n" + \
            "Title: <title> \n" + "Summary: <summary> \n" + "Aspect: "
    answer = complete("{}".format(prompt.replace("<title>", title).replace("<summary>", summary)))
    return answer

@app.post("/request")
def process(article: ArticleRequest):
    print("???")
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

# from apscheduler.schedulers.background import BackgroundScheduler
# import subprocess

# scheduler = BackgroundScheduler()
# def call_script():
#     subprocess.run(['/bin/bash', './run.sh'])
# scheduler.add_job(call_script, 'cron', day_of_week='sun', hour=0, minute=0)
# scheduler.add_job(call_script, 'interval', seconds=30)
# scheduler.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)