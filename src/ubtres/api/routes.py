from datetime import datetime
from flask import Blueprint
from flask import url_for
from flask import jsonify, g, request
from ubtres.models import User, Result
from ubtres import db
from ubtres.api.auth import basic_auth, token_auth
from ubtres.api.errors import bad_request

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

@restapi.route('/newresult', methods=['POST'])
@token_auth.login_required
def set_result():
    data = request.get_json() or {}
    for ch in ['title', 'build_date', 'arch', 'soc', 'cpu', 'toolchain', 'basecommit', 'boardname', 'defconfig', 'splsize', 'ubsize', 'content', 'success']:
        if ch not in data:
            return bad_request(f'must include {ch} field')

    res = Result()
    res.from_dict(data)
    res.author = g.current_user
    db.session.add(res)
    db.session.commit()
    response = jsonify(res.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_token')
    return response
