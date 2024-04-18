from flask import Blueprint, request

import controllers

auth = Blueprint('auth', __name__)


@auth.route('/auth', methods=['POST'])
def auth_token_add():
    return controllers.auth_token_add(request)


@auth.route("/logout/<user_id>", methods=["PUT"])
def logout(user_id):
    return controllers.logout(request, user_id)
