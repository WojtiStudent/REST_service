from flask import Flask
from flask_restful import Api
from sqlalchemy_utils.functions import database_exists

from db_models import db
from resources import File, Statistics

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///statistics.db'
db.init_app(app)




if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    with app.app_context():
        from db_models import FileModel, ColumnStatisticsModel
        db.create_all()



api.add_resource(File, '/file/<string:filename>')
api.add_resource(Statistics, '/statistics/<string:filename>/<string:statistic_name>')



if __name__ == '__main__':
    app.run(debug=True)