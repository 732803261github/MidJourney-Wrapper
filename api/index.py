from flask import Flask, request, jsonify, render_template
import openai
import random

# 创建 Flask 实例
app = Flask(__name__)

# 获取 openai 的 API 密钥

dict = ['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']

openai.api_key = random.choices(dict, k=1)[0]


# @app.route('/', methods=['GET', 'POST'])
# def test():
#     if request.method == 'POST':
#         message = {'content':'afadfafffadfadfafadfafffadfadfafadfafffadfadf','index':2}
#         return jsonify(message)
#
#     return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug=True)
