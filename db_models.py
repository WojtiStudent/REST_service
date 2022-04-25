from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FileModel(db.Model):
    __tablename__ = 'files'
    filename = db.Column(db.String(100), primary_key=True)
    n_columns = db.Column(db.Integer)
    n_rows = db.Column(db.Integer)
    columns = db.relationship('ColumnStatisticsModel', backref='files', lazy=True, cascade='all, delete')

    def to_json(self):
        return {
            'filename': self.filename,
            'n_columns': self.n_columns,
            'n_rows': self.n_rows
        }


class ColumnStatisticsModel(db.Model):
    __tablename__ = 'column_statistics'
    column_name = db.Column(db.String(100), primary_key=True)
    filename = db.Column(db.String(100), db.ForeignKey('files.filename'), primary_key=True)
    minimum_val = db.Column(db.Float)
    maximum_val = db.Column(db.Float)
    mean = db.Column(db.Float)
    percentile_10 = db.Column(db.Float)
    percentile_90 = db.Column(db.Float)
    percent_of_missing_values = db.Column(db.Float)

    def to_json(self):
        return {
            'column_name': self.column_name,
            'filename': self.filename,
            'minimum_val': self.minimum_val,
            'maximum_val': self.maximum_val,
            'mean': self.mean,
            'percentile_10': self.percentile_10,
            'percentile_90': self.percentile_90,
            'percent_of_missing_values': self.percent_of_missing_values
        }