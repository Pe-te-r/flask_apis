from flask import request
from app.api.comments import comment_bp

comments = []

@comment_bp.route('/', methods=['GET'])
def get_comments():
    return {'comments': comments}, 200

@comment_bp.route('/', methods=['POST'])
def create_comment():
    data = request.get_json()
    comment = {
        'id': len(comments) + 1,
        'text': data['text'],
        'author': data['author']
    }
    comments.append(comment)
    return {'comment': comment}, 201