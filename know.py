from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from openai import OpenAI
import os

# 在应用初始化之前加载 .env 文件中的环境变量
load_dotenv()

app = Flask(__name__)

# 现在 os.environ.get() 会读取到 .env 文件中的变量（如果存在的话）
api_key = os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("OPENAI_BASE_URL")

# 从环境变量或直接设置你的 OpenAI API 密钥
# 强烈建议使用环境变量来保护你的密钥
client = OpenAI(
    # api_key="AIzaSyDUyX8Yt9w6Wgj2ypWCQ5lZZ9oWTV-TU9w",
    # base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    
    # api_key = 'sk-xeszeaoulryacxysouxcbnfmliuilaluwlevyoywtxyrxqor',
    # base_url="https://api.siliconflow.cn/v1",
    # base_url = "https://api.openai.com/v1",
    # api_key='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',
    api_key = api_key,
    base_url = base_url
)

@app.route('/chat', methods=['POST'])
def chat():
    if not request.json or 'message' not in request.json:
        return jsonify({ 'error': 'Invalid request' }), 400

    user_message = request.json['message']


    try:
       
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {"role": "system", "content": "你是一个有帮助的助手。"},
                {"role": "user", "content": user_message}
            ]
        )

        # 提取助手的回复
        assistant_reply = response.choices[0].message.content

        # 返回 JSON 格式的回复给前端
        return jsonify({ 'response': assistant_reply })

    except Exception as e:
        print(f"调用 OpenAI API 失败: {e}")
        return jsonify({ 'response': f'获取回复时发生错误: {e}' }), 500

@app.route('/')
def index():
    try:
        return send_file('test.html')
    except FileNotFoundError:
        return "test.html not found", 404

if __name__ == '__main__':
    # 在开发模式下运行 Flask 应用
    # debug=True 会在代码修改时自动重启服务器
    app.run(debug=True,port=5001)
