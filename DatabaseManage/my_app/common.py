from flask import Flask, jsonify, request, render_template, make_response, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from my_app import app, db
import requests
from urllib.parse import quote
from my_app.forms import CreateTableForm
import sys
import pymysql
import json
