from django.test import TestCase
from django.utils.translation import activate

from ..models import Hazard, Pictogram


class TestHazard(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.hazard = Hazard(
            name='H201',
            fr_description='fr language desc',
            en_description='en language desc'
        )
        cls.hazard.save()

    def test_description_shoud_be_fr_when_active_lang_is_fr(self):
        activate('fr')
        self.assertEqual(self.hazard.description, 'fr language desc')

    def test_description_shoud_be_en_when_active_lang_is_en(self):
        activate('en')
        self.assertEqual(self.hazard.description, 'en language desc')


class TestPictogram(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pictogram = Pictogram(
            name='SG01',
            fr_description='Explosif',
            en_description='Explosive',
            fr_note='Rend SGH02 et SGH03 facultatifs',
            en_note='SGH02 and SGH03 become optional'
        )
        cls.pictogram.save()

    def test_description_shoud_be_fr_when_active_lang_is_fr(self):
        activate('fr')
        self.assertEqual(self.pictogram.description, 'Explosif')

    def test_description_shoud_be_en_when_active_lang_is_en(self):
        activate('en')
        self.assertEqual(self.pictogram.description, 'Explosive')

    def test_note_shoud_be_fr_when_active_lang_is_fr(self):
        activate('fr')
        self.assertEqual(self.pictogram.note,
                         'Rend SGH02 et SGH03 facultatifs')

    def test_note_shoud_be_en_when_active_lang_is_en(self):
        activate('en')
        self.assertEqual(self.pictogram.note,
                         'SGH02 and SGH03 become optional')
