'''
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
  return "Hello, World!"
Hello.World!を表示する簡易プログラムです
'''
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

@app.route("/search")
def search():
    query = request.args.get("query")
    searchengine = request.args.get("engine", "bing")  # デフォルトはbing
    if searchengine.lower() == "bing":
        url = f"https://www.bing.com/search?q={query}"
    else:
        return jsonify({"error": "Unsupported search engine. Only 'bing' is supported."}), 400

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raiseforstatus()  # HTTPリクエストが成功したか確認
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = [anchor['href'] for anchor in soup.find_all('a', href=True)]
        if search_results:
            return jsonify({"random_url": random.choice(search_results)})
        else:
            return jsonify({"message": "No search results found."}), 404
    except requests.RequestException as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

