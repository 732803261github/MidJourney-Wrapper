import Globals
from flask import Flask, request, jsonify, render_template
import openai
import random
from discord.ext import commands
import requests

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

        headers = {
            'authorization': Globals.SALAI_TOKEN
        }
        payload = {
            "type": 2,
            "application_id": "1116670202210435092",
            "guild_id": "1116666992238276620",
            "channel_id": "1116666992993259573",
            "session_id": "8fd1e6029a5d0604113dae462e6b9f57",
            "data": {
                "version": "1116938194840191063",
                "id": "1116938194840191057",
                "name": "hello",
                "type": 1,
                "options": [
                    {
                        "type": 3,
                        "name": "sentence",
                        "value": int(prompt)
                    }
                ],
                "attachments": []
            },
        }
        # url = 'https://discord.com/api/webhooks/1118400244565160087/LAcZ19qK8Q9RfubXVjUziT2b6GpKaSzBvtuc5JKqswegbq5RXSJCQBCJIv2us1RFLVev'
        url = 'https://discord.com/api/webhooks/1118398227985743872/TgDfOPmetJ3bk_eOD-1uy1rSh3nLLlJcbNL_vVAJeN6pLg6c_HkP_8NMN3UeY7AKwcvQ'
        # 发送消息内容
        # payload = {'content': prompt}
        # 发送 POST 请求
        response = requests.post('https://discord.com/api/v9/interactions', json=payload)
        # 打印响应状态码和响应内容
        return response.content

    return render_template('midjourney.html')


if __name__ == '__main__':
    # 启动 Discord bot
    app.run(host='0.0.0.0', port=8088)  # 启动 Flask App
