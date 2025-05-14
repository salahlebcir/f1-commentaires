#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 11:47:15 2025

@author: slebcir
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Comment
import hashlib
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def home():
    return "✅ Backend opérationnel"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    pseudo = data.get("pseudo")
    password = data.get("password")
    if not pseudo or not password:
        return jsonify({"error": "Champs requis"}), 400
    if User.query.filter_by(pseudo=pseudo).first():
        return jsonify({"error": "Pseudo déjà pris"}), 409
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    db.session.add(User(pseudo=pseudo, password_hash=password_hash))
    db.session.commit()
    return jsonify({"message": "Compte créé"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    pseudo = data.get("pseudo")
    password = data.get("password")
    user = User.query.filter_by(pseudo=pseudo).first()
    if not user:
        return jsonify({"error": "Utilisateur inconnu"}), 404
    if user.password_hash != hashlib.sha256(password.encode()).hexdigest():
        return jsonify({"error": "Mot de passe incorrect"}), 401
    return jsonify({"message": "Connexion réussie", "pseudo": pseudo}), 200

@app.route("/comments", methods=["POST"])
def add_comment():
    data = request.get_json()
    c = Comment(
        auteur=data.get("auteur"),
        contenu=data.get("contenu"),
        timestamp=datetime.utcnow().isoformat(),
        type_graphique=data.get("type_graphique"),
        grand_prix=data.get("grand_prix"),
        cible=data.get("cible")
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({"message": "Commentaire enregistré"}), 201

@app.route("/comments", methods=["GET"])
def get_comments():
    type_graphique = request.args.get("type")
    grand_prix = request.args.get("gp")
    cible = request.args.get("cible")
    q = Comment.query.filter_by(type_graphique=type_graphique, grand_prix=grand_prix)
    if cible:
        q = q.filter_by(cible=cible)
    return jsonify([
        {"auteur": c.auteur, "contenu": c.contenu, "timestamp": c.timestamp}
        for c in q.order_by(Comment.timestamp.desc()).all()
    ])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
