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


ports = []

class CharacterModel(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    tag = db.Column(db.String(100), nullable=False)
    reader = db.Column(db.String(100), nullable=False)
    soundFile = db.Column(db.String(100), nullable=False)
    isRegistered = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Character(name ={self.name}, tag = {self.tag}, reader = {self.reader}, registered = {self.isRegistered})"
    
class PortModel(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    port = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Port(port = {self.port})"
    


set_char_args = reqparse.RequestParser()
set_char_args.add_argument("name", type=str, help="Name of character is needed", required=True)
set_char_args.add_argument("tag", type=str, help="Tag is needed", required=True)
set_char_args.add_argument("reader", type=str, help="Reader is needed", required=True)
set_char_args.add_argument("soundFile", type=str, help="Sound file is needed", required=True)


update_char_args = reqparse.RequestParser()
update_char_args.add_argument("name", type=str, help="Name of character is needed", required=True)
update_char_args.add_argument("tag", type=str, help="Tag is needed")
update_char_args.add_argument("reader", type=str, help="Reader is needed")

add_sound_file_to_char_args = reqparse.RequestParser()
add_sound_file_to_char_args.add_argument("prevName", type=str, help="previous name of character is needed", required=True)
add_sound_file_to_char_args.add_argument("newName", type=str, help="New name of character is needed")
add_sound_file_to_char_args.add_argument("reader", type=str, help="Reader is needed")
add_sound_file_to_char_args.add_argument("soundFile", type=str, help="Sound file is needed")


delete_char_args = reqparse.RequestParser()
delete_char_args.add_argument("name", type=str, help="Name of character is needed", required=True)


get_char_args = reqparse.RequestParser()
get_char_args.add_argument("tag", type=str, help="Tag is needed", required=True)
get_char_args.add_argument("reader", type=str, help="Reader is needed", required=True)


add_ports_args = reqparse.RequestParser()
add_ports_args.add_argument("reader1", type=str, help="reader1 is needed", required=True)
add_ports_args.add_argument("reader2", type=str, help="reader2 is needed", required=True)
add_ports_args.add_argument("reader3", type=str, help="reader3 is needed", required=True)
add_ports_args.add_argument("reader4", type=str, help="reader4 is needed", required=True)


get_sound_file_args = reqparse.RequestParser()
get_sound_file_args.add_argument("name", type=str, help="Name of character is needed", required=True)





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

resource_fields_reader = {
    'reader': fields.String
}

resource_fields_update_char = {
    'name': fields.String,
    'tag': fields.String,
    'reader': fields.String,
    'soundFile': fields.String
}



resource_fields_ports = {
    'reader1': fields.String,
    'reader2': fields.String,
    'reader3': fields.String,
    'reader4': fields.String,
}

resource_fields_name_and_ports= {
    'name': fields.String,
    'port': fields.String,
}


resource_fields_soundFiles = {
    'soundFile': fields.String,
}

resource_fields_char_table = {
    'name': fields.String,
    'reader': fields.String,
    'soundFile': fields.String
}



class ModifyChar(Resource):

    
   
    
    # would only we ever called by python
    @marshal_with(resource_fields)
    def put(self):
        args = set_char_args.parse_args()
        result = CharacterModel.query.filter_by(name=args['tag']).first()
        if result:
            abort(409, message="Character with name exsist")
        character = CharacterModel(name=args['name'], tag=args['tag'], reader=args['reader'], isRegistered=False, soundFile=args['soundFile'])
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

   
    def delete(self):
        args = delete_char_args.parse_args()
        CharacterModel.query.filter_by(name=args["name"]).delete()
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

    # returns the name of all characters that have been scanned or an empty list if there are no character names
    @marshal_with(resource_fields_char_table)
    def get(self):
        result = CharacterModel.query.filter_by(isRegistered=True).all()
        return result
    
class GetAllReaders(Resource):

    # returns the name of all characters that have been scanned or an emoty list if there are no character names
    @marshal_with(resource_fields_reader)
    def get(self):
        result = CharacterModel.query.all()
        return result

        

class GetRecentlyScannedChar(Resource):

    # returns the oldest tag thats doesn't have a character name with the reader and tag its associated with or an empty list if all characters have a name/there are no characters
    @marshal_with(resource_fields_tag_and_reader)
    def get(self):
        result =  CharacterModel.query.filter_by(isRegistered=False).first()
        return result
    
class LinkSoundFileToCharcater(Resource):

    @marshal_with(resource_fields_update_char)
    def patch(self):
        args =  add_sound_file_to_char_args.parse_args()
        result =  CharacterModel.query.filter_by(name=args["prevName"]).first()
        # character with given name doesn't exsist so can't update
        if not result:
                abort(404, message="Character doesn't exsist")

        result.name = args['newName']

        if args["reader"]:
            result.reader = args['reader']

        if args["soundFile"]:
            result.soundFile = args['soundFile']      
        db.session.commit()

        return result
    
    @marshal_with(resource_fields_soundFiles)
    def get(self):
        args = get_sound_file_args.parse_args()
        result =  CharacterModel.query.filter_by(name=args['name']).first()
        if not result:
            return []
        return result
    
class Ports(Resource):

    @marshal_with(resource_fields_name_and_ports)
    def get(self):
        result = PortModel.query.all()
        if not result:
            return []
        
        return result

    @marshal_with(resource_fields_ports)
    def patch(self):
        args =  add_ports_args.parse_args() 
        reader1Result = PortModel.query.filter_by(name='reader1').first()
        reader2Result = PortModel.query.filter_by(name='reader2').first()
        reader3Result = PortModel.query.filter_by(name='reader3').first()
        reader4Result = PortModel.query.filter_by(name='reader4').first()

        # no ports have been assgined yet
        if not reader1Result:
            reader1 = PortModel(name="reader1", port=args['reader1'])
            reader2 = PortModel(name="reader2", port=args['reader2'])
            reader3 = PortModel(name="reader3", port=args['reader3'])
            reader4 = PortModel(name="reader4", port=args['reader4'])
            db.session.add(reader1)
            db.session.add(reader2)
            db.session.add(reader3)
            db.session.add(reader4)

        else:
            # ports have been assigned, just being updated
            reader1Result.port = args['reader1']
            reader2Result.port = args['reader2']
            reader3Result.port = args['reader3']
            reader4Result.port = args['reader4']

        db.session.commit()

        return {"reader1": args['reader1'], "reader2": args['reader2'], "reader3": args['reader3'], "reader4": args['reader4']}, 201
    
 
api.add_resource(ModifyChar, "/modifyChar")
api.add_resource(GetAllChar, "/getAllChar")
api.add_resource(GetRecentlyScannedChar, "/getRecentlyScannedChar")
api.add_resource(LinkSoundFileToCharcater, "/updateChar")
api.add_resource(Ports, "/ports")



if __name__ == "__main__":
    app.run(debug=True)