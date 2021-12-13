from flask import Flask, jsonify, request, render_template, make_response, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from my_app import app, db
import requests
from urllib.parse import quote
from my_app.forms import CreateTableForm
import sys
import pymysql
import json

def InfoConnection():
    rds_host = "dbtest.cctxaxqlrtny.us-east-1.rds.amazonaws.com"
    name = "admin"
    password = "quang810"
    db_name = ""

    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print(e)
        sys.exit()

    return conn