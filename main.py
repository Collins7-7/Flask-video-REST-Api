from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"


video_post_args = reqparse.RequestParser()
video_post_args.add_argument('name', type=str, required=True, help="Name of video is required")
video_post_args.add_argument('views', type=int, required=True, help="Views of video is required")
video_post_args.add_argument('likes', type=int, required=True, help="Likes of video is required")

video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str,help="Name of video is required")
video_update_args.add_argument('views', type=int,help="Views of video is required")
video_update_args.add_argument('likes', type=int,help="Likes of video is required")

resource_fields ={
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Addvideo(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = video_post_args.parse_args()
        result = VideoModel(name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(result)
        db.session.commit()
        return result, 201

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message='Could not find video with that id...')
        return result
        

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_post_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if result:
            abort(409, message='Video id taken...')
        video = VideoModel(id=video_id, name=args['name'],views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201


    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message='Could not find video with that id...')
        
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
            
        db.session.commit()
        return result, 200

    def delete(self, video_id):
        abort_if_video_id_missing(video_id)
        result = VideoModel.query.filter_by(id = video_id).first()
        db.session.delete(result)
        db.session.commit
        return '', 204

api.add_resource(Addvideo, '/videos')
api.add_resource(Video, "/videos/<int:video_id>")

if __name__ == '__main__':
    app.run(debug=True)