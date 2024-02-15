import requests
from requests.auth import HTTPDigestAuth
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class Atlas:
    def __init__(self, field_names_and_dims, index_name="default"):
        self.cluster_name = os.getenv("CLUSTER_NAME")
        self.group_id = os.getenv("GROUP_ID")
        self.public_key = os.getenv("PUBLIC_KEY")
        self.private_key = os.getenv("PRIVATE_KEY")
        self.field_names_and_dims = field_names_and_dims
        self.index_name = index_name
        self.base_url = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{self.group_id}/clusters/{self.cluster_name}/fts/indexes?pretty=true"

    def create_index(self):
        # Prepare the data payload
        data = {
            "collectionName": "index_mapping",
            "database": "test",
            "name": self.index_name,
            "mappings": {
                "dynamic": True,
                "fields": self._generate_fields_mapping()
            }
        }

        # Make the request to create the index
        response = requests.post(self.base_url, headers={'Content-Type': 'application/json'},
                                 data=json.dumps(data),
                                 auth=HTTPDigestAuth(self.public_key, self.private_key))
        print(response.text)

    def _generate_fields_mapping(self):
        # Generate the fields mapping based on provided field names and dimensions
        fields_mapping = {}
        for field_name, dim in self.field_names_and_dims:
            fields_mapping[field_name] = {
                "dimensions": dim,
                "similarity": "euclidean",
                "type": "knnVector"
            }
        return fields_mapping
