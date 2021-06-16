import app as app
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, request, Response, send_file
from matplotlib.pyplot import pie, axis
import io
import random
import numpy as np
from pandas.core.common import random_state
from sklearn.model_selection import train_test_split
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import plotly.express as px

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# Basic everything of the function page
@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')


@app.route('/pyl', methods=['GET', 'POST'])
def pyl():
    return render_template('pyl.html')


# Html view for import csv files
@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file = request.form.get('csvfile')
        data1 = pd.read_csv(file)
    return render_template('data.html', data=data1.to_html())


# All the values after csv processing
@app.route('/mean', methods=['GET', 'POST'])
def mean():
    if request.method == 'POST':
        file = request.form.get('csvfile')
        df = pd.read_csv(file)
        targetcol = request.form.get('targetcol')
        mean1 = df[targetcol].mean()
        sum1 = df[targetcol].sum()
        max1 = df[targetcol].max()
        min1 = df[targetcol].min()
        count1 = df[targetcol].count()
        median1 = df[targetcol].median()
        std1 = df[targetcol].std()
        var1 = df[targetcol].var()

        ShowData = {
            "Mean:": str(mean1),
            "Sum:": str(sum1),
            "Max:": str(max1),
            "Min:": str(min1),
            "Count:": str(count1),
            "Median:": str(median1),
            "Std:": str(std1),
            "Var:": str(var1)
        }

        return render_template('ShowData.html', data=ShowData)


@app.route('/piechart', methods=['GET', 'POST'])
def piechart():
    if request.method == 'POST':
        file = request.form.get('csvfile')
        f = pd.read_csv(file)
        # sums = f.groupby(f["Product Name;"])["Number Of Bugs"].sum()
        # axis('equal')
        # pie(sums, labels=sums.index)
        # plt.show()
        # fig = px.line(f, x='Date;', y='Number Of Bugs', title='Here is the line chart for result')
        # fig.show()
        fig1 = px.data.tips()
        fig1 = px.pie(f, values='Number Of Bugs', names='Date;')
        fig1.show()
        # Did not use the showpie.html, external library supports!
        return render_template('test.html', figure=fig1)


# Download file from the Html(Sample!!!)
@app.route('/download')
def download():
    p = "petty.jpg"
    return send_file(p, as_attachment=True)


# Add new column
@app.route('/Add_col', methods=['GET', 'POST'])
def Add_col():
    if request.method == 'POST':
        file = request.form.get('csvfile')
        data2 = pd.read_csv(file)
        colname = request.form.get('colname', type=str)
        dvalue = request.form.get('dvalue', type=int)
        data2[colname] = dvalue
        data2.to_csv("new_column.csv", index=False)
        file1 = "new_column.csv"
        # as_attachment-True to save file, False to have a web view
        return send_file(file1, mimetype=file, as_attachment=False)


# Split csv file as percentage
@app.route('/split', methods=['GET', 'POST'])
def split():
    if request.method == 'POST':
        file = request.form.get('csvfile')
        train_data = pd.read_csv(file)
        # get user inputs to make the split
        t = request.form.get('pct', type=int)
        split_ratio = t / 100
        xtrain, xtest, ytrain, ytest = train_test_split(train_data, range(train_data.shape[0]), test_size=split_ratio)
        xtest.to_csv("split_file.csv", index=False)
        xtrain.to_csv("Rest.csv", index=False)
        if request.form['submit_button'] == 'Split':
            pass
            s1 = "split_file.csv"
            # as_attachment-True to save file, False to have a web view
            return send_file(s1, mimetype=file, as_attachment=False)
        elif request.form['submit_button'] == 'Rest':
            pass
            s2 = "Rest.csv"
            # as_attachment-True to save file, False to have a web view
        return send_file(s2, mimetype=file, as_attachment=False)


# New idea not finished
@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if request.method == 'POST':
        file = request.form.get('csvfile')
        df = pd.read_csv(file)
        gb = df.groupby('Product Name;')
        return [gb.get_group(x) for x in gb.groups]


# Sort by date
@app.route('/sort', methods=['GET', 'POST'])
def sort():
    if request.method == 'POST':
        file = request.form.get('csvfile')
        d1 = pd.read_csv(file)
        d1.sort_values(by='Date;', ascending=True, inplace=True)
        return render_template('data.html', data=d1.to_html())


if __name__ == '__main__':
    app.run(debug=True)
