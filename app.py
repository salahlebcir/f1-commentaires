#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 11:47:15 2025

@author: slebcir
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

COMMENTS_FILE = "comments.json"

# Charger les commentaires depuis le fichier
def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Sauvegarder les commentaires dans le fichier
def save_comments(data):
    with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/comments", methods=["GET"])
def get_comments():
    type_graphique = request.args.get("type")
    gp = request.args.get("gp")
    cible = request.args.get("cible")
    comments = load_comments()
    filtres = [
        c for c in comments
        if c["type_graphique"] == type_graphique and c["grand_prix"] == gp and str(c["cible"]) == str(cible)
    ]
    return jsonify(filtres)

@app.route("/comments", methods=["POST"])
def post_comment():
    try:
        data = request.get_json()
        all_comments = load_comments()
        data["timestamp"] = request.headers.get("Date", "")
        all_comments.append(data)
        save_comments(all_comments)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/")
def index():
    return "✅ Backend Flask opérationnel"

if __name__ == "__main__":
    app.run(debug=True)


