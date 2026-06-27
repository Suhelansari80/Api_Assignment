from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
import uuid
import hashlib

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))

db = client["student_db"]
collection = db["students"]

db = client["student_db"]

collection = db["students"]
todo_collection = db["todo_items"]   # New collection

@app.route('/')
def home():
    return render_template("index.html")


# Task 1 API Route
@app.route('/api')
def api():

    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


# Task 2 Form Submit
@app.route('/submit', methods=['POST'])
def submit():



    try:

        last_student = collection.find_one(sort=[("item_id", -1)])
        next_id = 1 if last_student is None else last_student["item_id"] + 1

        hash_string = request.form["name"] + request.form["email"]
        item_hash = hashlib.sha256(hash_string.encode()).hexdigest()

        student = {
            "item_id": next_id,
            "item_uuid": str(uuid.uuid4()),
            "item_hash": item_hash,
            "name": request.form["name"],
            "email": request.form["email"]
        }

        collection.insert_one(student)

        return redirect(url_for('success'))

    except Exception as e:
        return render_template("index.html", error=str(e))


@app.route('/success')
def success():
    return render_template("success.html")

@app.route("/todo")
def todo():
    return render_template("todo.html")


@app.route('/submittodoitem', methods=['POST'])
def submittodoitem():
    try:
        todo = {
            "itemName": request.form["itemName"],
            "itemDescription": request.form["itemDescription"]
        }

        db["todo_items"].insert_one(todo)

        return jsonify({
            "message": "Todo item saved successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/submittodoitem', methods=['POST'])
def submittodoitem():
    try:
        todo = {
            "itemName": request.form["itemName"],
            "itemDescription": request.form["itemDescription"]
        }

        db["todo_items"].insert_one(todo)

        return jsonify({
            "message": "Todo item saved successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)