from flask_restful import Resource, request
from pandas import read_csv
from numpy import percentile
from pandas.api.types import is_numeric_dtype
import joblib

from db_models import FileModel, ColumnStatisticsModel, db


class File(Resource):
    """
    Resource to handle actions associated with files.

    """
    def get(self, file_id_or_filename):
        """
        If file_id_or_filename is file_id return data of file and data of all of this file
        If file_id_or_filename is filename return data for files with that name

        :param file_id_or_filename: file ID or filename
        """

        file_data = FileModel.query.filter_by(id=file_id_or_filename).first()
        if file_data:
            columns_data = (
                ColumnStatisticsModel.query.filter_by(file_id=file_id_or_filename)
                .order_by(ColumnStatisticsModel.column_name)
                .all()
            )
            return {
                "file": file_data.to_json(),
                "columns": [column.to_json() for column in columns_data],
            }, 200

        file_data = FileModel.query.filter_by(filename=file_id_or_filename).all()
        if file_data:
            return {
                "filenames": file_id_or_filename,
                "files": [file.to_json() for file in file_data],
            }, 200

        return {"message": "File not found"}, 404

    def post(self):
        """
        Upload file to server.
        """
        file = request.files["file"]
        file_data = read_csv(file)
        file_data_hash = joblib.hash(file_data)
        file_in_database = FileModel.query.filter_by(id=file_data_hash).first()
        if file_in_database:
            return {
                "message": f"File already exists in database. Request file with id: {file_data_hash}"
            }, 400
        filename = file.filename
        file_row_numbers = file_data.shape[0]
        file_column_numbers = file_data.shape[1]
        file = FileModel(
            id=file_data_hash,
            filename=filename,
            n_columns=file_column_numbers,
            n_rows=file_row_numbers,
        )
        db.session.add(file)

        columns_to_return = []
        for column_name in file_data.columns:
            if is_numeric_dtype(file_data[column_name]):
                column_statistics = ColumnStatisticsModel(
                    column_name=column_name,
                    data_type="Numeric",
                    file_id=file_data_hash,
                    numeric_minimum_val=float(file_data[column_name].min()),
                    numeric_maximum_val=float(file_data[column_name].max()),
                    mean=float(file_data[column_name].mean()),
                    percentile_10=float(percentile(file_data[column_name], 10)),
                    percentile_90=float(percentile(file_data[column_name], 90)),
                    percent_of_missing_values=float(
                        file_data[column_name].isnull().sum() / file_row_numbers
                    ),
                )
            else:
                column_statistics = ColumnStatisticsModel(
                    column_name=column_name,
                    data_type="Text",
                    file_id=file_data_hash,
                    text_minimum_val=str(file_data[column_name].min()),
                    text_maximum_val=str(file_data[column_name].max()),
                    percent_of_missing_values=float(
                        file_data[column_name].isnull().sum() / file_row_numbers
                    ),
                )
            columns_to_return.append(column_statistics)
            db.session.add(column_statistics)

        db.session.commit()
        return {
            "file": file.to_json(),
            "columns": [column.to_json() for column in columns_to_return],
        }, 201

    def delete(self, file_id_or_filename):
        """
        Delete file from server database.

        :param file_id_or_filename: file ID (passing filename won't work) 
        """
        file = FileModel.query.filter_by(id=file_id_or_filename).first()
        if file:
            db.session.delete(file)
            db.session.commit()
            return {"message": "File deleted"}, 200
        return {"message": "File not found"}, 404


class Statistics(Resource):
    """
    Resource to handle actions associated with statistics.
    """
    def get(self, file_id, statistic_name):
        """
        Return value of passed statistic for each column in passed file.

        :param file_id: file ID to get values from 
        :param statistic_name: name of statistic to get
        """
        try:
            columns_data = (
                ColumnStatisticsModel.query.filter_by(file_id=file_id)
                .order_by(ColumnStatisticsModel.column_name)
                .all()
            )
            if columns_data: 
                return {
                    "columns": [
                        {
                            "column_name": getattr(column, "column_name"),
                            statistic_name: getattr(column, statistic_name),
                        }
                        for column in columns_data
                    ],
                }, 200
            else:
                return {"message": "File not found"}, 404

        except AttributeError:
            return {"message": "Statistic not found"}, 404

