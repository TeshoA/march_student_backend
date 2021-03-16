from flask import jsonify
from middleware import post, post_by_id, add_post, update_post
from middleware import register, login, logout


def initialize_routes(app):
    if app:
        app.add_url_rule('/api', 'list_routes', list_routes, methods=['GET'], defaults={'app': app})
        app.add_url_rule('/api/post', 'post', post, methods=['GET'])
        app.add_url_rule('/api/post', 'add_post', add_post, methods=['POST'])
        app.add_url_rule('/api/post/<int:post_id>', 'post_by_id', post_by_id, methods=['GET'])
        # app.add_url_rule('/api/post/update/<int:post_id>', 'update_post', update_post, methods=['PUT'])
        app.add_url_rule('/api/post/update/<int:post_id>', 'update_post', update_post, methods=['PUT'])
        app.add_url_rule('/api/user', 'register', register, methods=['POST'])
        app.add_url_rule('/api/user/login', 'login', login, methods=['POST'])
        app.add_url_rule('/api/user/logout', 'logout', logout, methods=['POST'])


def list_routes(app):
    result = []
    for rt in app.url_map.iter_rules():
        result.append({
            'methods': list(rt.methods),
            'route': str(rt)
        })
    return jsonify({'routes': result, 'total': len(result)})
