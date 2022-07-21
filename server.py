from flask import Flask
from flask_restful import Api

from sqlalchemy_utils.functions import database_exists
from argparse import ArgumentParser, RawTextHelpFormatter

from db_models import db
from resources import File, Statistics


parser = ArgumentParser(
    formatter_class=RawTextHelpFormatter,
    description="Simple REST API which receives tabular .csv files and"
    + " send back information about it:\n"
    + "\t * number of rows and columns\n"
    + "\t * statistics for each column:\n"
    + "\t\t - mean\n"
    + "\t\t - min and max val\n"
    + "\t\t - 10th and 90th percentile\n"
    + "\t\t - percent of missing values\n"
    + "\n"
    + "This application accepts both numeric and text data.",
)
parser.add_argument(
    "-p",
    "--port",
    type=int,
    default=5000,
    metavar="",
    help="Port on which the server should start. Default 5000.",
)
parser.add_argument(
    "-dbn",
    "--database-name",
    type=str,
    default="statistics",
    metavar="",
    help='Name of database that store data about receives files. Default "statistics".',
)
args = parser.parse_args()

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{args.database_name}.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    with app.app_context():
        from db_models import FileModel, ColumnStatisticsModel
        db.create_all()

api.add_resource(File, "/file", "/file/<string:file_id_or_filename>")
api.add_resource(Statistics, "/statistics/<string:file_id>/<string:statistic_name>")


if __name__ == "__main__":
    app.run(debug=False, port=args.port)
