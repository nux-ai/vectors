import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()


class DataLoader:
    def __init__(self, db, collection):
        self.connection_string = os.getenv("CONNECTION_STRING")
        self.client = MongoClient(self.connection_string)
        self.db = self.client[db]
        self.collection = self.db[collection]
        self.models_info = self._load_models_info()

    def _load_models_info(self):
        # Load models information from models.json
        try:
            with open("models.json", "r") as file:
                models_info = json.load(file)
                return models_info
        except Exception as e:
            print(f"Failed to load models information. Error: {e}")
            return []

    def _get_model(self, model_name):
        # Find the model info by name and load it
        for model_info in self.models_info:
            if model_info['model_name'] == model_name:
                if model_info['invokation'] == 'sentence-transformers':
                    return SentenceTransformer(model_name)
        return None

    def load(self, data_mapping):
        # Process and load data based on the mapping
        for mapping in data_mapping:
            old_field = mapping['old_field_name']
            new_field = mapping['new_field_name']
            model_name = mapping['model']
            model = self._get_model(model_name)

            if model:
                # Query documents, transform, and update
                documents = self.collection.find({})
                for doc in documents:
                    old_value = doc.get(old_field, "")
                    embedding = model.encode([old_value])[
                        0] if old_value else None
                    if embedding is not None:
                        self.collection.update_one({'_id': doc['_id']}, {
                                                   '$set': {new_field: embedding}})
            else:
                print(f"Model {model_name} not found or failed to load.")
