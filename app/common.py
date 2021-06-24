from flask import Blueprint, Response, session, request, render_template
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join(script_dir, '..', "..")
sys.path.append(mymodule_dir)
import smartschool.app.modules.common.login as login

common = Blueprint('common', __name__)


@common.route('/login', methods=['POST'])
def login_post():
    if not session.get("is_admin"):
        session["is_admin"] = login.login(request.form)

    resp = Response("")
    resp.headers["Location"] = "aquarium"
    resp.status_code = 302
    return resp


@common.route('/login', methods=['GET'])
def login_get():
    if not session.get("is_admin"):
        return render_template("/login.html")

    resp = Response("")
    resp.headers["Location"] = "aquarium"
    resp.status_code = 302
    return resp


@common.route('/logout')
def logout():
    if session.get("is_admin"):
        session.pop("is_admin")

    resp = Response("")
    resp.headers["Location"] = "aquarium"
    resp.status_code = 302
    return resp


@common.route("/api/logged_in", methods=["GET"])
def logged_in():
    resp = Response("")
    if not session.get("is_admin") or not session["is_admin"]:
        resp.set_cookie("logged_in", "false", 86400)
        return resp

    resp.set_cookie("logged_in", "true", 86400)
    return resp
