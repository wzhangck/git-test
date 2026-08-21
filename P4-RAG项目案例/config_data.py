
md5_path = 'C:\\Users\\37696\\Desktop\\大模型技术资料\\黑马\\黑马\\代码\\/md5_text' # 存储已处理过的md5文件

# Chroma相关
collection_name = 'rag'
persist_dicectory = 'C:\\Users\\37696\\Desktop\\大模型技术资料\\黑马\\黑马\\代码\\chroma_db'

# Spliter相关
chunk_size = 1000 # 分割后的文本段最大长度 字符个数
chunk_overlap = 100 # 连续文本段之间重叠数量
separators = ['\n\n', '\n', '.'] # 自然段落划分的符号
max_split_char_number = 1000

# 相似度检索阈值
similarity_threshold = 2 # 检索返回匹配的文档数量

# session_id配置
session_config = {
    'configurable':{
        'session_id':'user_001'
    }
}
