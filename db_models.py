from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class FileModel(db.Model):
    __tablename__ = "files"
    id = db.Column(db.String(32), primary_key=True)
    filename = db.Column(db.String(100))
    insert_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    n_columns = db.Column(db.Integer)
    n_rows = db.Column(db.Integer)
    columns = db.relationship(
        "ColumnStatisticsModel", backref="files", lazy=True, cascade="all, delete"
    )

    def to_json(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "insert_date": self.insert_date.strftime("%m/%d/%Y, %H:%M:%S"),
            "n_columns": self.n_columns,
            "n_rows": self.n_rows,
        }


class ColumnStatisticsModel(db.Model):
    __tablename__ = "column_statistics"
    column_name = db.Column(db.String(100), primary_key=True)
    file_id = db.Column(db.String(32), db.ForeignKey("files.id"), primary_key=True)
    data_type = db.Column(db.String(10))
    numeric_minimum_val = db.Column(db.Float)
    numeric_maximum_val = db.Column(db.Float)
    text_minimum_val = db.Column(db.String(200))
    text_maximum_val = db.Column(db.String(200))

    mean = db.Column(db.Float)
    percentile_10 = db.Column(db.Float)
    percentile_90 = db.Column(db.Float)

    percent_of_missing_values = db.Column(db.Float)

    def to_json(self):
        return (
            {
                "column_name": self.column_name,
                "data_type": self.data_type,
                "minimum_val": self.numeric_minimum_val,
                "maximum_val": self.numeric_maximum_val,
                "mean": self.mean,
                "percentile_10": self.percentile_10,
                "percentile_90": self.percentile_90,
                "percent_of_missing_values": self.percent_of_missing_values,
            }
            if self.data_type == "Numeric"
            else {
                "column_name": self.column_name,
                "data_type": self.data_type,
                "minimum_val": self.text_minimum_val,
                "maximum_val": self.text_maximum_val,
                "mean": self.mean,
                "percentile_10": self.percentile_10,
                "percentile_90": self.percentile_90,
                "percent_of_missing_values": self.percent_of_missing_values,
            }
        )
