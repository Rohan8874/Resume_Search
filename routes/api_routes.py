from flask import Blueprint, jsonify, request
from core.search_engine import SearchEngine
from core.chroma_manager import ChromaManager

api_blueprint = Blueprint('api', __name__)

# Initialize components
chroma_manager = ChromaManager()
collection = chroma_manager.get_collection()
search_engine = SearchEngine(collection)

@api_blueprint.route('/api/search', methods=['POST'])
def search_resumes():
    data = request.get_json()
    query = data.get('query', '')
    n_results = data.get('n_results', 5)
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        similar_resumes = search_engine.find_similar_resumes(query, n_results)
        return jsonify({
            "query": query,
            "results": similar_resumes
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500