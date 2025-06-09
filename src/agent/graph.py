import os
from typing import Optional

from typing_extensions import Literal
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

RoleId = Literal[11063, 11064, 12]


@tool  # (return_direct=True)
def add_user(user_name: str, name: str, role_ids: list[RoleId], phone: Optional[int] = None, fake: bool = False) -> str:
    """创建用户、账号

    Args:
        user_name: 用户登录账号(必须)，默认用户昵称(中文转拼音)
        name: 用户昵称(必须)
        role_ids: 用户角色(必须)，选项：轻量-管理员(11063)、轻量-生产人员(11064)、用户账号管理员(12)
        phone: 用户手机号(非必须)，默认为空
        fake: 是否为虚拟用户(非必须)
    """
    print(f'{{"username":"{user_name}","name":"{name}","roleIds":"{role_ids}","phone":"{phone}","fake":"{fake}"}}')
    return "success"


# qwen模型适配OpenAI
llm_adapter = ChatOpenAI(
    model="qwen-max",
    api_key=os.getenv("TONGYI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", )

# class UserAddCO(BaseModel):
#     user_name: str = Field(None, description="用户登录账号")
#     name: str = Field(None, description="用户昵称")
#     role_ids: Literal[11063, 11064] = Field(None, description="轻量-管理员(11063)、轻量-生产人员(11064)")
#     fake: bool = Field(False, description="是否为虚拟用户")
#
#
# add_user_llm = llm_adapter.with_structured_output(UserAddCO)

graph = create_react_agent(
    model=llm_adapter,
    tools=[add_user],
    prompt="你是一位小工单系统的助手"
)

# graph = create_supervisor(
#     agents=[add_user_assistant],
#     model=llm_adapter,
#     prompt=(
#         "你是一位小工单系统的助手"
#     )
# ).compile()
