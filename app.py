from flask import Flask, render_template
from core.chroma_manager import ChromaManager
from core.search_engine import SearchEngine
from routes.api_routes import api_blueprint
import os

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(api_blueprint)
    
    # Initialize ChromaDB
    chroma_manager = ChromaManager()
    chroma_manager.ensure_persistence_directory()
    collection = chroma_manager.get_collection()
    
    # Initialize search engine and load data if empty
    search_engine = SearchEngine(collection)
    if collection.count() == 0:
        search_engine.load_and_process_data()
    else:
        print(f"Using existing collection with {collection.count()} resumes")
    
    @app.route('/')
    def home():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", debug=True)