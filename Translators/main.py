
from models.exceptions import *

def main():
    file_cashe = {}
    print('Welcome to my Translator ^_^')
    while True:
        command = input('\n1.Translate New File\n2.Translate Previous File\n3.Save Translation\n4.Exit\n>>> ')
        if command == '1':
            path = input('\n\t<Open New File>\n~$ ')
            if path in file_cashe:
                logging.warning('File Already has Read...')
            else:
                new_file = Translation(path)
                if new_file: file_cashe[path] = new_file

        elif command == '2':
            print('\n\t<Translating>\nList of Files:', *file_cashe.keys(), sep = '\n')
            path = input('\n~$ ')
            try:
                file_cashe[path]
            except KeyError:
                logging.error('No File Match Search...')
            else:
                language = input('What Target Language Translation?(Enter for Persian) ').lower()[: 2] or 'fa'
                file_cashe[path].process(target_language = language)
                logging.debug('Successfully Translate.')

        elif command == '3':
            print('\n\t<Saving File Translate>\nList of Files:', *file_cashe.keys(), sep='\n')
            path = input('\n~$ ')
            try:
                file_cashe[path]
            except KeyError:
                logging.error('No File Match Search...')
            else:
                name = input('Please Enter Your File Name: ')
                file_cashe[path].save_file(name)

        elif command == '4':
            logging.warning('Close Program.')
            break

        else:
            logging.error('Invalid Input! Try Again...')

import argparse, os
parser = argparse.ArgumentParser(description = 'Translator')
parser.add_argument('text', metavar = 'PATH', action = 'store', type = str, default = "", nargs='?',help = 'Path File')
parser.add_argument('-t', '--to_lang', metavar='TO LANGUAGE', action='store', required= True, type=str, help='To Language')
parser.add_argument('-f', '--from_lang', metavar='From Language', action='store', default = 'auto', help='From Language')
parser.add_argument('-p', '--provider', metavar='PROVIDER', action='store', default = 'google', choices=['google', 'bing'])
args = parser.parse_args()

if args.text == "":
    lines = []
    while True:
        try:
            line = input(">>> ")
            lines.append(line + '\n')
        except KeyboardInterrupt:
            break
    with open('example.txt','w') as f:
        f.writelines(lines)
    args.text = os.getcwd() + "\\example.txt"

trans = Translation(args.text)
print(trans.process(args.from_lang, args.to_lang, args.provider))
