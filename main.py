#pip install openai

import openai
import requests
from flask import Flask, jsonify, render_template

openai.api_key = 'Your---ChatGPT---API---Key'
OPENAI_API_KEY = 'Your---ChatGPT---API---Key'
DALLE_API_URL = "https://api.openai.com/v1/images/generations"

app = Flask(__name__)

@app.route('/generate_prompt')
def generate_prompt():
    model_engine = 'text-davinci-002'
    prompt = openai.Completion.create(
        engine=model_engine,
        prompt="Create a wallpaper with ",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    ).choices[0].text
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    data = {
        "model": "image-alpha-001",
        "prompt": f"{prompt}",
        "num_images": 1,
        "size": "512x512",
        "response_format": "url",
    }
    response = requests.post(DALLE_API_URL, headers=headers, json=data)
    image_url = response.json()["data"][0]["url"]
    return jsonify({'prompt': prompt, 'image_url': image_url})

@app.route('/generate_wallpaper')
def generate_wallpaper():
    # Generate a prompt
    prompt = generate_prompt()
    
    # Use the OpenAI API to generate the image
    response = openai.Image.create(
        prompt=prompt,
        size="256x256",
        model="image-alpha-001"
    )
    
    # Return the image data as a binary response
    return response(response.body, mimetype='image/jpeg', headers={
        'Content-Disposition': 'attachment;filename=wallpaper.jpg'
    })

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
