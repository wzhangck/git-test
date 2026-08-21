
"""
知识库基础代码服务
"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma # 向量数据库
from langchain_community.embeddings import DashScopeEmbeddings # 向量模型
from langchain_text_splitters import RecursiveCharacterTextSplitter # 递归文件分割器
from datetime import datetime

def check_md5(md5_str):
    # 检查传入的MD5字符串是否已被处理过
    if not os.path.exists(config.md5_path):
        # 如果文件不存在 则说明没处理过该字符串
        open(config.md5_path, 'w', encoding='utf-8').close() # 创建空文件
        return False
    else:# 如果存在 则拿到所有行
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False


def save_md5(md5_str):
    # 将传入的md5字符串 记录到文件中保存 以免重复处理
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n') # 跟上换行符 写完后切换到下一行


def get_string_md5(input_str, encoding='utf-8'):
    # 将传入的字符串转为md5字符串
    # 将字符串转换为字节流数组bytes
    str_bytes = input_str.encode(encoding=encoding)

    # 创建md5对象
    md5_obj = hashlib.md5() # 得到md5
    md5_obj.update(str_bytes) # 更新内容 传入要转换的字节数组
    md5_hex = md5_obj.hexdigest() # 得到md5的16进制字符串
    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self, ):
        os.makedirs(config.persist_dicectory, exist_ok=True)
        self.chroma = Chroma(
            collection_name = config.collection_name, # 数据库表名
            embedding_function = DashScopeEmbeddings(
                dashscope_api_key = "sk-ws-H.EPYYHIM.bya3.MEQCIB3Kac1trAgjONrJ8DyDPwY1A17jPtysaeyQso_j1UbDAiAD0DESCU4Q7vDnYnXEAXn6XE8ThyzGh5Bd4Yb4CQGx5A",
                model = 'text-embedding-v4'
            ), # 选择向量embedding模型
            persist_directory = config.persist_dicectory, # 数据库本地存储路径
        ) # chroma在线向量数据库 存储向量 实例类

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size, # 分割后的文本段最大长度
            chunk_overlap = config.chunk_overlap, # 连续文本段之间重叠数量
            separators = config.separators, # 自然段落划分的符号
            length_function = len, # 计算长度的函数 使用python自带的len函数计算长度

        ) # 文本分割器 实例

    def upload_by_str(self, data, filename):
        # 将当前传入的字符串 进行向量化 存入chroma向量数据库中
        # 先得到传入字符串的md5值
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "跳过 内容已存在知识库中"

        if len(data) > config.max_split_char_number:
            # 传入字符长度大于最小要分割的长度才进行分割 否则不用分割 直接计算
            knowledge_chunk = self.spliter.split_text(data) # 返回值是个list 存储的是原始文本字符串 还没有计算md5

        else:
            knowledge_chunk = [data]

        # print('knowledge_chunk: ', knowledge_chunk)

        metadata = {
            'source':filename,
            'create_time':datetime.now().strftime('%Y-%m-%d'),
            'operator':'zw',
        }

        self.chroma.add_texts(
            knowledge_chunk,
            metadatas = [metadata for _ in knowledge_chunk] # 每个原文档都对应一份meta信息
        )

        save_md5(md5_hex)

        return '成功存储到向量库chroma中'

if __name__ == '__main__':

    service = KnowledgeBaseService()

    print(service.upload_by_str('周杰伦', 'testfile'))




