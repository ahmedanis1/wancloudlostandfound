from flask import Flask, request, jsonify,make_response
from model.models import User
from flask_restful import Resource 
from app import app
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
# from jwt import JWT
import datetime
from app import dataBase


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

@app.route('/signup', methods=['POST'])
def signup():

    # name= request.json['name']
    # email=request.json['email']
    # age=request.json['age']
    # password=request.json['password']
    dataBase.create_all()
    # hashed_password = generate_password_hash(request.json['password'], method='sha256')
    new_user = User(name= request.json['name'],email=request.json['email'],public_id=str(uuid.uuid4()),age=request.json['age'],password=request.json['password'])
    print(new_user)
    dataBase.session.add(new_user)
    dataBase.session.commit()
    dataBase.session.close()
    resp = jsonify({"Response": 'User Added Successfully',"username":""})
    resp.status_code = 200
    return resp

    # except:
    #     resp = jsonify({"Response": 'User not added succesfully'})
    #     resp.status_code = 200
    #     return resp


@app.route('/sigin',methods=['POST'])
def sigin():
    # jwt = JWT()
    dataBase.create_all()
    
    auth = request.json
    


    if not auth or not str(auth['email']) or not auth['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        
    user = User.query.filter_by(email=auth['email']).first()
    
        
    if not user:
        return make_response('Could not verify2', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    a=str(user.password)
    b=str( auth['password'])
    print (a,b)
    # c=check_password_hash(a, b)
    # print(c)
    if a==b:
        token = jwt.encode({'public_id' : user.public_id} , app.config['SECRET_KEY'])
        print(str(token))
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not find you', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
@app.route('/updatepassword',methods=['PUT'])
@token_required
def updatePassword(current_user,):
    try:
        
        updatePassword = User.query.filter_by(id=request.args['id'],).update(dict(password=request.json["password"]))
        print(updatePassword)
        dataBase.session.commit()
        dataBase.session.close()

        resp = jsonify({"Action": 'Password update Successfully'})

        resp.status_code = 200
        return resp
    except:
        resp = jsonify({"Response": 'sorry cant update'})
        resp.status_code = 200
        return resp

