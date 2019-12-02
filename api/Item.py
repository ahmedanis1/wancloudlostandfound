from flask_restful import Resource
from flask import Flask,request, jsonify
from model.models import Item
from model.models import User
from app import app
from app import dataBase
from functools import wraps
import jwt
import json


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

         
        data = jwt.decode(token, app.config['SECRET_KEY'])
        decod=data['public_id']
        
        current_user = User.query.filter_by(public_id=decod).first()
    
        # return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
@app.route('/itemadded', methods=['POST'])
@token_required
def ItemAdded(current_user):
    
    
    newItem = Item(Categories=request.json["categories"], NameOfItem=request.json["name"], Location=request.json["location"], DescriptionOfItem=request.json["description"], Date=request.json["Date"],PicOfItem=request.json["picpath"],user_id=current_user.id)
    dataBase.create_all()
    dataBase.session.add(newItem)
    dataBase.session.commit()
    dataBase.session.close()
    
    resp = jsonify({"Action": 'Item Added Successfully'})
  
    resp.status_code = 200
    return resp
    

    # except:
    #     resp = jsonify({"Response": 'User not added succesfully'})
    #     resp.status_code = 200
    #     return resp
@app.route('/deleteitem/<_id>',methods=['delete'])
@token_required
def ItemDelted(current_user,_id):
    
    deletedItem = Item.query.filter_by(id=_id, user_id=current_user.id).first()

    if not deletedItem:
        return jsonify({'message' : 'No item found!'})

    dataBase.session.delete(deletedItem)
    dataBase.session.commit()
    return jsonify({'message' : ' item deleted!'})

@app.route('/search')
@token_required
def searchItem(current_user):
    try:
        if("name" in request.args and "location" in request.args):
            
            searchResult = Item.query.filter_by(NameOfItem=request.args['name'],Location=request.args['location'])
            return jsonify({'result': 'Item Found'})
        if("location" in request.args  ):
            
            searchResult = Item.query.filter_by(Location=request.args['location'])
            return jsonify({'result': 'Item Found'})
        if("name" in request.args):
            
            searchResult = Item.query.filter_by(NameOfItem=request.args['name'])
            return jsonify({'result': 'Item Found'})
        

    except:
        resp = jsonify({"Response": 'Item not found'})
        resp.status_code = 200
        return resp
@app.route('/search/<_id>',methods=['PUT'])
@token_required
def updateItem(current_user,_id):
    
    
    updateItem = Item.query.filter_by(id=_id, user_id=current_user.id).update(dict(Categories=request.json["categories"], NameOfItem=request.json["name"], Location=request.json["location"], DescriptionOfItem=request.json["description"], Date=request.json["Date"],PicOfItem=request.json["picpath"],user_id=current_user.id))
    # updateItem = Item(Categories=request.json["categories"], NameOfItem=request.json["name"], Location=request.json["location"], DescriptionOfItem=request.json["description"], Date=request.json["Date"],PicOfItem=request.json["picpath"],user_id=current_user.id)
    # dataBase.session.update(updateItem)
    dataBase.session.commit()
    dataBase.session.close()
    
    resp = jsonify({"Action": 'Item update Successfully'})
  
    resp.status_code = 200
    return resp
    
