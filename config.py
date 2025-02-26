import os

class Config:
    # Vector Database
    VECTOR_DIM = 384
    ANNOY_METRIC = 'angular'
    ANNOY_TREES = 50
    VECTOR_DB_PATH = 'data/vector_index.ann'
    
    # Embeddings
    EMBEDDING_MODEL = 'paraphrase-MiniLM-L6-v2'
    
    # Paths
    RESEARCH_DIR = 'research_papers/'
    UPLOAD_DIR = 'uploads/'
    
    # API Keys (set in .env)
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    
    # UI Settings
    LANGUAGES = {
        "en": "English",
        "mr": "Marathi"
    }