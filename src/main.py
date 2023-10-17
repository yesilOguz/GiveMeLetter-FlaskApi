import mysql.connector
from mysql.connector import Error

from flask import Flask, jsonify, request

from connection import Connection

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify({"message" : "There is no website. Please use api path"})

@app.route("/api", methods=["GET", "POST"])
def getTranslates():
    word = request.values['word']
    lang = request.values['lang']

    if(word == ''):
        return jsonify({"message" : "Please fill in the word argument"})

    conn = Connection("tr-en", "root", "12345")

    translateDict = {"message" : 'There is no lang for ' + lang}
    
    if(lang == 'en'):
        translateDict = conn.getTurksihFromEnglish(word)
    elif(lang == 'tr'):
        translateDict = conn.getEnglishFromTurkish(word)
        
    return jsonify(translateDict)        
 
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
