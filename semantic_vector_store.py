from datasets import load_from_disk, Dataset
from transformers import AutoTokenizer, AutoModel
import os
import json
import torch
import logging
import pandas as pd

os.environ['KMP_DUPLICATE_LIB_OK']='True'
class SemanticVectorStore():
    def __init__(self, path, vanila_path=None):
        logging.basicConfig(level=logging.INFO)
        self.path = path

        # if vanila path is a file, then ignore
        if vanila_path is not None and not vanila_path.endswith(".csv"):
            logging.error("Vanila path has to end with .csv")
            return 
        
        self.vanila_path = vanila_path
        
        logging.info("Loading model")
        model_ckpt = "sentence-transformers/all-MiniLM-L6-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
        self.model = AutoModel.from_pretrained(model_ckpt)

        self.device = torch.device("cpu")
        self.model.to(self.device)
        
        logging.info("Initializing embedding dataset")
        self.embeddings_dataset = None
        self.embeddings_dataset = self.initiaze_embeddings_dataset()

        logging.info("Done initializing")
    

    def get_embeddings(self, text_list):
        encoded_input = self.tokenizer(
            text_list, padding=True, truncation=True, return_tensors="pt"
        )
        encoded_input = {k: v.to(self.device) for k, v in encoded_input.items()}
        model_output = self.model(**encoded_input)
        # cls_pooling
        return model_output.last_hidden_state[:, 0]

    def initiaze_embeddings_dataset(self):
        if os.path.exists(self.path):
            embeddings_dataset = load_from_disk(self.path)
            embeddings_dataset.add_faiss_index(column="embeddings")
            return embeddings_dataset

        data = pd.read_csv(self.vanila_path)
        data['vector_text'] = data.apply(lambda x: "Title: {}\n\nAbstract: {}".format(x['title'], x['gpt_summary']), axis=1)

        df = Dataset.from_pandas(data)
        embeddings_dataset = df.map(
            lambda x: {"embeddings": self.get_embeddings(x["vector_text"]).detach().cpu().numpy()[0]}
        )
        
        if not os.path.exists(self.path):
            embeddings_dataset.save_to_disk(self.path)
        
        embeddings_dataset.add_faiss_index(column="embeddings")
        return embeddings_dataset
    

    def search(self, query, k=5):
        if self.embeddings_dataset is None:
            logging.error("embedding dataset is not initialized")
            return {"error": "embedding dataset is not initialized"}
        query_embedding = self.get_embeddings([query]).cpu().detach().numpy()
        scores, samples = self.embeddings_dataset.get_nearest_examples(
            "embeddings", query_embedding, k=k
        )

        samples_df = pd.DataFrame.from_dict(samples)
        samples_df["scores"] = scores
        samples_df.sort_values("scores", ascending=False, inplace=True)

        # return all the dataframe
        embeddings_df = pd.DataFrame(self.embeddings_dataset)
        combined_df = pd.concat([samples_df, embeddings_df], axis=0, ignore_index=True)
        combined_df.drop_duplicates(subset="embeddings", keep="first", inplace=True)

        return combined_df

    
# vs = SemanticVectorStore("static/data/all_vectors", "static/data/overall.csv")
# vs.search("Something about diverse people from other countries use voice assistants/AI?")
        