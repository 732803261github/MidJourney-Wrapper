import Globals
from flask import Flask, request, jsonify, render_template
import openai
import random
from discord.ext import commands
import requests
import json
import re

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
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": '翻译，只需输出英文即可 %s' % prompt}
            ]
        )
        prompt = completion.choices[0].message.content
        headers = {
            'authorization': Globals.SALAI_TOKEN
        }
        payload = {
            "type": 2,
            "application_id": "936929561302675456",
            "guild_id": "1116666992238276620",
            "channel_id": "1116666992993259573",
            "session_id": "8fd1e6029a5d0604113dae462e6b9f57",
            "data": {
                "version": "1077969938624553050",
                "id": "938956540159881230",
                "name": 'imagine',
                "type": 1,
                "options": [
                    {
                        "type": 3,
                        "name": "prompt",
                        "value": prompt
                    }
                ],
                "attachments": []
            },
        }
        payload2 = {
            "type": 2,
            "application_id": "1116670202210435092",
            "guild_id": "1116666992238276620",
            "channel_id": "1116666992993259573",
            "session_id": "8fd1e6029a5d0604113dae462e6b9f57",
            "data": {
                "version": "1116938194840191064",
                "id": "1116938194840191058",
                "name": "mj_imagine",
                "type": 1,
                "options": [
                    {
                        "type": 3,
                        "name": "prompt",
                        "value": prompt
                    }
                ],
                "attachments": []
            },
        }
        # 发送消息内容
        # payload = {'content': prompt}
        # 发送 POST 请求
        response = requests.post('https://discord.com/api/v9/interactions', json=payload, headers=headers)
        # 打印响应状态码和响应内容
        return response.content

    return render_template('midjourney.html')


@app.route('/midjson', methods=['GET', 'POST'])
def retrieve_messages():
    headers = {'authorization': Globals.SALAI_TOKEN}
    r = requests.get(f'https://discord.com/api/v10/channels/1116666992993259573/messages?limit={10}', headers=headers)
    jsonn = json.loads(r.text)
    return jsonn


@app.route('/collect', methods=['GET', 'POST'])
def collecting_results():
    message_list = retrieve_messages()
    for message in message_list:
        if (message['author']['username'] == 'Midjourney Bot') and ('**' in message['content']) and (
                'image/png' in message['attachments'][0]['content_type']):
            if len(message['attachments']) > 0:
                # 已完成列表
                if (message['attachments'][0]['filename'][-4:] == '.png') or (
                        '(Open on website for full quality)' in message['content']):
                    id = message['id']
                    task_id = re.findall("<@\d+>", message['content'])[0].replace("<@", "").replace(">", "")
                    prompt = message['content'].split('**')[1].split('--')[0].strip()
                    # 如果 prompt 中含有链接，则需要把链接删除掉
                    pic_url_list = re.findall(
                        r'<http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+>', prompt)
                    if len(pic_url_list) > 0:
                        for pic_url in pic_url_list:
                            prompt = prompt.replace(pic_url, "").strip()
                    else:
                        pass
                    url = message['attachments'][0]['url']
                    filename = message['attachments'][0]['filename']
                    print(url)
                    print(filename)
                    return url
                # 进行中列表
                else:
                    id = message['id']
                    task_id = re.findall("<@\d+>", message['content'])[0].replace("<@", "").replace(">", "")
                    prompt = message['content'].split('**')[1].split('--')[0].strip()
                    status = 'unknown status'
                    if ('(fast)' in message['content']) or ('(relaxed)' in message['content']):
                        try:
                            status = re.findall("(\w*%)", message['content'])[0]
                        except:
                            status = 'unknown status'
                    return status

            else:
                id = message['id']
                task_id = re.findall("<@\d+>", message['content'])[0].replace("<@", "").replace(">", "")
                prompt = message['content'].split('**')[1].split('--')[0].strip()
                status = 'unknown status'
                if '(Waiting to start)' in message['content']:
                    status = 'Waiting to start'
                return status


if __name__ == '__main__':
    # 启动 Discord bot
    app.run(host='0.0.0.0', port=8088)  # 启动 Flask App
