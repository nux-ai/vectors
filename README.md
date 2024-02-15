# Embedding Model Evaluation & Integration Toolkit

Welcome to the **Embedding Model Evaluation & Integration Toolkit**, an open-source project designed to streamline the end-to-end lifecycle of embedding model evaluation, index creation, and querying embeddings. 

Our mission is to provide a robust and simple-to-use interface for developers to leverage the power of embedding models across various applications, from natural language processing to vector search databases.

## 🚀 Purpose

The toolkit aims to empower developers by simplifying the process of:
- **Evaluating** different embedding models to find the best fit for your specific dataset and query patterns.
- **Creating** efficient indices for fast retrieval.
- **Querying** embeddings to unlock insights and patterns within your data.

## 📘 Lifecycle Walkthrough

### 1. Evaluate and Select a Model

Jumpstart your project by evaluating potential models against your data and criteria.

```python
# /utilities/evaluate.py
evaluate_instance = Evaluate(
    model="all-MiniLM-L6-v2", 
    testing_set=[{'text': 'Sample text 1'}, {'text': 'Sample text 2'}]
)

evaluate_instance.evaluate(
    query="Example query", 
    acceptance_criteria={['Sample text 2', 'Sample text 1'],
    order="specific"
)
```

### 2. Mount the Selected Model(s) via HTTP

Easily integrate models into your workflow with HTTP endpoints.

**Mount the model:**
```bash
curl -X POST http://localhost:5000/mount_model \
     -H "Content-Type: application/json" \
     -d '{"model_name": "all-MiniLM-L6-v2"}'
```

**Retrieve an embedding:**
```bash
curl -X POST http://localhost:5000/get_embedding \
     -H "Content-Type: application/json" \
     -d '{"text": "Example text for embedding."}'
```

### 3. Create Your Index

Optimize data retrieval with custom indices tailored to your model's embeddings.

```python
# /cloud/mongodb.py
atlas = Atlas(field_names_and_dims, "index_keyword_map_test")
atlas.create_index()
```

### 4. Load Data Using Selected Model

Embed and store your data efficiently using the model of your choice.

```python
# /utilities/load.py
data_loader = DataLoader("your_db_name", "your_collection_name")
data_loader.load(data_mapping)
```

### 5. Design Query and Evaluate Results

Unleash the full potential of your data with powerful querying capabilities.

```python
client.collection.aggregate([
  {
    '$vectorSearch': {
      'index': 'default',
      'path': 'plot_embedding_384',
      'queryVector': 'lorem ipsum',
      'numCandidates': 150,
      'limit': 10
    }
  },
  {
    '$project':
    {
      'plot': 1, 
      'title' : 1
    }
  }
])
```

## 🗺 Library Roadmap

We're constantly looking to expand the toolkit's capabilities, with plans to include:
- Each time an embedding model is changed:
    - Spark job to paralellize re-embedding 
    - Migration of previous vectors to S3
- Migration of vectors from other stores (ex Pinecone to Mongo)
- Federated KNN querying capabilities.
- Containerization of embedding models for ease of deployment.

## 🌟 Why Contribute?

Contributing to this toolkit not only helps improve a project at the forefront of embedding technology but also connects you with a community of like-minded developers. Whether you're looking to:
- Enhance your understanding of embedding models and their applications.
- Share your expertise and learn from others in the field.
- Drive innovation in embedding model evaluation and integration.

We welcome contributions of all forms, from code improvements and feature additions to documentation and examples!

## 🛠 How to Contribute

1. **Fork the repository:** Start with a personal copy of the project.
2. **Pick an issue or propose a feature:** Look for open issues or suggest new ideas.
3. **Submit a pull request:** Implement your changes and submit a PR for review.