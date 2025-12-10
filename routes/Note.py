
from flask import Blueprint,render_template,request,jsonify

home_blueprint = Blueprint("home", __name__)

@home_blueprint.route("/home")
def home():
    return render_template("home.html")


notes_blueprint = Blueprint("notes",__name__)

note_list = []
next_id = 1



@notes_blueprint.route("/", methods=["GET"])
def get_notes():
    return jsonify(note_list), 200

@notes_blueprint.route("/", methods=["POST"])
def notes():
    data = request.get_json()
    required_field = ['title','content','tags']

    for field in required_field:
     if not data.get(field):    
      return jsonify({"error":f"Missing {field}"}),400
     
    new_notes = {
          "id": next_id,
          "title": data['title'],
          "content":data['content'],
          "tags":data['tags']
     }
    
    note_list.append(new_notes)
    next_id = next_id +1

    

    return jsonify(new_notes), 201