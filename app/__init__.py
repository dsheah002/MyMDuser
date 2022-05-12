from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#    'mysql+pymysql://DevLogMaterialInventory_u01:.eL=vW/M::2Oqw5@devux-db.sin.infineon.com:3306/DevLogMaterialInventory'
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'mysql+pymysql://DevLogMaterialInventory_adm:JZul3IM/lvBSnS0@devux-db.sin.infineon.com:3306/DevLogMaterialInventory'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import routes, models_glue, routes_glue, models_lead, routes_lead, models_mold, routes_mold, models_wafer, \
    routes_wafer
