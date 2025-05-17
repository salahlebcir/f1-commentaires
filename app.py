#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 11:47:15 2025

@author: slebcir
"""

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "commentaires.json"
USERS_FILE = "users.json"

# Initialiser les fichiers si vides
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    pseudo = data.get("pseudo")
    password = data.get("password")

    if not pseudo or not password:
        return jsonify({"error": "Champs manquants"}), 400

    with open(USERS_FILE, "r+") as f:
        users = json.load(f)
        if pseudo in users:
            return jsonify({"error": "Pseudo déjà pris"}), 400
        users[pseudo] = password
        f.seek(0)
        json.dump(users, f)
        f.truncate()

    return jsonify({"message": "Inscription réussie"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    pseudo = data.get("pseudo")
    password = data.get("password")

    with open(USERS_FILE, "r") as f:
        users = json.load(f)
        if pseudo not in users or users[pseudo] != password:
            return jsonify({"error": "Identifiants incorrects"}), 401

    return jsonify({"message": "Connexion réussie"}), 200

@app.route("/comments", methods=["GET", "POST"])
def comments():
    if request.method == "GET":
        type_graphique = request.args.get("type")
        gp = request.args.get("gp")
        cible = request.args.get("cible")

        with open(DATA_FILE, "r") as f:
            commentaires = json.load(f)

        filtres = [
            c for c in commentaires
            if c["type_graphique"] == type_graphique and
               c["grand_prix"] == gp and
               str(c["cible"]) == str(cible)
        ]
        return jsonify(filtres)

    if request.method == "POST":
        data = request.json
        data["timestamp"] = time_now()
        with open(DATA_FILE, "r+") as f:
            commentaires = json.load(f)
            commentaires.append(data)
            f.seek(0)
            json.dump(commentaires, f, indent=2)
            f.truncate()
        return jsonify({"message": "Commentaire ajouté"}), 201

# Fonction utilitaire pour l'heure
from datetime import datetime
def time_now():
    return datetime.utcnow().isoformat()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


