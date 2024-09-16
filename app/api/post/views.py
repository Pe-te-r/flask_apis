from app.api.post import post_bp

@post_bp.route('/',methods=['GET'])
def get_posts():
    return {'posts': []}, 200
    