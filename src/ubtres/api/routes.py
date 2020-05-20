import os
from datetime import datetime
from flask import Blueprint
from flask import url_for
from flask import current_app
from flask import jsonify, g, request
from ubtres.models import User, Result
from ubtres import db
from ubtres.utils import get_defconfig_data
from ubtres.api.auth import basic_auth, token_auth
from ubtres.api.errors import bad_request
from ubtres.errors.handlers import error_404, error_416

restapi = Blueprint('api', __name__)

# token managment
@restapi.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

@restapi.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204

# routing
@restapi.route('/result/<int:id>', methods=['GET'])
@token_auth.login_required
def get_result(id):
    return jsonify(Result.query.get_or_404(id).to_dict())

@restapi.route('/result/<string:defconfig>', methods=['GET'])
@token_auth.login_required
def get_defconfig_lastid(defconfig):
    """
    get last reported result from defconfig
    """
    result = Result.query.filter(Result.defconfig==defconfig).order_by(-Result.id).first()
    if result == None:
        return error_404(0)

    # ToDo return ID
    return jsonify(result.to_dict())


@restapi.route('/newresult', methods=['POST'])
@token_auth.login_required
def set_result():
    # https://medium.com/@manivannan_data/how-to-get-data-received-in-flask-request-8ebadc2bb5c6
    # https://toolbelt.readthedocs.io/en/latest/uploading-data.html
    #print("---- Headers ", request.headers)
    #print("---------------------------- args ", request.args)
    #print("---------------------------- files ", request.files)
    #print("---------------------------- value ", request.values)
    #print("---------------------------- form ", request.form)
    #print("---------------------------- data ", request.data)

    form = request.form
    for ch in ['title', 'build_date', 'arch', 'soc', 'cpu', 'toolchain', 'basecommit', 'boardname', 'defconfig', 'content', 'success', 'images']:
        if ch not in form:
            return bad_request(f'must include {ch} field')

    res = Result()
    ret = res.from_form(form)
    if not ret:
        return bad_request(f'images must be in json format [{"name":"imgname", "size":"imgsize"}]')

    res.author = g.current_user
    # we only have a id, when we committed the result, so commit...
    db.session.add(res)
    db.session.commit()

    # now get files
    path = current_app.config['STORE_FILES'] + f"/{res.id}"

    os.mkdir(path)
    if "tbotlog" in request.files:
        f = request.files["tbotlog"]
        f.save(f"{path}/tbot.log")
        res.hastbotlog = True
        db.session.commit()
    if "tbotjson" in request.files:
        f = request.files["tbotjson"]
        f.save(f"{path}/tbot.json")
        res.hastbotjson = True
        db.session.commit()
    if "systemmap" in request.files:
        f = request.files["systemmap"]
        f.save(f"{path}/System.map")
        res.hassystemmap = True
        db.session.commit()


    response = jsonify({})
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_token')
    return response
