from mybotlib.check import *
check_config_file()

from graia.ariadne.app import Ariadne
import pkgutil
from graia.ariadne.entry import config
from graia.saya import Saya
from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import config

saya = create(Saya)

bot_config=BotConfig('botconfig.yaml')

app = Ariadne(
    connection=config(bot_config.data['Bot'],bot_config.data['key'])
    )


with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        if module_info.name.startswith("_"):
            # 假设模组是以 `_` 开头的，就不去导入
            # 根据 Python 标准，这类模组算是私有函数
            continue
        saya.require(f"modules.{module_info.name}")

app.launch_blocking()
