from io import BytesIO
from pathlib import Path
import shutil
from tempfile import mkdtemp
import urllib.request
import zipfile

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        if settings.DEBUG:
            static_dir = Path(settings.STATICFILES_DIRS[0])
        else:
            static_dir = Path(settings.STATIC_ROOT)

        if not static_dir.exists():
            self.stdout.write('creating {} directory'.format(static_dir))
            static_dir.mkdir()

        for directory in ('css', 'fonts', 'js'):
            if not (static_dir / directory).exists():
                self.stdout.write('creating {} directory'.
                                  format(static_dir / directory))
                (static_dir / directory).mkdir()

        self.stdout.write('downloading {}'.format(settings.BOOTSTRAP_URL))
        response = urllib.request.urlopen(settings.BOOTSTRAP_URL)

        file = zipfile.ZipFile(BytesIO(response.read()))
        tmpdir = mkdtemp()
        file.extractall(tmpdir)

        for path in Path(tmpdir).glob('bootstrap-*/js/*.min.js'):
            self.stdout.write('copy {} to {}'.format(path, static_dir / 'js'))
            shutil.copy(str(path), str(static_dir / 'js'))

        for path in Path(tmpdir).glob('bootstrap-*/css/*.min.css'):
            self.stdout.write('copy {} to {}'.format(path, static_dir / 'css'))
            shutil.copy(str(path), str(static_dir / 'css'))

        for path in Path(tmpdir).glob('bootstrap-*/fonts/*'):
            self.stdout.write('copy {} to {}'.format(path, static_dir / 'fonts'))
            shutil.copy(str(path), str(static_dir / 'fonts'))

        self.stdout.write('downloading {}'.format(settings.JQUERY_URL))
        response = urllib.request.urlopen(settings.JQUERY_URL)

        with (static_dir / 'js' / 'jquery.min.js').open('wb') as file:
            file.write(response.read())


