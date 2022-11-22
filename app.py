from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('presidents', user='postgres', password='', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db


class Presidents(BaseModel):
  name = CharField()
  party = CharField()
  year_elected = IntegerField()
  is_alive = BooleanField()
  vice_president_id = IntegerField()


db.connect()

app = Flask(__name__)

@app.route('/presidents/', methods=['GET', 'POST'])
@app.route('/presidents/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Presidents.get(Presidents.id == id)))
    else:
        presidents_list = []
        for person in Presidents.select():
            presidents_list.append(model_to_dict(person))
        return jsonify(presidents_list)

  if request.method =='PUT':
    body = request.get_json()
    Presidents.update(body).where(Presidents.id == id).execute()
    return "President " + str(id) + " has been updated."

  if request.method == 'POST':
    new_president = dict_to_model(Presidents, request.get_json())
    new_president.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    Presidents.delete().where(Presidents.id == id).execute()
    return "President " + str(id) + " deleted."

app.run(debug=True, port=9000)
