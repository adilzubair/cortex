from typing import List
from langchain_core.documents import Document


class Reranker:
    """Reranks search results using LLM to assess relevance to the query."""
    
    def __init__(self, llm):
        """Initialize reranker with an LLM instance.
        
        Args:
            llm: LangChain LLM instance for scoring relevance
        """
        self.llm = llm
    
    def rerank(self, query: str, documents: List[Document], top_k: int = 5) -> List[Document]:
        """Rerank documents by relevance to the query.
        
        Args:
            query: The search query
            documents: List of documents to rerank
            top_k: Number of top documents to return
            
        Returns:
            List of top_k most relevant documents, ordered by relevance
        """
        if not documents:
            return []
        
        # If we have fewer documents than top_k, return all
        if len(documents) <= top_k:
            return documents
        
        # Create a concise representation of each document for the LLM
        doc_summaries = []
        for i, doc in enumerate(documents):
            # Get first 300 chars of content
            content_preview = doc.page_content[:300].replace('\n', ' ')
            # Include file path from metadata if available
            file_path = doc.metadata.get('path', 'unknown')
            doc_summaries.append(f"[{i}] File: {file_path}\nContent: {content_preview}...")
        
        docs_text = "\n\n".join(doc_summaries)
        
        # Create prompt for LLM to rank documents
        prompt = f"""Given the search query: "{query}"

Rank these code snippets by relevance to the query. Consider:
- How directly the code relates to the query
- Whether it contains definitions or implementations mentioned in the query
- The file path and context

Code snippets:
{docs_text}

Return ONLY the indices of the top {top_k} most relevant snippets, in order from most to least relevant.
Format: comma-separated numbers (e.g., "3,0,7,1,5")
Response:"""
        
        try:
            # Get LLM response
            response = self.llm.invoke(prompt).content.strip()
            
            # Parse the response to extract indices
            indices = []
            for part in response.split(','):
                part = part.strip()
                # Extract first number found in the part
                num_str = ''.join(c for c in part if c.isdigit())
                if num_str and int(num_str) < len(documents):
                    indices.append(int(num_str))
            
            # If we got valid indices, reorder documents
            if indices:
                reranked = [documents[i] for i in indices[:top_k]]
                # If we didn't get enough indices, append remaining docs
                if len(reranked) < top_k:
                    remaining = [doc for i, doc in enumerate(documents) if i not in indices]
                    reranked.extend(remaining[:top_k - len(reranked)])
                return reranked
            else:
                # Fallback: return original order
                return documents[:top_k]
                
        except Exception as e:
            # On any error, fallback to original order
            print(f"Reranking failed: {e}. Using original order.")
            return documents[:top_k]
