
"""
基于Streamlit框架完成WEB网页上传服务

streamlit机制 当页面元素发生变化 则页面重新执行一遍 会造成状态丢失 
"""

import streamlit as st
from knowledge_base import KnowledgeBaseService

# 1.创建网页 设置标题
st.title('知识库更新服务')

# 2.实现文件上传功能
uploader_file = st.file_uploader(
    label = "请上传txt文件", 
    type = ['txt'],
    accept_multiple_files = False, # 是否接受多文件上传
)


# 为了避免重复刷新导致状态丢失的问题 session_state是一个字典 可用户维护全局信息 
if 'service' not in st.session_state:
    st.session_state['service'] = KnowledgeBaseService()

if uploader_file is not None:
    # 表明拿到文件
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024 # 原单位是B 得到KB单位
    st.subheader(f'文件名: {file_name}')
    st.write(f'格式: {file_type} 大小: {file_size:.2f}KB')

    # 获取文件内容  getvalue->bytes-decode('utf-8')
    text = uploader_file.getvalue().decode('utf-8')
    # st.write(text)
    
    result = st.session_state['service'].upload_by_str(text, file_name)
    st.write(result)


