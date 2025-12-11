from flask import *
import pymysql
import os
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename





app = Flask(__name__)



@app.route('/')
def home():
    return render_template('Homepage.html')




if __name__ == '__main__':
    app.run(debug=True)

