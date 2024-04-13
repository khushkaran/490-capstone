from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, marshal_with, fields
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


# how to run it: flask --app server --debug run

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class CharacterModel(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    tag = db.Column(db.String(100), nullable=False)
    reader = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Character(name ={name}, tag = {tag}, reader = {reader})"

set_char_args = reqparse.RequestParser()
set_char_args.add_argument("name", type=str, help="Name of character is needed", required=True)
set_char_args.add_argument("tag", type=str, help="tag is needed", required=True)
set_char_args.add_argument("reader", type=str, help="reader is needed", required=True)

update_char_args = reqparse.RequestParser()
update_char_args.add_argument("name", type=str, help="Name of character is needed", required=True)
update_char_args.add_argument("tag", type=str, help="tag is needed")
update_char_args.add_argument("reader", type=str, help="reader is needed")

resource_fields = {
    'name': fields.String,
    'tag': fields.String,
    'reader': fields.String
}

resource_fields2 = {
    'tag': fields.String,
    'reader': fields.String
}

resource_fields3 = {
    'name': fields.String
}


class AddChar(Resource):

    @marshal_with(resource_fields)
    def get(self, name):
        result = CharacterModel.query.filter_by(name=name).first()
        if not result:
            abort(404, message="Could not find character")
        return result
    
   
    
    @marshal_with(resource_fields)
    def put(self, name):
        args = set_char_args.parse_args()
        result = CharacterModel.query.filter_by(name=name).first()
        if result:
            abort(409, message="Character with name exsist")
        character = CharacterModel(name=name, tag=args['tag'], reader=args['reader'])
        db.session.add(character)
        db.session.commit()
        return character, 201
    
    @marshal_with(resource_fields)
    def patch(self, name):
        args =  update_char_args.parse_args()
        result = CharacterModel.query.filter_by(name=name).first()
        if not result:
            abort(404, message="Character doesn't exsist")

        if args["name"]:
            result.name = args['name']

        if args["tag"]:
            result.tag = args['tag']

        if args["reader"]:
            result.name = args['reader']
        
        db.session.commit()

        return result


    def delete(self, name):

        result = CharacterModel.query.filter_by(name=name).first()
        if not result:
            abort(404, message="Character doesn't exsist")

        result.delete()
        db.session.commit()

        return '', 204



class GetReaderAndTags(Resource):

    @marshal_with(resource_fields2)
    def get(self):
        result = CharacterModel.query.all()
        if not result:
            abort(404, message="No characters exsist")
        
        return result
    
class GetAllChar(Resource):

    @marshal_with(resource_fields3)
    def get(self):
        result = CharacterModel.query.all()
        if not result:
            abort(404, message="No characters exsist")
        return result
    
api.add_resource(AddChar, "/addChar/<string:name>")
api.add_resource(GetReaderAndTags, "/getReaderAndTags")
api.add_resource(GetAllChar, "/getAllChar")
    
if __name__ == "__main__":
    app.run(debug=True)