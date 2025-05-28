from typing import List, Optional, Dict, Any
import chromadb
from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import (
    TextLoader,
    UnstructuredPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)
import os
from datetime import datetime

class KnowledgeBase:
    def __init__(self, persist_directory: str = "data/chroma"):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
        )
        self.vector_store = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """初始化向量存储"""
        try:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        except Exception:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
    
    def _get_loader(self, file_path: str):
        """根据文件类型获取对应的加载器"""
        ext = os.path.splitext(file_path)[1].lower()
        loaders = {
            '.txt': TextLoader,
            '.pdf': UnstructuredPDFLoader,
            '.docx': Docx2txtLoader,
            '.md': UnstructuredMarkdownLoader
        }
        return loaders.get(ext)
    
    def add_file(self, file_path: str) -> Dict[str, Any]:
        """添加文件到知识库"""
        try:
            loader_class = self._get_loader(file_path)
            if not loader_class:
                return {
                    "success": False,
                    "message": f"不支持的文件类型: {os.path.splitext(file_path)[1]}"
                }
            
            loader = loader_class(file_path)
            documents = loader.load()
            
            # 添加元数据
            for doc in documents:
                doc.metadata.update({
                    "source": file_path,
                    "added_time": datetime.now().isoformat(),
                    "file_type": os.path.splitext(file_path)[1][1:].upper()
                })
            
            # 分割文档
            texts = self.text_splitter.split_documents(documents)
            
            # 添加到向量存储
            self.vector_store.add_documents(texts)
            self.vector_store.persist()
            
            return {
                "success": True,
                "message": f"成功添加文件: {file_path}",
                "chunks": len(texts)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"添加文件失败: {str(e)}"
            }
    
    def add_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """添加文本到知识库"""
        try:
            # 分割文本
            texts = self.text_splitter.split_text(text)
            
            # 准备元数据
            if metadata is None:
                metadata = {}
            metadata.update({
                "added_time": datetime.now().isoformat(),
                "source": "direct_input"
            })
            
            # 添加到向量存储
            self.vector_store.add_texts(texts, metadatas=[metadata] * len(texts))
            self.vector_store.persist()
            
            return {
                "success": True,
                "message": "成功添加文本",
                "chunks": len(texts)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"添加文本失败: {str(e)}"
            }
    
    def search(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        """搜索知识库"""
        if not self.vector_store:
            return []
        
        docs = self.vector_store.similarity_search_with_score(query, k=k)
        results = []
        for doc, score in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            })
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """获取知识库统计信息"""
        if not self.vector_store:
            return {
                "total_documents": 0,
                "sources": []
            }
        
        collection = self.vector_store._collection
        if not collection:
            return {
                "total_documents": 0,
                "sources": []
            }
        
        # 获取所有文档的元数据
        results = collection.get()
        if not results or not results['metadatas']:
            return {
                "total_documents": 0,
                "sources": []
            }
        
        # 统计不同来源的文档数量
        sources = {}
        for metadata in results['metadatas']:
            source = metadata.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "total_documents": len(results['metadatas']),
            "sources": [
                {"source": source, "count": count}
                for source, count in sources.items()
            ]
        }
    
    def clear(self):
        """清空知识库"""
        if self.vector_store:
            self.vector_store.delete_collection()
            self._initialize_vector_store() 