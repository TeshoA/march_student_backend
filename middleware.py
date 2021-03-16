from flask import jsonify, abort, make_response, request
from data_provider_service import DataProviderService
from utilities import titlecase

DATA_PROVIDER = DataProviderService()


# get all posts
def post():
    posts = DATA_PROVIDER.get_post_with_author()
    return jsonify({"posts": posts})


# get post by id
def post_by_id(post_id):
    current_post = DATA_PROVIDER.get_post_with_author(post_id)
    if current_post:
        return jsonify({"post": current_post})
    else:
        # In case we did not find the post by id
        # we send HTTP 404 - Not Found error to the client
        abort(404)


# update a post
def update_post(post_id):
    title = request.form["title"]
    content = request.form["content"]

    formatted_title = titlecase(title)
    formatted_content = (str(content))[:1].upper() + (str(content))[1:]

    new_post = {
        "title": formatted_title,
        "content": formatted_content
    }
    updated_post = DATA_PROVIDER.update_post(post_id, new_post)
    if not updated_post:
        return make_response('', 404)
    else:
        return jsonify({"post": updated_post})


def add_post():
    try:
        title = request.form["title"]
        content = request.form["content"]
        user_id = request.form["userid"] # if no one is logged in, there is no userid, so an exception is raised

    except Exception:
        user_id = 1 # set to user 1 (Guest) since no one is logged in

    # uses a utilities class to correctly capitalise the title string
    formatted_title = titlecase(title)
    formatted_content = (str(content))[:1].upper() + (str(content))[1:]

    new_post_id = DATA_PROVIDER.add_post(title=formatted_title, content=formatted_content, author_id=user_id)

    created_post = DATA_PROVIDER.get_post_with_author(new_post_id)
    if created_post:
        return jsonify({"post": created_post})
    else:
        # In case we did not find the post by id
        # we send HTTP 404 - Not Found error to the client
        abort(404)


def login():
    username = request.form["username"]
    password = request.form["password"]
    user = DATA_PROVIDER.is_user_valid(username, password)
    if user is not None:
        resp = make_response(jsonify({'id': user[0],'username': user[1]}), 200)
        return resp
    else:
        abort(404)


def logout():
    userid = request.cookies.get('userid')
    username = request.cookies.get('username')
    user = DATA_PROVIDER.is_logged_in_user_valid(userid, username)

    if user is not None:
        resp = make_response(jsonify({'id': '','username': ''}), 200)
        return resp
    else:
        abort(404)


def register():
    username = request.form["username"]
    password = request.form["password"]

    new_user_id = DATA_PROVIDER.add_user(username, password)

    if new_user_id:
        return jsonify({"user": new_user_id})
    else:
        # In case we did not create the user
        # we send HTTP 404 - Not Found error to the client
        abort(404)

