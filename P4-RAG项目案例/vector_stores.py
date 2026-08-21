
# 向量存储服务类
from langchain_chroma import Chroma
import config_data as config

class VectorStoreService(object):
    def __init__(self, embedding):
        # embedding 指定的嵌入模型
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name = config.collection_name, # 数据库表名
            embedding_function = self.embedding, # 选择向量embedding模型
            persist_directory = config.persist_dicectory, # 数据库本地存储路径
        )

    def get_retriever(self, ):
        # 返回向量检索器 方便加入chain
        return self.vector_store.as_retriever(search_kwargs={'k':config.similarity_threshold})

if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings

    embedding_function = DashScopeEmbeddings(
            dashscope_api_key = "sk-ws-H.EPYYHIM.bya3.MEQCIB3Kac1trAgjONrJ8DyDPwY1A17jPtysaeyQso_j1UbDAiAD0DESCU4Q7vDnYnXEAXn6XE8ThyzGh5Bd4Yb4CQGx5A",
            model = 'text-embedding-v4'
        )

    retriever = VectorStoreService(embedding_function).get_retriever() # 返回值是个retriever对象 集成自Runnable 可调用invoke方法
    res = retriever.invoke("conda中查找文件") # 调用模型查找

    print(res)
