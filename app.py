from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

db_url = 'mysql://ijvfg0wx4cjc30z1:zl87h5usl76bemkt@enqhzd10cxh7hv2e.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/rw3nklf1029jieu3'

url = urlparse(db_url)

db_user = url.username
db_password = url.password
db_host = url.hostname
db_port = url.port
db_name = url.path[1:]

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class leiItems(db.Model):
    __tablename__ = 'preset_leis'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    description = db.Column(db.String(1000))
    color1 = db.Column(db.String(45), nullable=False)
    color2 = db.Column(db.String(45))
    color3 = db.Column(db.String(45))
    color4 = db.Column(db.String(45))
    type = db.Column(db.String(20))


def create_tables():
    db.create_all()


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

@app.route("/get-preset-leis", defaults={'leiType': None}, methods=["GET"])
@app.route('/get-preset-leis/<leiType>')
def get_preset_leis(leiType):
    try:
        results = leiItems.query.all()

        data = [{
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'image': item.image.decode('utf-8'),
            'description': item.description,
            'color1': item.color1,
            'color2': item.color2,
            'color3': item.color3,
            'color4': item.color4,
            'type': item.type
        } for item in [ leitype for leitype in results if leitype.type == leiType]]

        return jsonify(data)
    except Exception as e:
        return jsonify(error=str(e)), 500
    

@app.route("/add-lei", methods=["POST"])
def add_lei():
    post_data = request.json

    name = post_data['name']
    price = post_data['price']
    image = post_data['image'].encode('utf-8')  # Assuming the image is provided as a base64-encoded string
    description = post_data['description']
    color1 = post_data['color1']
    color2 = post_data['color2']
    color3 = post_data['color3']
    color4 = post_data['color4']
    type = post_data['type']

    new_lei = leiItems(
        name=name,
        price=price,
        image=image,
        description=description,
        color1=color1,
        color2=color2,
        color3=color3,
        color4=color4,
        type=type
    )

    db.session.add(new_lei)
    db.session.commit()

    return jsonify("record inserted")


@app.route("/get-one-lei", defaults={'product_id': None}, methods=["GET"])
@app.route('/get-one-lei/<product_id>')
def get_lei(product_id):
    leiItem = leiItems.query.filter_by(id=product_id).first()

    def decodeBytes(data):
        return [{   
            'id': data.id,
            'name': data.name,
            'price': data.price,
            'image': data.image.decode('utf-8'),
            'description': data.description,
            'color1': data.color1,
            'color2': data.color2,
            'color3': data.color3,
            'color4': data.color4,
            'type': data.type
        }]
    
    decodedData = decodeBytes(leiItem)

    json_data = json.dumps(decodedData)

    return json_data

    
@app.route('/delete-lei/<product_id>', methods=["DELETE"])
def deleteLei(product_id):
    leiItems.query.filter_by(id=product_id).delete()
    db.session.commit()
    return 'Successfully deleted Lei'


if __name__ == "__main__":
    app.run(host='localhost', port=5000)
    # app.run(debug=True)