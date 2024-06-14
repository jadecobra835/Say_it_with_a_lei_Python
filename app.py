from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from mysql.connector import Error
import json
from datetime import date

app = Flask(__name__)
cors = CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000", 
            "https://xjj-say-it-with-a-lei-34e7166cb08e.herokuapp.com"
        ],
        "methods": ["POST", "GET", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://ijvfg0wx4cjc30z1:zl87h5usl76bemkt@enqhzd10cxh7hv2e.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/rw3nklf1029jieu'

# jawsdb_url = SQLAlchemy(app)

# def my_db():
#     connection = None
#     try: 
#         if jawsdb_url:
#             import urllib.parse as urlparse
#             url = urlparse.urlparse(jawsdb_url)
#             connection = mysql.connector.connect(
#                 user=url.username,
#                 password=url.password,
#                 host=url.hostname,
#                 port=url.port,
#                 database=url.path[1:]
#             )
#         else:
#             connection = mysql.connector.connect(
#                 user="root",
#                 password="BlueStitch2006!",
#                 host="localhost",
#                 port=3306,
#                 database = "lei_catalog"
#             )
#         print("Connection to MySQL DB successful")
#     except Error as e:
#         print(f"The error '{e}' occured")

#     return connection



# mydb = my_db()
mydb = SQLAlchemy(app)

@app.route("/auth", methods=["POST"])
def authCheck():
    developer = {
        "auth[userName]": "xanderjamesjensen@icloud.com",
        "auth[password]": "stitch2006"
    }

    jen = {
        "auth[userName]": "djgilsons",
        "auth[password]": "Aloha2001!"
    }

    auth_data = (request.form)
    
    if auth_data["auth[userName]"] == developer["auth[userName]"] and auth_data["auth[password]"] == developer["auth[password]"]:
        return "Success"
    elif auth_data["auth[userName]"] == jen["auth[userName]"] and auth_data["auth[password]"] == jen["auth[password]"]:
        return "Success"
    else:
        return "Wrong username or password"


@app.route("/add-lei", methods=["POST"])
def add_lei():
    post_data = (request.json)

    name = post_data['name']
    price = post_data['price']
    image = post_data['image']
    description = post_data['description']
    color1 = post_data['color1']
    color2 = post_data['color2']
    color3 = post_data['color3']
    color4 = post_data['color4']
    type = post_data['type']

    sql = '''INSERT INTO preset_leis ( name, price, image, description, color1, color2, color3, color4, type)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    
    leiItem = ( name, price, image, description, color1, color2, color3, color4, type)
    
    mydb.execute(sql, leiItem)
    mydb.commit()

    return jsonify("record inserted")


@app.route("/get-preset-leis", defaults={'type': None}, methods=["GET"])
@app.route('/get-preset-leis/<type>')
def get_leis(type):
    graduation = ("SELECT * FROM preset_leis WHERE type ='%s'" % type)
    mydb.execute(graduation)
    myresult = mydb.fetchall()

    def decodeBytes(data):
        return [{   
            'id': item[0],
            'name': item[1],
            'price': item[2],
            'image': item[3].decode('utf-8'),
            'description': item[4],
            'color1': item[5],
            'color2': item[6],
            'color3': item[7],
            'color4': item[8],
            'type': item[9]
        } for item in data]
    
    decodedData = decodeBytes(myresult)

    json_data = json.dumps(decodedData)

    return json_data
    

@app.route("/get-one-lei", defaults={'product_id': None}, methods=["GET"])
@app.route('/get-one-lei/<product_id>')
def get_lei(product_id):
    comboString = "SELECT * FROM preset_leis WHERE id =" + product_id
    mydb.execute(comboString)
    myresult = mydb.fetchall()

    def decodeBytes(data):
        return [{   
            'id': item[0],
            'name': item[1],
            'price': item[2],
            'image': item[3].decode('utf-8'),
            'description': item[4],
            'color1': item[5],
            'color2': item[6],
            'color3': item[7],
            'color4': item[8],
            'type': item[9]
        } for item in data]
    
    decodedData = decodeBytes(myresult)

    json_data = json.dumps(decodedData)

    return json_data


@app.route('/delete-lei/<product_id>', methods=["DELETE"])
def deleteLei(product_id):
    command = "DELETE FROM preset_leis WHERE id=" + product_id
    
    try: 
        mydb.execute(command)
        mydb.commit()
        return 'Successfully deleted Lei'

    except mysql.connector.Error as error:
        return 'Failed to delete Lei'


if __name__ == "__main__":
    app.run(host='localhost', port=5000)