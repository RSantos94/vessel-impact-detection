from flask import Flask
from flask import request
#from flask_restful import Resource, Api
import csv
import json

app = Flask(__name__)
#api = Api(app)

todos = {}

@app.route('/header/', methods=['POST'])
def header():
    print(request.data)
    converted_data = request.data.decode('utf8')  # .replace('"', "'")
    print(converted_data)
    data = json.dumps(converted_data)
    print(json.loads(converted_data))
    json_file = json.loads(converted_data)
    mylist = []
    for key, value in json_file.items():
        print(key, value)
        mylist.append(key)

    with open('data.csv', 'w', newline='', encoding='utf8') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(mylist)

    return "Hello World!"

@app.route('/data/', methods=['GET','POST'])
def data():
    if request.method == "POST":
        print(request.data)
        converted_data = request.data.decode('utf8')#.replace('"', "'")
        print(converted_data)
        data = json.dumps(converted_data)
        print(json.loads(converted_data))
        json_file = json.loads(converted_data)
        mylist = []
        for key, value in json_file.items():
            print(key, value)
            mylist.append(value)

        with open('data.csv', 'a', newline='', encoding='utf8') as csvfile:
            wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            wr.writerow(mylist)
        #f = open('data.csv', 'w', newline='')
        #csv_file = csv.writer(f)
        #for item in json_file:
        #    print(item)
        #    csv_file.writerow(item)
        #f.close()
        return "Hello World!"
    if request.method == "GET":
        print("Boas")
        return "Boas"
@app.route('/log/', methods=['GET','POST'])
def logmessages():
    print(request.data.decode('utf8'))
    return request.data.decode('utf8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)