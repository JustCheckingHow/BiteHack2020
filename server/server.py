from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
import json
from aggregator import Aggregator
from reverse_search import ReverseSearch

CORS(app)

aggregator = Aggregator()
r_search = ReverseSearch()

@app.route('/')
def hello():
    return """<script> 
                function send_ajax(){
                    var xhr = new XMLHttpRequest();
                    xhr.open('GET', 'http://127.0.0.1:5000/search?test=123');
                    xhr.send();
                }
            </script>
            <div onclick='send_ajax()' style='width:100px;height:100px;background-color:red'></div>"""

@app.route('/reverse_search', methods=['GET'])
def reverse_search():
    skills = request.args['skills'].lower()
    required, additional = skills.split("|")
    required = required.split(",")
    additional = additional.split(",")
    print(required, additional)
    limit = None
    try:
        limit = request.args['limit']
        limit = int(limit)
    except:
        limit = None
    return r_search.perform_search(required, additional, 10)

@app.route('/search', methods=['GET'])
def search():
    return aggregator.search_in_db(request.args['text'], int(request.args['limit']))
    
if __name__ == '__main__':
    app.run()
