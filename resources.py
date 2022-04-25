from flask_restful import Resource, request, abort
from pandas import read_csv
from numpy import percentile

from db_models import FileModel, ColumnStatisticsModel, db


class File(Resource):
    def get(self, filename):
        file_data = FileModel.query.filter_by(filename=filename).first()
        if file_data:
            columns_data = (
                ColumnStatisticsModel.query.filter_by(filename=filename)
                .order_by(ColumnStatisticsModel.column_name)
                .all()
            )
            return {
                "file": file_data.to_json(),
                "columns": [column.to_json() for column in columns_data],
            }, 200

        return {"message": "File not found"}, 404

    def post(self, filename):
        csv_file = FileModel.query.filter_by(filename=filename).first()
        if csv_file:
            return {"message": "File already exists"}, 400
        csv_file = read_csv(request.files["files"])
        file_row_numbers = csv_file.shape[0]
        file_column_numbers = csv_file.shape[1]
        file = FileModel(
            filename=filename, n_columns=file_column_numbers, n_rows=file_row_numbers
        )
        db.session.add(file)

        columns_to_return = []
        for column_name in csv_file.columns:
            column_statistics = ColumnStatisticsModel(
                column_name=column_name,
                filename=filename,
                minimum_val=float(csv_file[column_name].min()),
                maximum_val=float(csv_file[column_name].max()),
                mean=float(csv_file[column_name].mean()),
                percentile_10=float(percentile(csv_file[column_name], 10)),
                percentile_90=float(percentile(csv_file[column_name], 90)),
                percent_of_missing_values=float(
                    csv_file[column_name].isnull().sum() / file_row_numbers
                ),
            )
            columns_to_return.append(column_statistics)
            db.session.add(column_statistics)

        db.session.commit()
        return {
            "file": file.to_json(),
            "columns": [column.to_json() for column in columns_to_return],
        }, 201

    def delete(self, filename):
        file = FileModel.query.filter_by(filename=filename).first()
        if file:
            db.session.delete(file)
            db.session.commit()
            return {"message": "File deleted"}, 200
        return {"message": "File not found"}, 404


class Statistics(Resource):
    def get(self, filename, statistic_name):
        print(filename, statistic_name)
        file_data = FileModel.query.filter_by(filename=filename).first()
        if file_data:
            try:
                columns_data = (
                    ColumnStatisticsModel.query.filter_by(filename=filename)
                    .order_by(ColumnStatisticsModel.column_name)
                    .all()
                )
                return {
                    "file": file_data.to_json(),
                    "columns": [
                        {
                            "column_name": getattr(column, "column_name"),
                            statistic_name: getattr(column, statistic_name),
                        }
                        for column in columns_data
                    ],
                }, 200
            except AttributeError:
                return {"message": "Statistic not found"}, 404

        return {"message": "File not found"}, 404
