
from flask import Blueprint,render_template,request,jsonify
from database import db
from models import Notetable

home_blueprint = Blueprint("home", __name__)

@home_blueprint.route("/home")
def home():
    return render_template("home.html")


notes_blueprint = Blueprint("notes",__name__)






@notes_blueprint.route("/", methods=["GET"])
def get_notes():
    notes = Notetable.query.all()  
    notes_data = []
    for note in notes:
        notes_data.append({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "tags": note.tags,
            "created_at": note.created_at,
            "updated_at": note.updated_at
        })
    return jsonify(notes_data), 200

@notes_blueprint.route("/", methods=["POST"])
def notes():
    data = request.get_json()
    required_field = ['title','content','tags']

    for field in required_field:
     if not data.get(field):    
      return jsonify({"error":f"Missing {field}"}),400
     
    new_notes = Notetable(
          title= data['title'],
          content=data['content'],
          tags=data['tags']
     )
    
   
    

    db.session.add(new_notes)
    db.session.commit()

    
    return jsonify(new_notes.to_dict()), 201


@notes_blueprint.route("/<int:note_id>",methods=["PUT"])
def update_data(note_id):
   data = request.get_json()

   if not data:
      return jsonify({"error":"no data provided"}),400
   
   note = Notetable.query.get(note_id)

   if not note:
      return jsonify({"error":"no data found"}),400
   
   if "title" in data:
      note.title=data["title"]

   if "content" in data:
     note.content=data["content"]

   if "tags" in data:
     note.tags=data["tags"]

   db.session.commit()

   return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "tags": note.tags.split(",") if note.tags else []
    }), 200
    


@notes_blueprint.route("/<int:note_id>",methods=["DELETE"])
def delete_data(note_id):
   note = Notetable.query.get(note_id)

   if not note:
      return jsonify({"error":"no data found"}),400
   
   db.session.delete(note)
   db.session.commit()

   return jsonify({"messege":"Data deleted succecfully"}),200



@notes_blueprint.route("/",methods=["GET"])
def search_data():
   tag = request.args.get("tag") 

   if tag:
      notes = Notetable.query.filter(
         Notetable.tags.like(f"{tag}")
      )

   
   result= []
   for note in notes:
        result.append({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "tags": note.tags,
            "created_at": note.created_at,
            "updated_at": note.updated_at
        })
   return jsonify(result), 200