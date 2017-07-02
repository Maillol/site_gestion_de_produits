from itertools import dropwhile
import csv
from functools import partial
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from gestion_de_produits.models import Pictogram, Hazard, Preventive


DATA_PATH = Path(__file__).parent / 'data'


class ReadCSVError(Exception):
    """
    Raised when reading CSV failed
    """

    def __init__(self, line, file_name, real_error=None):
        self.line = line
        self.file_name = file_name
        self.real_error = real_error
        super().__init__()


class Command(BaseCommand):

    STEPS = ('hazard', 'preventive', 'pictogram')
    LANGS = ('en', 'fr')

    def add_arguments(self, parser):
        parser.add_argument('--start-resource', nargs='?', default='hazard')
        parser.add_argument('--start-line', nargs='?', type=int, default=1)

    def handle(self, *args, **options):
        start_resource = options['start_resource']
        start_line = options['start_line']

        for step in dropwhile(lambda step: step != start_resource,
                              self.STEPS):
            self.stdout.write(step + ' filling ...')
            for lang in self.LANGS:
                try:
                    if lang == self.LANGS[0]:
                        action = getattr(self, 'save_{}'.format(step))
                    else:
                        action = partial(
                            getattr(self, 'update_{}'.format(step)),
                            lang=lang)

                    self._fill(lang,
                               '{}.csv'.format(step),
                               action,
                               start_line)

                except ReadCSVError as error:
                    msg = self.style.ERROR(
                        'Error in CSV file {} line {}.'
                        ' Fix it and relaunch command with'
                        ' `--start-resource={} --start-line={}`'.
                        format(error.file_name, error.line, step, error.line))
                    self.stdout.write(msg)
                    raise error.real_error

            start_line = 1

        self.stdout.write(self.style.SUCCESS('Successfully database filled'))

    def _fill(self, lang, csv_file_name, save_func, start=1):
        """
        Read csv_file_name and call save_func for each line.
        Can raise a ReadCSVError exception.
        """
        with (DATA_PATH / lang / csv_file_name).open() as csv_file:
            lines = enumerate(csv.reader(csv_file, delimiter=';'), 1)
            for line_num, row in dropwhile(lambda line: line[0] != start,
                                           lines):
                try:
                    save_func(row)
                except Exception as error:
                    raise ReadCSVError(line_num, csv_file_name, error)

    @staticmethod
    def save_hazard(row):
        attrs = {
            'name': row[0],
            'en_description': row[1]
        }
        Hazard(**attrs).save()

    @staticmethod
    def save_preventive(row):
        attrs = {
            'name': row[0],
            'en_description': row[1]
        }
        Preventive(**attrs).save()

    @staticmethod
    def save_pictogram(row):
        attrs = {
            'name': row[0],
            'en_description': row[1],
            'en_note': row[2]
        }
        with (DATA_PATH / 'pictogram_jpg' /
                '{}.jpg'.format(row[0])).open('rb') as jpg_file:

            pictogram = Pictogram(**attrs)
            pictogram.picture.save(row[0], File(jpg_file))

    @staticmethod
    def update_hazard(row, lang):
        attrs = {
            '{}_description'.format(lang): row[1]
        }
        Hazard.objects.filter(name=row[0]).update(**attrs)

    @staticmethod
    def update_preventive(row, lang):
        attrs = {
            '{}_description'.format(lang): row[1]
        }
        Preventive.objects.filter(name=row[0]).update(**attrs)

    @staticmethod
    def update_pictogram(row, lang):
        attrs = {
            '{}_description'.format(lang): row[1],
            '{}_note'.format(lang): row[2]
        }
        Pictogram.objects.filter(name=row[0]).update(**attrs)
