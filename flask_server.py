import pandas as pd
from flask import Flask, request, redirect
import pickle
import csv

app = Flask(__name__)

def predictors(filename):
    df = pd.read_csv(f'uploads/{filename}')
    keys = list(df.keys())
    values = list(df.to_dict('records')[0].values())
    const_vals = values[keys.index("E3"):]

    metals = ["Mo", "V", "Cr"]
    output = {}

    for metal in metals:
        x_test = [[df["TotalIngotsWeight"][0], df[f"{metal}_Last_EOP"][0], df[f"{metal}_Final_basic"][0],
                  df[f"{metal}_Final"][0]] + const_vals]

        model = pickle.load(open(f'{metal}_model.pkl', 'rb'))
        output[metal] = model.predict(x_test)[0]

    return output

@app.route('/', methods = ['GET', 'POST'])
def page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        file.save(f'./uploads/{file.filename}')

        data = predictors(file.filename)
        print(data)

        url = request.url
        if request.url.find("?") != -1:
            url = url.split("?")[0]

        return redirect(f'{url}?mo={data["Mo"]}&v={data["V"]}&cr={data["Cr"]}')

    return open('page.html', 'r', encoding = 'utf-8').read()

app.run(debug = True)