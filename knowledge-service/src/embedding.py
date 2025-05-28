import numpy as np
from typing import List
import logging

logger = logging.getLogger(__name__)

class EmbeddingModel:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        logger.info(f"Embedding model initialized with dimension {dimension}")
    
    def embed_text(self, text: str) -> np.ndarray:
        """将文本转换为向量嵌入"""
        # 这里使用简单的随机向量作为示例
        # 实际应用中应该使用预训练的语言模型
        embedding = np.random.randn(self.dimension)
        embedding = embedding / np.linalg.norm(embedding)
        return embedding
    
    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """批量转换文本为向量嵌入"""
        return [self.embed_text(text) for text in texts] 