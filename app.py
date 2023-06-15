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


# @app.route('/', methods=['GET', 'POST'])
# def chat():
#     if request.method == 'POST':
#         prompt = request.form['prompt']
#         completion = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         return jsonify(completion.choices[0].message)
#
#     return render_template('index.html')
#
#
# @app.route('/image', methods=['GET', 'POST'])
# def image():
#     if request.method == 'POST':
#         prompt = request.form['prompt']
#         completion = openai.Image.create(
#             prompt=prompt,
#             n=2,
#             size="1024x1024"
#         )
#         return completion['data'][0]['url']
#
#     return render_template('image.html')


@app.route('/', methods=['GET', 'POST'])
def midjourney():
    if request.method == 'POST':
        prompt = request.json['prompt']
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
    # headers = {'authorization': Globals.SALAI_TOKEN}
    # r = requests.get(f'https://discord.com/api/v10/channels/1116666992993259573/messages?limit={10}', headers=headers)
    # jsonn = json.loads(r.text)
    # return jsonn

    jsonn = json.dumps([{"attachments":[{"content_type":"image/png","filename":"april39_Sea_waves_background_image_realistic._89bd8e05-eda9-4d6e-9b77-1ef4293398ca.png","height":2048,"id":"1118549875865427998","proxy_url":"https://media.discordapp.net/attachments/1116666992993259573/1118549875865427998/april39_Sea_waves_background_image_realistic._89bd8e05-eda9-4d6e-9b77-1ef4293398ca.png","size":6730686,"url":"https://cdn.discordapp.com/attachments/1116666992993259573/1118549875865427998/april39_Sea_waves_background_image_realistic._89bd8e05-eda9-4d6e-9b77-1ef4293398ca.png","width":2048}],"author":{"avatar":"f6ce562a6b4979c4b1cbc5b436d3be76","avatar_decoration":None,"bot":True,"discriminator":"9282","global_name":None,"id":"936929561302675456","public_flags":589824,"username":"Midjourney Bot"},"channel_id":"1116666992993259573","components":[{"components":[{"custom_id":"MJ::JOB::upsample::1::89bd8e05-eda9-4d6e-9b77-1ef4293398ca","label":"U1","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::2::89bd8e05-eda9-4d6e-9b77-1ef4293398ca","label":"U2","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::3::89bd8e05-eda9-4d6e-9b77-1ef4293398ca","label":"U3","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::4::89bd8e05-eda9-4d6e-9b77-1ef4293398ca","label":"U4","style":2,"type":2},{"custom_id":"MJ::JOB::reroll::0::89bd8e05-eda9-4d6e-9b77-1ef4293398ca::SOLO","emoji":{"name":"🔄"},"style":2,"type":2}],"type":1},{"components":[{"custom_id":"MJ::JOB::variation::1::89bd8e05-eda9-4d6e-9b77-1ef4293398ca","label":"V1","style":2,"type":2},{"custom_id":"MJ::JOB::variation::2::89bd8e05-eda9-4d6e-9b77-1ef4293398ca","label":"V2","style":2,"type":2},{"custom_id":"MJ::JOB::variation::3::89bd8e05-eda9-4d6e-9b77-1ef4293398ca","label":"V3","style":2,"type":2},{"custom_id":"MJ::JOB::variation::4::89bd8e05-eda9-4d6e-9b77-1ef4293398ca","label":"V4","style":2,"type":2}],"type":1}],"content":"**Sea, waves, background image, realistic.** - <@1013250593877397634> (relaxed)","edited_timestamp":None,"embeds":[],"flags":0,"id":"1118549876049973350","mention_everyone":False,"mention_roles":[],"mentions":[{"accent_color":None,"avatar":None,"avatar_decoration":None,"banner":None,"banner_color":None,"discriminator":"7106","display_name":"Esun","flags":0,"global_name":"Esun","id":"1013250593877397634","public_flags":0,"username":"april39"}],"pinned":False,"timestamp":"2023-06-14T14:37:52.102000+00:00","tts":False,"type":0},{"attachments":[{"content_type":"image/png","filename":"april39_Little_tiger_is_eating_an_apple._d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2.png","height":2048,"id":"1118549561984700456","proxy_url":"https://media.discordapp.net/attachments/1116666992993259573/1118549561984700456/april39_Little_tiger_is_eating_an_apple._d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2.png","size":4620892,"url":"https://cdn.discordapp.com/attachments/1116666992993259573/1118549561984700456/april39_Little_tiger_is_eating_an_apple._d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2.png","width":2048}],"author":{"avatar":"f6ce562a6b4979c4b1cbc5b436d3be76","avatar_decoration":None,"bot":True,"discriminator":"9282","global_name":None,"id":"936929561302675456","public_flags":589824,"username":"Midjourney Bot"},"channel_id":"1116666992993259573","components":[{"components":[{"custom_id":"MJ::JOB::upsample::1::d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2","label":"U1","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::2::d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2","label":"U2","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::3::d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2","label":"U3","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::4::d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2","label":"U4","style":2,"type":2},{"custom_id":"MJ::JOB::reroll::0::d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2::SOLO","emoji":{"name":"🔄"},"style":2,"type":2}],"type":1},{"components":[{"custom_id":"MJ::JOB::variation::1::d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2","label":"V1","style":2,"type":2},{"custom_id":"MJ::JOB::variation::2::d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2","label":"V2","style":2,"type":2},{"custom_id":"MJ::JOB::variation::3::d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2","label":"V3","style":2,"type":2},{"custom_id":"MJ::JOB::variation::4::d5f6f7e8-8d90-4dff-acfb-bf6ecac51ab2","label":"V4","style":2,"type":2}],"type":1}],"content":"**Little tiger is eating an apple.** - <@1013250593877397634> (relaxed)","edited_timestamp":None,"embeds":[],"flags":0,"id":"1118549562475413604","mention_everyone":False,"mention_roles":[],"mentions":[{"accent_color":None,"avatar":None,"avatar_decoration":None,"banner":None,"banner_color":None,"discriminator":"7106","display_name":"Esun","flags":0,"global_name":"Esun","id":"1013250593877397634","public_flags":0,"username":"april39"}],"pinned":False,"timestamp":"2023-06-14T14:36:37.340000+00:00","tts":False,"type":0},{"attachments":[{"content_type":"image/png","filename":"april39_Little_Tiger_f7840a41-ca54-4040-a8bc-e82be0438b76.png","height":2048,"id":"1118549150464757891","proxy_url":"https://media.discordapp.net/attachments/1116666992993259573/1118549150464757891/april39_Little_Tiger_f7840a41-ca54-4040-a8bc-e82be0438b76.png","size":6014142,"url":"https://cdn.discordapp.com/attachments/1116666992993259573/1118549150464757891/april39_Little_Tiger_f7840a41-ca54-4040-a8bc-e82be0438b76.png","width":2048}],"author":{"avatar":"f6ce562a6b4979c4b1cbc5b436d3be76","avatar_decoration":None,"bot":True,"discriminator":"9282","global_name":None,"id":"936929561302675456","public_flags":589824,"username":"Midjourney Bot"},"channel_id":"1116666992993259573","components":[{"components":[{"custom_id":"MJ::JOB::upsample::1::f7840a41-ca54-4040-a8bc-e82be0438b76","label":"U1","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::2::f7840a41-ca54-4040-a8bc-e82be0438b76","label":"U2","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::3::f7840a41-ca54-4040-a8bc-e82be0438b76","label":"U3","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::4::f7840a41-ca54-4040-a8bc-e82be0438b76","label":"U4","style":2,"type":2},{"custom_id":"MJ::JOB::reroll::0::f7840a41-ca54-4040-a8bc-e82be0438b76::SOLO","emoji":{"name":"🔄"},"style":2,"type":2}],"type":1},{"components":[{"custom_id":"MJ::JOB::variation::1::f7840a41-ca54-4040-a8bc-e82be0438b76","label":"V1","style":2,"type":2},{"custom_id":"MJ::JOB::variation::2::f7840a41-ca54-4040-a8bc-e82be0438b76","label":"V2","style":2,"type":2},{"custom_id":"MJ::JOB::variation::3::f7840a41-ca54-4040-a8bc-e82be0438b76","label":"V3","style":2,"type":2},{"custom_id":"MJ::JOB::variation::4::f7840a41-ca54-4040-a8bc-e82be0438b76","label":"V4","style":2,"type":2}],"type":1}],"content":"**Little Tiger** - <@1013250593877397634> (relaxed)","edited_timestamp":None,"embeds":[],"flags":0,"id":"1118549151068717056","mention_everyone":False,"mention_roles":[],"mentions":[{"accent_color":None,"avatar":None,"avatar_decoration":None,"banner":None,"banner_color":None,"discriminator":"7106","display_name":"Esun","flags":0,"global_name":"Esun","id":"1013250593877397634","public_flags":0,"username":"april39"}],"pinned":False,"timestamp":"2023-06-14T14:34:59.253000+00:00","tts":False,"type":0},{"attachments":[{"content_type":"image/png","filename":"april39_Azure_skies_and_misty_rains_yet_I_am_waiting_for_you._c334d7e3-79e9-429c-85d2-137fc8ddc7af.png","height":2048,"id":"1118539021547753482","proxy_url":"https://media.discordapp.net/attachments/1116666992993259573/1118539021547753482/april39_Azure_skies_and_misty_rains_yet_I_am_waiting_for_you._c334d7e3-79e9-429c-85d2-137fc8ddc7af.png","size":4801301,"url":"https://cdn.discordapp.com/attachments/1116666992993259573/1118539021547753482/april39_Azure_skies_and_misty_rains_yet_I_am_waiting_for_you._c334d7e3-79e9-429c-85d2-137fc8ddc7af.png","width":2048}],"author":{"avatar":"f6ce562a6b4979c4b1cbc5b436d3be76","avatar_decoration":None,"bot":True,"discriminator":"9282","global_name":None,"id":"936929561302675456","public_flags":589824,"username":"Midjourney Bot"},"channel_id":"1116666992993259573","components":[{"components":[{"custom_id":"MJ::JOB::upsample::1::c334d7e3-79e9-429c-85d2-137fc8ddc7af","label":"U1","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::2::c334d7e3-79e9-429c-85d2-137fc8ddc7af","label":"U2","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::3::c334d7e3-79e9-429c-85d2-137fc8ddc7af","label":"U3","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::4::c334d7e3-79e9-429c-85d2-137fc8ddc7af","label":"U4","style":2,"type":2},{"custom_id":"MJ::JOB::reroll::0::c334d7e3-79e9-429c-85d2-137fc8ddc7af::SOLO","emoji":{"name":"🔄"},"style":2,"type":2}],"type":1},{"components":[{"custom_id":"MJ::JOB::variation::1::c334d7e3-79e9-429c-85d2-137fc8ddc7af","label":"V1","style":2,"type":2},{"custom_id":"MJ::JOB::variation::2::c334d7e3-79e9-429c-85d2-137fc8ddc7af","label":"V2","style":2,"type":2},{"custom_id":"MJ::JOB::variation::3::c334d7e3-79e9-429c-85d2-137fc8ddc7af","label":"V3","style":2,"type":2},{"custom_id":"MJ::JOB::variation::4::c334d7e3-79e9-429c-85d2-137fc8ddc7af","label":"V4","style":2,"type":2}],"type":1}],"content":"**Azure skies and misty rains, yet I am waiting for you.** - <@1013250593877397634> (relaxed)","edited_timestamp":None,"embeds":[],"flags":0,"id":"1118539021862322249","mention_everyone":False,"mention_roles":[],"mentions":[{"accent_color":None,"avatar":None,"avatar_decoration":None,"banner":None,"banner_color":None,"discriminator":"7106","display_name":"Esun","flags":0,"global_name":"Esun","id":"1013250593877397634","public_flags":0,"username":"april39"}],"pinned":False,"timestamp":"2023-06-14T13:54:44.262000+00:00","tts":False,"type":0},{"attachments":[{"content_type":"image/webp","filename":"april39_Coca-Cola._715f250c-6ccb-4419-8e16-1b98b4e5e12b.webp","height":2048,"id":"1118520773976530974","proxy_url":"https://media.discordapp.net/attachments/1116666992993259573/1118520773976530974/april39_Coca-Cola._715f250c-6ccb-4419-8e16-1b98b4e5e12b.webp","size":2058032,"url":"https://cdn.discordapp.com/attachments/1116666992993259573/1118520773976530974/april39_Coca-Cola._715f250c-6ccb-4419-8e16-1b98b4e5e12b.webp","width":2048}],"author":{"avatar":"f6ce562a6b4979c4b1cbc5b436d3be76","avatar_decoration":None,"bot":True,"discriminator":"9282","global_name":None,"id":"936929561302675456","public_flags":589824,"username":"Midjourney Bot"},"channel_id":"1116666992993259573","components":[{"components":[{"custom_id":"MJ::JOB::upsample::1::715f250c-6ccb-4419-8e16-1b98b4e5e12b","label":"U1","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::2::715f250c-6ccb-4419-8e16-1b98b4e5e12b","label":"U2","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::3::715f250c-6ccb-4419-8e16-1b98b4e5e12b","label":"U3","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::4::715f250c-6ccb-4419-8e16-1b98b4e5e12b","label":"U4","style":2,"type":2},{"custom_id":"MJ::JOB::reroll::0::715f250c-6ccb-4419-8e16-1b98b4e5e12b::SOLO","emoji":{"name":"🔄"},"style":2,"type":2}],"type":1},{"components":[{"custom_id":"MJ::JOB::variation::1::715f250c-6ccb-4419-8e16-1b98b4e5e12b","label":"V1","style":2,"type":2},{"custom_id":"MJ::JOB::variation::2::715f250c-6ccb-4419-8e16-1b98b4e5e12b","label":"V2","style":2,"type":2},{"custom_id":"MJ::JOB::variation::3::715f250c-6ccb-4419-8e16-1b98b4e5e12b","label":"V3","style":2,"type":2},{"custom_id":"MJ::JOB::variation::4::715f250c-6ccb-4419-8e16-1b98b4e5e12b","label":"V4","style":2,"type":2}],"type":1}],"content":"**Coca-Cola. --s 750 --niji 5** - <@1013250593877397634> (Open on website for full quality) (relaxed)","edited_timestamp":None,"embeds":[],"flags":0,"id":"1118520774299488306","mention_everyone":False,"mention_roles":[],"mentions":[{"accent_color":None,"avatar":None,"avatar_decoration":None,"banner":None,"banner_color":None,"discriminator":"7106","display_name":"Esun","flags":0,"global_name":"Esun","id":"1013250593877397634","public_flags":0,"username":"april39"}],"pinned":False,"timestamp":"2023-06-14T12:42:13.704000+00:00","tts":False,"type":0},{"attachments":[{"content_type":"image/png","filename":"april39_Eat_hamburgers_drink_cola_be_realistic._f905e3b8-1136-4977-bd32-d947000e147f.png","height":2048,"id":"1118517355681677452","proxy_url":"https://media.discordapp.net/attachments/1116666992993259573/1118517355681677452/april39_Eat_hamburgers_drink_cola_be_realistic._f905e3b8-1136-4977-bd32-d947000e147f.png","size":7430361,"url":"https://cdn.discordapp.com/attachments/1116666992993259573/1118517355681677452/april39_Eat_hamburgers_drink_cola_be_realistic._f905e3b8-1136-4977-bd32-d947000e147f.png","width":2048}],"author":{"avatar":"f6ce562a6b4979c4b1cbc5b436d3be76","avatar_decoration":None,"bot":True,"discriminator":"9282","global_name":None,"id":"936929561302675456","public_flags":589824,"username":"Midjourney Bot"},"channel_id":"1116666992993259573","components":[{"components":[{"custom_id":"MJ::JOB::upsample::1::f905e3b8-1136-4977-bd32-d947000e147f","label":"U1","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::2::f905e3b8-1136-4977-bd32-d947000e147f","label":"U2","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::3::f905e3b8-1136-4977-bd32-d947000e147f","label":"U3","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::4::f905e3b8-1136-4977-bd32-d947000e147f","label":"U4","style":2,"type":2},{"custom_id":"MJ::JOB::reroll::0::f905e3b8-1136-4977-bd32-d947000e147f::SOLO","emoji":{"name":"🔄"},"style":2,"type":2}],"type":1},{"components":[{"custom_id":"MJ::JOB::variation::1::f905e3b8-1136-4977-bd32-d947000e147f","label":"V1","style":2,"type":2},{"custom_id":"MJ::JOB::variation::2::f905e3b8-1136-4977-bd32-d947000e147f","label":"V2","style":2,"type":2},{"custom_id":"MJ::JOB::variation::3::f905e3b8-1136-4977-bd32-d947000e147f","label":"V3","style":2,"type":2},{"custom_id":"MJ::JOB::variation::4::f905e3b8-1136-4977-bd32-d947000e147f","label":"V4","style":2,"type":2}],"type":1}],"content":"**Eat hamburgers, drink cola, be realistic. --s 750 --niji 5** - <@1013250593877397634> (relaxed)","edited_timestamp":None,"embeds":[],"flags":0,"id":"1118517356306649088","mention_everyone":False,"mention_roles":[],"mentions":[{"accent_color":None,"avatar":None,"avatar_decoration":None,"banner":None,"banner_color":None,"discriminator":"7106","display_name":"Esun","flags":0,"global_name":"Esun","id":"1013250593877397634","public_flags":0,"username":"april39"}],"pinned":False,"timestamp":"2023-06-14T12:28:38.791000+00:00","tts":False,"type":0},{"attachments":[{"content_type":"image/webp","filename":"april39_Translation_English_output_only._cd439a52-f122-427a-8ca5-7f8a611b4919.webp","height":2048,"id":"1118500494277627965","proxy_url":"https://media.discordapp.net/attachments/1116666992993259573/1118500494277627965/april39_Translation_English_output_only._cd439a52-f122-427a-8ca5-7f8a611b4919.webp","size":1997226,"url":"https://cdn.discordapp.com/attachments/1116666992993259573/1118500494277627965/april39_Translation_English_output_only._cd439a52-f122-427a-8ca5-7f8a611b4919.webp","width":2048}],"author":{"avatar":"f6ce562a6b4979c4b1cbc5b436d3be76","avatar_decoration":None,"bot":True,"discriminator":"9282","global_name":None,"id":"936929561302675456","public_flags":589824,"username":"Midjourney Bot"},"channel_id":"1116666992993259573","components":[{"components":[{"custom_id":"MJ::JOB::upsample::1::cd439a52-f122-427a-8ca5-7f8a611b4919","label":"U1","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::2::cd439a52-f122-427a-8ca5-7f8a611b4919","label":"U2","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::3::cd439a52-f122-427a-8ca5-7f8a611b4919","label":"U3","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::4::cd439a52-f122-427a-8ca5-7f8a611b4919","label":"U4","style":2,"type":2},{"custom_id":"MJ::JOB::reroll::0::cd439a52-f122-427a-8ca5-7f8a611b4919::SOLO","emoji":{"name":"🔄"},"style":2,"type":2}],"type":1},{"components":[{"custom_id":"MJ::JOB::variation::1::cd439a52-f122-427a-8ca5-7f8a611b4919","label":"V1","style":2,"type":2},{"custom_id":"MJ::JOB::variation::2::cd439a52-f122-427a-8ca5-7f8a611b4919","label":"V2","style":2,"type":2},{"custom_id":"MJ::JOB::variation::3::cd439a52-f122-427a-8ca5-7f8a611b4919","label":"V3","style":2,"type":2},{"custom_id":"MJ::JOB::variation::4::cd439a52-f122-427a-8ca5-7f8a611b4919","label":"V4","style":2,"type":2}],"type":1}],"content":"**Translation, English output only. --s 750 --niji 5** - <@1013250593877397634> (Open on website for full quality) (relaxed)","edited_timestamp":None,"embeds":[],"flags":0,"id":"1118500494692851793","mention_everyone":False,"mention_roles":[],"mentions":[{"accent_color":None,"avatar":None,"avatar_decoration":None,"banner":None,"banner_color":None,"discriminator":"7106","display_name":"Esun","flags":0,"global_name":"Esun","id":"1013250593877397634","public_flags":0,"username":"april39"}],"pinned":False,"timestamp":"2023-06-14T11:21:38.669000+00:00","tts":False,"type":0},{"attachments":[{"content_type":"image/png","filename":"april39_Translation_only_English_output_is_required._9c731dfe-5d3c-452f-a898-ebb127ff1ce7.png","height":2048,"id":"1118499788762136656","proxy_url":"https://media.discordapp.net/attachments/1116666992993259573/1118499788762136656/april39_Translation_only_English_output_is_required._9c731dfe-5d3c-452f-a898-ebb127ff1ce7.png","size":7368891,"url":"https://cdn.discordapp.com/attachments/1116666992993259573/1118499788762136656/april39_Translation_only_English_output_is_required._9c731dfe-5d3c-452f-a898-ebb127ff1ce7.png","width":2048}],"author":{"avatar":"f6ce562a6b4979c4b1cbc5b436d3be76","avatar_decoration":None,"bot":True,"discriminator":"9282","global_name":None,"id":"936929561302675456","public_flags":589824,"username":"Midjourney Bot"},"channel_id":"1116666992993259573","components":[{"components":[{"custom_id":"MJ::JOB::upsample::1::9c731dfe-5d3c-452f-a898-ebb127ff1ce7","label":"U1","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::2::9c731dfe-5d3c-452f-a898-ebb127ff1ce7","label":"U2","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::3::9c731dfe-5d3c-452f-a898-ebb127ff1ce7","label":"U3","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::4::9c731dfe-5d3c-452f-a898-ebb127ff1ce7","label":"U4","style":2,"type":2},{"custom_id":"MJ::JOB::reroll::0::9c731dfe-5d3c-452f-a898-ebb127ff1ce7::SOLO","emoji":{"name":"🔄"},"style":2,"type":2}],"type":1},{"components":[{"custom_id":"MJ::JOB::variation::1::9c731dfe-5d3c-452f-a898-ebb127ff1ce7","label":"V1","style":2,"type":2},{"custom_id":"MJ::JOB::variation::2::9c731dfe-5d3c-452f-a898-ebb127ff1ce7","label":"V2","style":2,"type":2},{"custom_id":"MJ::JOB::variation::3::9c731dfe-5d3c-452f-a898-ebb127ff1ce7","label":"V3","style":2,"type":2},{"custom_id":"MJ::JOB::variation::4::9c731dfe-5d3c-452f-a898-ebb127ff1ce7","label":"V4","style":2,"type":2}],"type":1}],"content":"**Translation, only English output is required. --s 750 --niji 5** - <@1013250593877397634> (relaxed)","edited_timestamp":None,"embeds":[],"flags":0,"id":"1118499789257048158","mention_everyone":False,"mention_roles":[],"mentions":[{"accent_color":None,"avatar":None,"avatar_decoration":None,"banner":None,"banner_color":None,"discriminator":"7106","display_name":"Esun","flags":0,"global_name":"Esun","id":"1013250593877397634","public_flags":0,"username":"april39"}],"pinned":False,"timestamp":"2023-06-14T11:18:50.480000+00:00","tts":False,"type":0},{"attachments":[{"content_type":"image/png","filename":"april39_Translation_output_in_English_only_4e3799ef-507c-4d4c-a019-40a5c5764f2b.png","height":2048,"id":"1118499763566956664","proxy_url":"https://media.discordapp.net/attachments/1116666992993259573/1118499763566956664/april39_Translation_output_in_English_only_4e3799ef-507c-4d4c-a019-40a5c5764f2b.png","size":6679239,"url":"https://cdn.discordapp.com/attachments/1116666992993259573/1118499763566956664/april39_Translation_output_in_English_only_4e3799ef-507c-4d4c-a019-40a5c5764f2b.png","width":2048}],"author":{"avatar":"f6ce562a6b4979c4b1cbc5b436d3be76","avatar_decoration":None,"bot":True,"discriminator":"9282","global_name":None,"id":"936929561302675456","public_flags":589824,"username":"Midjourney Bot"},"channel_id":"1116666992993259573","components":[{"components":[{"custom_id":"MJ::JOB::upsample::1::4e3799ef-507c-4d4c-a019-40a5c5764f2b","label":"U1","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::2::4e3799ef-507c-4d4c-a019-40a5c5764f2b","label":"U2","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::3::4e3799ef-507c-4d4c-a019-40a5c5764f2b","label":"U3","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::4::4e3799ef-507c-4d4c-a019-40a5c5764f2b","label":"U4","style":2,"type":2},{"custom_id":"MJ::JOB::reroll::0::4e3799ef-507c-4d4c-a019-40a5c5764f2b::SOLO","emoji":{"name":"🔄"},"style":2,"type":2}],"type":1},{"components":[{"custom_id":"MJ::JOB::variation::1::4e3799ef-507c-4d4c-a019-40a5c5764f2b","label":"V1","style":2,"type":2},{"custom_id":"MJ::JOB::variation::2::4e3799ef-507c-4d4c-a019-40a5c5764f2b","label":"V2","style":2,"type":2},{"custom_id":"MJ::JOB::variation::3::4e3799ef-507c-4d4c-a019-40a5c5764f2b","label":"V3","style":2,"type":2},{"custom_id":"MJ::JOB::variation::4::4e3799ef-507c-4d4c-a019-40a5c5764f2b","label":"V4","style":2,"type":2}],"type":1}],"content":"**Translation, output in English only --s 750 --niji 5** - <@1013250593877397634> (relaxed)","edited_timestamp":None,"embeds":[],"flags":0,"id":"1118499764565196820","mention_everyone":False,"mention_roles":[],"mentions":[{"accent_color":None,"avatar":None,"avatar_decoration":None,"banner":None,"banner_color":None,"discriminator":"7106","display_name":"Esun","flags":0,"global_name":"Esun","id":"1013250593877397634","public_flags":0,"username":"april39"}],"pinned":False,"timestamp":"2023-06-14T11:18:44.593000+00:00","tts":False,"type":0},{"attachments":[{"content_type":"image/png","filename":"april39_Delicious_barbecue._cc1b4f91-56c7-45c9-a202-dba08dd45524.png","height":2048,"id":"1118493419023638568","proxy_url":"https://media.discordapp.net/attachments/1116666992993259573/1118493419023638568/april39_Delicious_barbecue._cc1b4f91-56c7-45c9-a202-dba08dd45524.png","size":7489706,"url":"https://cdn.discordapp.com/attachments/1116666992993259573/1118493419023638568/april39_Delicious_barbecue._cc1b4f91-56c7-45c9-a202-dba08dd45524.png","width":2048}],"author":{"avatar":"f6ce562a6b4979c4b1cbc5b436d3be76","avatar_decoration":None,"bot":True,"discriminator":"9282","global_name":None,"id":"936929561302675456","public_flags":589824,"username":"Midjourney Bot"},"channel_id":"1116666992993259573","components":[{"components":[{"custom_id":"MJ::JOB::upsample::1::cc1b4f91-56c7-45c9-a202-dba08dd45524","label":"U1","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::2::cc1b4f91-56c7-45c9-a202-dba08dd45524","label":"U2","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::3::cc1b4f91-56c7-45c9-a202-dba08dd45524","label":"U3","style":2,"type":2},{"custom_id":"MJ::JOB::upsample::4::cc1b4f91-56c7-45c9-a202-dba08dd45524","label":"U4","style":2,"type":2},{"custom_id":"MJ::JOB::reroll::0::cc1b4f91-56c7-45c9-a202-dba08dd45524::SOLO","emoji":{"name":"🔄"},"style":2,"type":2}],"type":1},{"components":[{"custom_id":"MJ::JOB::variation::1::cc1b4f91-56c7-45c9-a202-dba08dd45524","label":"V1","style":2,"type":2},{"custom_id":"MJ::JOB::variation::2::cc1b4f91-56c7-45c9-a202-dba08dd45524","label":"V2","style":2,"type":2},{"custom_id":"MJ::JOB::variation::3::cc1b4f91-56c7-45c9-a202-dba08dd45524","label":"V3","style":2,"type":2},{"custom_id":"MJ::JOB::variation::4::cc1b4f91-56c7-45c9-a202-dba08dd45524","label":"V4","style":2,"type":2}],"type":1}],"content":"**Delicious barbecue. --s 750 --niji 5** - <@1013250593877397634> (relaxed)","edited_timestamp":None,"embeds":[],"flags":0,"id":"1118493419493404713","mention_everyone":False,"mention_roles":[],"mentions":[{"accent_color":None,"avatar":None,"avatar_decoration":None,"banner":None,"banner_color":None,"discriminator":"7106","display_name":"Esun","flags":0,"global_name":"Esun","id":"1013250593877397634","public_flags":0,"username":"april39"}],"pinned":False,"timestamp":"2023-06-14T10:53:31.810000+00:00","tts":False,"type":0}])
    arr = json.loads(jsonn)
    return arr


@app.route('/collect', methods=['GET', 'POST'])
def collecting_results():
    type = 'txt'
    message_list = retrieve_messages()
    for message in message_list:
        if (message['author']['username'] == 'Midjourney Bot') and ('**' in message['content']):
            if len(message['attachments']) > 0:
                # 已完成列表
                if (message['attachments'][0]['filename'][-4:] == '.png') or (
                        '(Open on website for full quality)' in message['content']):
                    if(message['attachments'][0]['filename'][-4:] == '.png'):
                        type = 'img'
                    if('(Open on website for full quality)' in message['content']):
                        type = 'web'
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
                    json = {type: url}
                    return json
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
                    return {type: status}

            else:
                id = message['id']
                task_id = re.findall("<@\d+>", message['content'])[0].replace("<@", "").replace(">", "")
                prompt = message['content'].split('**')[1].split('--')[0].strip()
                status = 'unknown status'
                if '(Waiting to start)' in message['content']:
                    status = 'Waiting to start'
                return {type: status}


if __name__ == '__main__':
    # 启动 Discord bot
    app.run(host='0.0.0.0', port=8080)  # 启动 Flask App
