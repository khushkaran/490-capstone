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
    isRegistered = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Character(name ={self.name}, tag = {self.tag}, reader = {self.reader}, registered = {self.isRegistered})"




set_char_args = reqparse.RequestParser()
set_char_args.add_argument("name", type=str, help="Name of character is needed", required=True)
set_char_args.add_argument("tag", type=str, help="Tag is needed", required=True)
set_char_args.add_argument("reader", type=str, help="Reader is needed", required=True)


update_char_args = reqparse.RequestParser()
update_char_args.add_argument("name", type=str, help="Name of character is needed", required=True)
update_char_args.add_argument("tag", type=str, help="Tag is needed")
update_char_args.add_argument("reader", type=str, help="Reader is needed")



resource_fields = {
    'name': fields.String,
    'tag': fields.String,
    'reader': fields.String,
}

resource_fields_tag_and_reader = {
    'tag': fields.String,
    'reader': fields.String
}

resource_fields_char_name = {
    'name': fields.String,
}



class AddChar(Resource):

    # get all info such as reader, tag, name and if it has been regsteried  for char with name
    @marshal_with(resource_fields)
    def get(self, name):
        result = CharacterModel.query.filter_by(name=name).first()
        if not result:
            abort(404, message="Could not find character")
        return result
    
   
    
    # would only we ever called by python
    @marshal_with(resource_fields)
    def put(self):
        args = set_char_args.parse_args()
        result = CharacterModel.query.filter_by(name=args['tag']).first()
        if result:
            abort(409, message="Character with name exsist")
        character = CharacterModel(name=args['name'], tag=args['tag'], reader=args['reader'], isRegistered=False)
        db.session.add(character)
        db.session.commit()
        return character, 201
    

    @marshal_with(resource_fields)
    def patch(self):
        args =  update_char_args.parse_args()

        
        result =  CharacterModel.query.filter_by(tag=args["tag"], reader=args["reader"]).first()

       

        # character with given name doesn't exsist so can't update
        if not result:
                abort(404, message="Character doesn't exsist")

        
        result.name = args['name']

        if args["tag"]:
            result.tag = args['tag']

        if args["reader"]:
            result.reader = args['reader']

        result.isRegistered = True

        print(result)
        
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

    @marshal_with(resource_fields_tag_and_reader)
    def get(self):
        result = CharacterModel.query.all()
        if not result:
            abort(404, message="No characters exsist")
        
        return result
    
class GetAllChar(Resource):

    # returns the name of all characters that have been scanned or an emoty list if there are no character names
    @marshal_with(resource_fields_char_name)
    def get(self):
        result = CharacterModel.query.filter_by(isRegistered=True).all()
        print(result)
        return result

        

class GetRecentlyScannedChar(Resource):

    # returns the oldest tag thats doesn't have a character name with the reader and tag its associated with or an empty list if all characters have a name/there are no characters
    @marshal_with(resource_fields_tag_and_reader)
    def get(self):
        result =  CharacterModel.query.filter_by(isRegistered=False).first()
        return result




api.add_resource(AddChar, "/addChar")
#api.add_resource(GetReaderAndTags, "/getReaderAndTags")
api.add_resource(GetAllChar, "/getAllChar")
api.add_resource(GetRecentlyScannedChar, "/getRecentlyScannedChar")
    
if __name__ == "__main__":
    app.run(debug=True)