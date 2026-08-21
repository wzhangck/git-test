
# RAG服务列
from vector_stores import VectorStoreService # 向量检索类
from langchain_community.embeddings import DashScopeEmbeddings # 文本embedding类
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # 模板类

from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser

from file_history_store import get_history
import config_data as config

class RagService(object):
    def __init__(self, ):
        embedding_function = DashScopeEmbeddings(
            dashscope_api_key = "sk-ws-H.EPYYHIM.bya3.MEQCIB3Kac1trAgjONrJ8DyDPwY1A17jPtysaeyQso_j1UbDAiAD0DESCU4Q7vDnYnXEAXn6XE8ThyzGh5Bd4Yb4CQGx5A",
            model = 'text-embedding-v4'
        )

        # 1.在线向量库检索类 
        self.vector_service = VectorStoreService(
            embedding = embedding_function
        ) # 在线向量存储库的实例类  功能: 用来做检索!

        # 2.提示词模板类
        self.prompt_template = ChatPromptTemplate.from_messages(
            # 提供对应角色和行为 context占位符
            [
                ('system', '以我提供的参考资料为主，精简回答，参考资料:{context}'),
                ('system', '并且我提供用户的对话历史记录, 如下: '),
                MessagesPlaceholder('history'), # 注入历史信息 占位
                ('user', '请回答用户提问 :{input}'),
            ]
        )

        # 3.大模型类
        self.chat_model = ChatTongyi(
            model = 'qwen-max', 
            streaming = True, # 流式输出
            api_key = "sk-ws-H.EPYYHIM.bya3.MEQCIB3Kac1trAgjONrJ8DyDPwY1A17jPtysaeyQso_j1UbDAiAD0DESCU4Q7vDnYnXEAXn6XE8ThyzGh5Bd4Yb4CQGx5A",
        )

        # 4.获取最终的执行链
        self.chain = self.__get_chain()


    def __get_chain(self, ): # 获取最终的执行链条
        retriever = self.vector_service.get_retriever() # 拿到向量库的检索器 

        # 定义执行链
        def format_document(docs):
            if not docs:
                return '无相关参考资料'

            formatted_str = ''
            for doc in docs:
                formatted_str += f'文档片段: {doc.page_content}\n 文档元数据: {doc.metadata}\n\n'

            return formatted_str

        def print_prompt(prompt_template):
            print('='*20)
            print(prompt_template.to_string())
            print('='*20)
            return prompt_template

        def format_for_retriever(value):
            # print('----------', value)
            return value['input']

        def format_for_prompt_template(value):
            # print('----------', value)
            new_value = {}
            new_value['input'] = value['input']['input']
            new_value['context'] = value['context']
            new_value['history'] = value['input']['history']
            return new_value

        # 主要理解链的语法 prompt_template模板类接收的是一个字典 因此需要先将检索器的输出包装为字典 再进行链接
        # 流程:  
        # 1.input先 将用户输出给检索器 2.随后查询出值 继承自Runnable 作为自定义函数的输入
        # 3.得到输入拼接字典输入给模板  4.模板再拿到字典后 给模型 模型输出后解析为字符串
        # input和content是模板类需要注入的变量 注意名字要一一对应
        chain = (
            {
                'input':RunnablePassthrough(), # 作用是原样传递或转发数据 不修改数据，只负责传递数据到下一个节点
                'context':RunnableLambda(format_for_retriever) | retriever | format_document # RunnablLambda(temp)的作用是包装函数 获取dict 作为检索器的输入
            } | RunnableLambda(format_for_prompt_template) | self.prompt_template| print_prompt  | self.chat_model | StrOutputParser()
        )

        # 长期记忆历史类 得到增强链 融合历史信息
        conversation_chain = RunnableWithMessageHistory(
            chain, # 被增强的普通链
            get_history, # 函数
            input_messages_key = 'input', # 用户输入 需要注入的变量
            history_messages_key = 'history', # 历史消息占位的变量
        )

        # return chain
        return conversation_chain # 返回新链

if __name__ == '__main__':
    # session_id配置
    session_config = {
        'configurable':{
            'session_id':'user_001'
        }
    }

    res = RagService().chain.invoke({'input':'春天穿什么颜色的衣服'}, session_config)
    print(res)

