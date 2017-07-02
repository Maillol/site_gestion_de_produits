from django.core.management import call_command
from django.test import TestCase

from ....models import Pictogram, Hazard, Preventive


class TestCommand(TestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()     
        call_command('fill_database')

    def test_hazard_h200_should_be_stored(self):
        hazard = Hazard.objects.get(name='H200')
        self.assertEqual(hazard.fr_description, "Explosif instable")
        self.assertEqual(hazard.en_description, "Unstable explosive")

    def test_database_should_contain_96_hazards(self):
        self.assertEqual(Hazard.objects.count(), 96)

    def test_preventive_p101_should_be_stored(self):
        preventive = Preventive.objects.get(name='P101')
        self.assertEqual(
            preventive.fr_description, 
            "En cas de consultation d’un médecin, garder à disposition le"
            " récipient ou l’étiquette.")
        self.assertEqual(
            preventive.en_description, 
            "If medical advice is needed, have product container or label"
            " at hand.")

    def test_database_should_contain_139_preventive(self):
        self.assertEqual(Preventive.objects.count(), 139)

    def test_pictogram_SGH01_should_be_stored(self):
        pictogram = Pictogram.objects.get(name='SGH01')
        self.assertEqual(pictogram.fr_description, "Explosif")
        self.assertEqual(pictogram.en_description, "Explosive")

    def test_database_should_contain_9_pictograms(self):
        self.assertEqual(Pictogram.objects.count(), 9)


class TestCommandWithCustomStart(TestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()     
        call_command('fill_database', start_resource='preventive', 
                     start_line=100)

    def test_hazard_should_not_stored(self):
        self.assertEqual(Hazard.objects.count(), 0)

    def test_database_should_contain_40_preventive(self):
        self.assertEqual(Preventive.objects.count(), 40)

    def test_database_should_contain_9_pictograms(self):
        self.assertEqual(Pictogram.objects.count(), 9)
