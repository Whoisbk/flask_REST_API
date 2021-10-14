from flask import Flask
from flask_restful import Api,Resource,reqparse,abort,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///AnimeDatabse.db'
db = SQLAlchemy(app)

class AnimeModel(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    seasons = db.Column(db.Integer,nullable=False)
    episodes = db.Column(db.Integer,nullable=False)
    rating = db.Column(db.Integer,nullable = False)


    def __repr__(self):#this if for when you want to view the data internaly in the database
        return f"Series(name = {name},seasons = {seasons},episodes = {episodes},rating={rating}"#


 
anime_put_args = reqparse.RequestParser()
anime_update_args = reqparse.RequestParser()

anime_put_args.add_argument("Name",type= str,help="Name of the anime series is required",required = True)#help is the error message that flask returns if i ddnt send that argument
anime_put_args.add_argument("Seasons",type= int,help="Seasons of the anime series are required",required = True)
anime_put_args.add_argument("Episodes",type= int,help="Number of Episodes for the anime series are required", required = True)
anime_put_args.add_argument("Rating",type= str,help="Rating of the anime series is reuired" ,required = True)


anime_update_args.add_argument("Name",type= str,help="Name of the anime series is required")#help is the error message that flask returns if i ddnt send that argument
anime_update_args.add_argument("Seasons",type= int,help="Seasons of the anime series are required")
anime_update_args.add_argument("Episodes",type= int,help="Number of Episodes for the anime series are required")
anime_update_args.add_argument("Rating",type= str,help="Rating of the anime series is reuired")

#resource feield is how an object should be serialised
resource_fields = {
    "id":fields.Integer,
    "name" :fields.String,
    "seasons" : fields.String,
    "episodes" : fields.String,
    "rating" : fields.String
    }

anime = {}
class MyAnime(Resource):#This class is a resource that we can override methods from and let us handle get,put,delete request
    @marshal_with(resource_fields)
    def get(self,animeId):
        seriesFound = AnimeModel.query.filter_by(id =animeId).first()

        if not seriesFound:
            abort(404,message = "Series ID not found")

        return seriesFound
    
    @marshal_with(resource_fields)
    def put(self,animeId):#create anime series
        
        args = anime_put_args.parse_args()#gets all the arguments in the put_args funtion and if not it will return a error message(help)
        seriesFound = AnimeModel.query.filter_by(id =animeId).first()

        if seriesFound:
            abort(409, message= "Series ID taken!!")

        series = AnimeModel(id = animeId,name =args["Name"],seasons = args["Seasons"],episodes= args["Episodes"],rating= args["Rating"])
        db.session.add(series)
        db.session.commit()
        return series,201#the 201 is the status code which stands for 'created'


    @marshal_with(resource_fields)
    def patch(self,animeId):
        args = anime_update_args.parse_args()
        seriesFound = AnimeModel.query.filter_by(id =animeId).first()
        if not seriesFound:
            abort(409, message= "Series does not exist, cannot update details!!")

        if "Name" in args:
            seriesFound.name = args["Name"]
        if "Seasons" in args:
            seriesFound.seasons = args["Seasons"]
        if "Episodes" in args:
            seriesFound.episodes = args["Episodes"]
        if "Rating" in args:
            seriesFound.rating = args["Rating"]

       
        db.session.commit()

        return seriesFound

    def delete(self,animeId):
        del anime[animeId]
        return '',204

api.add_resource(MyAnime,"/myAnime/<int:animeId>")#how to add resource
#animeId is the key for our anime dictionary


if __name__ == "__main__":
    
    app.run(debug=True)

