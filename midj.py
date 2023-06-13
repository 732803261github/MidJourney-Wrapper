# 导入所需模块
from flask import Flask, render_template, request
import discord
from discord.ext import commands

# 创建 Flask 应用程序和 SocketIO 实例
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# 创建 Discord 机器人
bot = commands.Bot(command_prefix='!')

# 定义路由，处理来自前端页面的请求
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_command')
def handle_command(command):
    # 向 Discord 机器人发送指令
    @bot.event
    async def on_ready():
        channel = bot.get_channel(1234567890) # 替换为您的频道 ID
        await channel.send(command)

    # 监听 Discord 机器人的回复，并将其发送到前端页面
    @bot.event
    async def on_message(message):
        if message.channel.id == 1234567890: # 替换为您的频道 ID
            response = message.content
            emit('response', response)

# 启动应用程序
if __name__ == '__main__':
    socketio.run(app)
