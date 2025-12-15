from app.core.vectordb import load_vector_db
import logging

logger = logging.getLogger(__name__)

def retrieve_context(query: str, k: int = 3):
    """
    Retrieves the most relevant document chunks from the vector database.
    
    Args:
        query: The user's question.
        k: The number of document chunks to retrieve.
        
    Returns:
        A tuple containing the combined context string and a list of source filenames.
    """
    try:
        vectordb = load_vector_db()
        if not vectordb:
            logger.error("Vector DB not loaded.")
            return "", []
            
        results = vectordb.similarity_search(query, k=k)
        
        if not results:
            logger.info(f"No documents found for query: {query}")
            return "", []

        context = "\n\n".join([doc.page_content for doc in results])

        sources = list(set([doc.metadata.get("source", "") for doc in results]))
        
        logger.info(f"Retrieved {len(results)} documents for query: {query}")

        return context, sources
    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        return "", []
