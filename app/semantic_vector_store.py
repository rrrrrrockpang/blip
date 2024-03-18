from datasets import load_from_disk, Dataset
from transformers import AutoTokenizer, AutoModel
import os
import json
import torch
import logging
import pandas as pd
from datasets import concatenate_datasets


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

    
    def batch_embeddings(texts, tokenizer, model, device):
        encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
        with torch.no_grad():
            model_output = model(**encoded_input)
        return model_output.last_hidden_state[:, 0].detach().cpu().numpy()

    def initiaze_embeddings_dataset(self):
        if os.path.exists(self.path):
            embeddings_dataset = load_from_disk(self.path)
            embeddings_dataset.add_faiss_index(column="embeddings")
            return embeddings_dataset
        
        data = pd.read_csv(self.vanila_path)
        data['vector_text'] = data.apply(lambda x: f"Title: {x['title']}\n\nAbstract: {x['gpt_summary']}", axis=1)
        texts = data['vector_text'].tolist()

        # Process in batches
        batch_size = 100 
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_embeddings = batch_embeddings(batch_texts, self.tokenizer, self.model, self.device)
            embeddings.append(batch_embeddings)
        
        embeddings = np.vstack(embeddings)
        data['embeddings'] = embeddings.tolist()
        embeddings_dataset = Dataset.from_pandas(data)
        
        embeddings_dataset.save_to_disk(self.path)
        embeddings_dataset.add_faiss_index(column="embeddings")
        return embeddings_dataset



    # def initiaze_embeddings_dataset(self):
    #     if os.path.exists(self.path):
    #         embeddings_dataset = load_from_disk(self.path)
    #         if embeddings_dataset.num_rows == len(pd.read_csv(self.vanila_path)):
    #             embeddings_dataset.add_faiss_index(column="embeddings")
    #             return embeddings_dataset

    #     data = pd.read_csv(self.vanila_path)
    #     data['vector_text'] = data.apply(lambda x: "Title: {}\n\nAbstract: {}".format(x['title'], x['gpt_summary']), axis=1)

    #     df = Dataset.from_pandas(data)
    #     embeddings_dataset = df.map(
    #         lambda x: {"embeddings": self.get_embeddings(x["vector_text"]).detach().cpu().numpy()[0]}
    #     )
        
    #     if not os.path.exists(self.path):
    #         embeddings_dataset.save_to_disk(self.path)
    
    #     if embeddings_dataset.num_rows == len(pd.read_csv(self.vanila_path)):
    #         embeddings_dataset.save_to_disk(self.path)
        
    #     embeddings_dataset.add_faiss_index(column="embeddings")
    #     return embeddings_dataset
    

    def search(self, query, domain, aspect, k=100):
        if self.embeddings_dataset is None:
            logging.error("embedding dataset is not initialized")
            return {"error": "embedding dataset is not initialized"}
        
        query_embedding = self.get_embeddings([query]).cpu().detach().numpy()
        if domain == "" and aspect == "":
            scores, samples = self.embeddings_dataset.get_nearest_examples(
                "embeddings", query_embedding, k=k
            )
        else:
            filtered_datasets = []
            for i, example in enumerate(self.embeddings_dataset):
                if example['sector'] == domain and example['label'] == aspect:
                    filtered_datasets.append(example)
                elif example['sector'] == domain:
                    filtered_datasets.append(example)
                elif example['label'] == aspect:
                    filtered_datasets.append(example)
            if not filtered_datasets:
                return {"error": "No matching entries for the given domain and aspect"}
            
            # print("Number of filtered datasets: ", len(filtered_datasets))
            filtered_datasets = Dataset.from_dict(pd.DataFrame(filtered_datasets))
            if "embeddings" not in filtered_datasets.list_indexes():
                filtered_datasets.add_faiss_index(column="embeddings")

            # query_embedding = self.get_embeddings([query]).cpu().detach().numpy()
            if filtered_datasets.num_rows <= k:
                k = filtered_datasets.num_rows
            scores, samples = filtered_datasets.get_nearest_examples("embeddings", 
                                                                    query_embedding, 
                                                                    k=k)

        samples_df = pd.DataFrame.from_dict(samples)
        samples_df["scores"] = scores
        samples_df.sort_values("scores", ascending=True, inplace=True)

        # print(samples_df["title"].tolist())
        return samples_df["title"].tolist()

    
# vs = SemanticVectorStore("static/data/all_vectors", "static/data/overall.csv")
# vs.search("Something about diverse people from other countries use voice assistants/AI?")
        