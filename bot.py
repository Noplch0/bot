from graia.ariadne.app import Ariadne
from graia.ariadne.entry import config
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Friend

app = Ariadne(
    config(
        verify_key="lkijnfgh",  # 填入 VerifyKey
        account=3079809050,  # 你的机器人的 qq 号
    ),
)


@app.broadcast.receiver("FriendMessage")
async def friend_message_listener(app: Ariadne, friend: Friend):
    await app.send_message(friend, MessageChain([Plain("Hello, World!")]))
    # 实际上 MessageChain(...) 有没有 "[]" 都没关系


app.launch_blocking()
