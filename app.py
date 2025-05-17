#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 11:47:15 2025

@author: slebcir
"""

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
COMMENTS_FILE = "comments.json"

def charger_commentaires():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_commentaires(commentaires):
    with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(commentaires, f, ensure_ascii=False, indent=2)

@app.route("/comments", methods=["GET", "POST"])
def comments():
    commentaires = charger_commentaires()

    if request.method == "GET":
        type_graph = request.args.get("type")
        gp = request.args.get("gp")
        cible = request.args.get("cible")
        filtres = [
            c for c in commentaires
            if c["type_graphique"] == type_graph and c["grand_prix"] == gp and str(c["cible"]) == str(cible)
        ]
        return jsonify(filtres)

    elif request.method == "POST":
        data = request.get_json()
        data["timestamp"] = datetime.utcnow().isoformat()
        commentaires.append(data)
        sauvegarder_commentaires(commentaires)
        return jsonify({"message": "Commentaire enregistré"}), 201
