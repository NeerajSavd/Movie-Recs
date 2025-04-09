from flask import Flask, render_template, request

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'awesome'
    return app
