from flask import Flask, render_template, redirect, request

app = Flask(__name__)

from app.controllers import default