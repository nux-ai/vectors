from sentence_transformers import SentenceTransformer
import hnswlib
import numpy as np
import json


class Evaluate:
    def __init__(self, model_name, test_data_subset):
        self.model_name = model_name
        self.model_info = self._find_model(model_name)
        self.model = self._load_model()
        self.data = test_data_subset
        self.index = self._initialize_hnsw()
        self.model_api_path = 'your_api_path/'

    def _find_model(self, model_name):
        with open('models.json', 'r') as f:
            models = json.load(f)

        # Find the supplied model
        for model in models:
            if model['model_name'] == model_name:
                return model

        # If the model is not found, return None
        return None

    def _load_model(self):
        if self.model_info is None:
            return None

        if self.model_info['invokation'] == 'sentence-transformers':
            # Use the SentenceTransformer class to load the model
            return SentenceTransformer(self.model_name)
        # TODO: other invokation methods
        # elif self.model_info['invokation'] == 'api':
        #     # Use the API path to load the model
        #     return self.model_api_path + self.model_name

    def _initialize_hnsw(self):
        # Initialize an HNSW store with the provided test data subset
        dim = self.model_info['dimensions']
        index = hnswlib.Index(space='cosine', dim=dim)
        index.init_index(
            max_elements=len(self.data),
            ef_construction=200, M=16
        )

        # Embedding the test data and adding to the index
        embeddings = self.model.encode([d['text'] for d in self.data])
        index.add_items(embeddings)

        return index

    def evaluate(self, query, acceptance_criteria):
        # Embed the query
        query_embedding = self.model.encode([query])

        # Performing k-NN search in the HNSW store
        labels, distances = self.index.knn_query(
            query_embedding,
            k=len(self.data)
        )

        # Map labels back to test data objects and calculate match with acceptance criteria
        results = [self.data[label] for label in labels[0]]
        # Here, implement the logic to compare results against acceptance criteria
        # For simplicity, we'll just print the results
        print("Query Results:", results)
        # Implement the comparison with acceptance criteria
        # This part will be specific to how acceptance criteria are defined

        # Return the comparison outcome
        return {"success": True, "details": "This is where details of the comparison would be returned"}
