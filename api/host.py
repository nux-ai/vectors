import json
from sentence_transformers import SentenceTransformer

# Assuming Host class is defined here or imported from another file


class Host:
    def __init__(self, model_config_path):
        self.models = self._load_model_config(model_config_path)
        if self.models:
            self.model_name = self.models[0]['model_name']
            self.model = self._load_model(self.models[0])

    def _load_model_config(self, model_config_path):
        try:
            with open(model_config_path, 'r') as file:
                models = json.load(file)
                return models
        except Exception as e:
            print(f"Failed to load model configurations. Error: {e}")
            return None

    def _load_model(self, model_info):
        try:
            if model_info['invokation'] == 'sentence-transformers':
                model = SentenceTransformer(model_info['model_name'])
                return model
            else:
                print(
                    f"Unsupported invocation method: {model_info['invokation']}")
                return None
        except Exception as e:
            print(
                f"Failed to load model {model_info['model_name']}. Error: {e}")
            return None

    def get_embedding(self, text):
        if self.model:
            embedding = self.model.encode([text])  # Ensure text is in a list
            return embedding[0]  # Return the first (and only) embedding
        else:
            return "Model not loaded."
