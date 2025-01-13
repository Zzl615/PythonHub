from pydantic import BaseModel, Field, validator
from typing import List

class Message(BaseModel):
    name: str = Field("", description="称呼")
    content: str = Field(..., description="消息内容")

class CallRequest(BaseModel):
    """
    医疗对话参数
    """
    messages: List[Message] = Field(None, description="对话内容")
    stream: bool = Field(False, description="是否流式")
    
    @validator("messages", always=True)
    def cut_off_messages(cls, v):
        if isinstance(v, list):
            total_length = 0
            messages = []
            for message in reversed(v):
                message_content_length = len(message.content)
                if total_length + message_content_length >= 4000:
                    remaining_length = 4000 - total_length
                    message.content = message.content[:remaining_length]
                    messages.insert(0, message)
                    break
                messages.insert(0, message)
                total_length += message_content_length
            return messages
        return v
    

def test_long_message():
    # 测试01：第一条消息，超过4000字符
    
    request1 = CallRequest(
        messages=[
            Message(name="user", content="a"*4001)
        ]
    )

    assert request1.messages[0].content == "a"*4000

    

    # 测试02：多条消息，总长度超过4000字符

    request2 = CallRequest(
        messages=[
            Message(name="user", content="a"*1000),
            Message(name="user", content="b"*1000),
            Message(name="user", content="c"*2000+"d"*1000)
        ]
    )
    
    assert len(request2.messages) == 2
    assert request2.messages[0].content == "b"*1000
    assert request2.messages[1].content == "c"*2000+"d"*1000
    

    

    # 测试03：多条消息，总长度不超过4000字符

    request3 = CallRequest(
        messages=[
            Message(name="user", content="a"*1000),
            Message(name="user", content="b"*1000),
            Message(name="user", content="c"*1000),
            Message(name="user", content="d"*1001),
            Message(name="user", content="e"*1000)
        ]
    )

    assert len(request3.messages) == 4
    assert request3.messages[0].content == "b"*999
    assert request3.messages[1].content == "c"*1000
    assert request3.messages[2].content == "d"*1001
    assert request3.messages[3].content == "e"*1000



test_long_message()