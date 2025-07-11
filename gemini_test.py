import google.generativeai as genai

genai.configure(api_key="AIzaSyDrVVP6LEtLKqrwn5vP5zeMxnouqh4l_pY")

models = genai.list_models()

for m in models:
    print(m.name)
