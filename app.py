from flask import *
import pandas as pd
import network

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_network')
def get_network():
    return "未実装"


@app.route('/get_networks_d3', methods=["POST"])
def get_networks_d3():
    file = request.files["file"]
    input_book = pd.ExcelFile(file)

    networks = {}
    for sheet in input_book.sheet_names:
        networks[sheet] = network.get_network_d3(input_book, sheet)

    return networks


@app.route('/get_saidai_renketsu', methods=["POST"])
def get_saidai_renketsu():
    data = request.form["data"]
    return network.get_saidai_renketsu(data)


@app.route('/test')
def test():
    df = pd.read_csv("category-brands.csv")
    j = df.to_json()
    return j


if __name__ == '__main__':
    app.run(debug=True)
