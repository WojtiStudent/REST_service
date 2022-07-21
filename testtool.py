import requests
from argparse import ArgumentParser
from pprint import pprint

parser = ArgumentParser(description="Test tool for the specyfic REST API.")

parser.add_argument(
    "-m",
    "--method",
    choices=["GET", "POST", "DELETE"],
    default="GET",
    help="Method to test. Default GET.",
)
parser.add_argument(
    "-d",
    "--destination",
    type=str,
    default="127.0.0.1:5000",
    help="Adress to which send request. Default 127.0.0.1:5000.",
)
parser.add_argument(
    "-p", "--path", type=str, help="Path to file. Used if method == POST."
)
parser.add_argument(
    "-s",
    "--statistic",
    type=str,
    help="Statistic to get. Used if method == GET and file_id is passed.",
)
parser.add_argument(
    "-id",
    "--file_id",
    type=str,
    help="ID of file. Used if method == GET or method == DELETE.",
)
parser.add_argument(
    "-f", "--filename", type=str, help="Filename to search. Used if method == GET."
)


args = parser.parse_args()


if __name__ == "__main__":
    args.destination = "http://" + args.destination

    if args.method == "GET":
        if args.file_id:
            if args.statistic:
                response = requests.get(
                    args.destination
                    + "/"
                    + "statistics/"
                    + args.file_id
                    + "/"
                    + args.statistic
                )
            else:
                response = requests.get(args.destination + "/" + "file" + "/" + args.file_id)
        elif args.filename:
            response = requests.get(args.destination + "/" + "file" + "/" + args.filename)
        else:
            raise Exception(
                "Nor file_id neither filename has been passed while method is GET"
            )

    elif args.method == "POST":
        if args.path:
            filename = args.path[args.path.rfind("/") + 1 :]
            response = requests.post(
                args.destination + "/" + "file", files={"file": open(args.path, "rb")}
            )
        else:
            raise Exception("path has not been passed while methos id POST")

    elif args.method == "DELETE":
        if args.file_id:
            response = requests.delete(args.destination + "/" + "file/" + args.file_id)
        else:
            raise Exception("file_id has not been passed while method is DELETE")

    pprint(response.json())
