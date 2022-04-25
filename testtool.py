import argparse
import requests
from pprint import pprint

BASE = "http://127.0.0.1:5000/"

parser = argparse.ArgumentParser(description='Test tool for the specyfic REST API')

parser.add_argument('-m', '--method', choices=['GET', 'POST', 'DELETE'], default='GET', help='Method to test', required=True)
parser.add_argument('-p', '--path', type=str, help='Path to file or just filename', required=True)
parser.add_argument('-s', '--statistic', type=str, help='File to upload')


args = parser.parse_args()


if __name__ == '__main__':
    filename = args.path[args.path.rfind('/') + 1:]

    if args.method == 'GET':
        if args.statistic:
            response = requests.get(BASE + 'statistics/' + filename + '/' + args.statistic)
        else:
            response = requests.get(BASE + 'file/' + filename)
    elif args.method == 'POST':
        if args.statistic:
            print('Can not upload file with statistic parameter, try without it')
            exit(1)
        else:
            response = requests.post(BASE + 'file/' + filename, files={'files': open(args.path, 'rb')})
    elif args.method == 'DELETE':
        if args.statistic:
            print('Can not delete specyfic statistic of file - you have to delete whole file.')
            exit(1)
        else:
            response = requests.delete(BASE + 'file/' + filename)
    else:
        print('Wrong method')
        exit(1)

    pprint(response.json())