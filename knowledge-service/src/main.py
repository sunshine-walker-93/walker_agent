from fastapi import FastAPI, HTTPException
from typing import List, Optional
import logging
from .vector_store import VectorStore
from .document import Document, DocumentCreate

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Knowledge Service")

# 初始化向量存储
vector_store = VectorStore()

@app.post("/knowledge/documents")
async def add_document(document: DocumentCreate):
    """添加新文档到知识库"""
    try:
        doc = Document(
            content=document.content,
            metadata=document.metadata
        )
        vector = await vector_store.embed(doc.content)
        result = await vector_store.add(vector, doc.metadata)
        return {"success": True, "document_id": result}
    except Exception as e:
        logger.error(f"Error adding document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge/search")
async def search_documents(query: str, limit: int = 5):
    """搜索相关文档"""
    try:
        vector = await vector_store.embed(query)
        results = await vector_store.search(vector, limit)
        return {
            "success": True,
            "results": results
        }
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge/stats")
async def get_stats():
    """获取知识库统计信息"""
    try:
        stats = await vector_store.get_stats()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/knowledge/clear")
async def clear_knowledge_base():
    """清空知识库"""
    try:
        await vector_store.clear()
        return {"success": True}
    except Exception as e:
        logger.error(f"Error clearing knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004) 