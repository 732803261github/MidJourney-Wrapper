import Globals
from flask import Flask, request, jsonify, render_template
import openai
import random
import discord
from discord.ext import commands

# 创建 Flask 实例
app = Flask(__name__)
# 获取 openai 的 API 密钥
dict = [Globals.OPEN_AI_KEY]
openai.api_key = random.choices(dict, k=1)[0]

bot = commands.Bot(command_prefix='/')


@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form['prompt']
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(completion.choices[0].message)
        return jsonify(completion.choices[0].message)

    return render_template('index.html')


@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        prompt = request.form['prompt']
        completion = openai.Image.create(
            prompt=prompt,
            n=2,
            size="1024x1024"
        )
        return completion['data'][0]['url']

    return render_template('image.html')


@app.route('/midjourney', methods=['GET', 'POST'])
def midjourney():
    if request.method == 'POST':
        prompt = request.form['prompt']

        @bot.event
        async def on_ready():
            channel = bot.get_channel(1116666992993259573)
            await channel.send(prompt)

        @bot.event
        async def on_message(message):
            if message.channel.id == 1116666992993259573:
                response = message.content
                return response

    return render_template('midjourney.html')


if __name__ == '__main__':
    # 启动 Discord bot
    app.run(host='0.0.0.0', port=8088)  # 启动 Flask App
