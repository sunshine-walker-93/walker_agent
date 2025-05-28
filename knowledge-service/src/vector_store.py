import numpy as np
from typing import List, Dict, Optional
import logging
from .document import Document

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.documents: List[Document] = []
        self.embeddings: List[np.ndarray] = []
        logger.info("Vector store initialized")
    
    def add_document(self, document: Document, embedding: np.ndarray) -> None:
        """添加文档和其向量嵌入"""
        self.documents.append(document)
        self.embeddings.append(embedding)
        logger.info(f"Added document with ID: {document.id}")
    
    def search(self, query_embedding: np.ndarray, limit: int = 5) -> List[Dict]:
        """搜索最相似的文档"""
        if not self.documents:
            return []
        
        # 计算余弦相似度
        similarities = [
            np.dot(query_embedding, doc_embedding) / 
            (np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding))
            for doc_embedding in self.embeddings
        ]
        
        # 获取最相似的文档
        top_indices = np.argsort(similarities)[-limit:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "document": self.documents[idx],
                "similarity": float(similarities[idx])
            })
        
        logger.info(f"Search completed, found {len(results)} results")
        return results
    
    def get_stats(self) -> Dict:
        """获取知识库统计信息"""
        return {
            "total_documents": len(self.documents),
            "average_embedding_dim": len(self.embeddings[0]) if self.embeddings else 0
        }
    
    def clear(self) -> None:
        """清空知识库"""
        self.documents.clear()
        self.embeddings.clear()
        logger.info("Vector store cleared") 