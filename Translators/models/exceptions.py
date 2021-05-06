
import logging, translators as ts

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)-10s - %(message)s')

class Translation:
    def __new__(cls, file_path: str):
        try:
            open(file_path)
        except FileNotFoundError:
            logging.error('No File Match Search...')
        except:
            logging.error('Invalid Path!!')
        else:
            return super().__new__(cls)

    def __init__(self, file_path: str):
        self.path = file_path
        with open(self.path, encoding = 'utf-8') as fl:
            self.text = fl.readlines()
        logging.info('Successfully Read File.')

    def process(self, from_lang = 'auto', target_language = 'fa', pro = 'google'):
        self.translated = []
        try:
            for line in self.text:
                self.translated.append(getattr(ts, pro)(line, from_language = 'auto', to_language = target_language))
        except: logging.error('Invalid Language! Pay Attention to Language in the Google Translate...')
        print(*self.translated, sep = '\n')
        return self.translated

    def save_file(self, file_name: str):
        try:
            fl = open('\\'.join(self.path.split('\\')[: -1]) + '\\' + file_name, 'x', encoding = 'utf-8')
        except FileExistsError:
            logging.warning('File has Existed...')
        except:
            logging.error('File Name Must be is a String.')
        else:
            try:
                translate = self.translated
            except AttributeError:
                translate = self.process()
            finally:
                with fl:
                    print(*translate, sep = '\n', file = fl)
                logging.info('Saved Content into the File!')

    def __repr__(self):
        return f"File at {self.path} Location."
