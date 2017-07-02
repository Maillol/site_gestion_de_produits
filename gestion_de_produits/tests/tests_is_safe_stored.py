from django.test import TestCase

from ..models import StoredChemicalProduct, PackagingProduct, Storage


class TestIsSafeStored(TestCase):

    def setUp(self):
        Storage.objects.create(
            storage_name='s1', laboratory_name='1', floor='1', room='1',
            temperature_min=10, temperature_max=20,
            ventilated_cupboard=False, air=False, moisture=False,
            light=False)

        Storage.objects.create(
            storage_name='s2', laboratory_name='1', floor='1', room='2',
            temperature_min=10, temperature_max=20,
            ventilated_cupboard=True, air=False, moisture=False,
            light=False)

        Storage.objects.create(
            storage_name='s3', laboratory_name='1', floor='1', room='3',
            temperature_min=10, temperature_max=20,
            ventilated_cupboard=False, air=True, moisture=False,
            light=False)

        Storage.objects.create(
            storage_name='s4', laboratory_name='1', floor='1', room='4',
            temperature_min=10, temperature_max=20,
            ventilated_cupboard=False, air=False, moisture=True,
            light=False)

        Storage.objects.create(
            storage_name='s5', laboratory_name='1', floor='1', room='5',
            temperature_min=10, temperature_max=20,
            ventilated_cupboard=False, air=False, moisture=False,
            light=True)

        Storage.objects.create(
            storage_name='s6', laboratory_name='1', floor='1', room='6',
            temperature_min=10, temperature_max=20,
            ventilated_cupboard=False, air=True, moisture=True,
            light=True)

        p1 = PackagingProduct.objects.create(
            name='p1',
            temperature_min=10, temperature_max=20,
            ventilated_cupboard=False, air=False, moisture=False,
            light=False)

        p2 = PackagingProduct.objects.create(
            name='p2',
            temperature_min=11, temperature_max=20,
            ventilated_cupboard=False, air=False, moisture=False,
            light=False)

        p3 = PackagingProduct.objects.create(
            name='p3',
            temperature_min=10, temperature_max=19,
            ventilated_cupboard=False, air=False, moisture=False,
            light=False)

        p4 = PackagingProduct.objects.create(
            name='p4',
            temperature_min=10, temperature_max=20,
            ventilated_cupboard=True, air=False, moisture=False,
            light=False)

        p5 = PackagingProduct.objects.create(
            name='p5',
            temperature_min=10, temperature_max=20,
            ventilated_cupboard=False, air=True, moisture=False,
            light=False)

        p6 = PackagingProduct.objects.create(
            name='p6',
            temperature_min=10, temperature_max=20,
            ventilated_cupboard=False, air=False, moisture=True,
            light=False)

        p7 = PackagingProduct.objects.create(
            name='p7',
            temperature_min=10, temperature_max=20,
            ventilated_cupboard=False, air=False, moisture=False,
            light=True)

    def assert_compatible_storage(self, packaging_name, storage_name,
                                  expected):
        storage = Storage.objects.get(storage_name=storage_name)
        packaging = PackagingProduct.objects.get(name=packaging_name)
        product = StoredChemicalProduct(packaging_product=packaging,
                                        storage_area=storage)

        if expected:
            self.assertTrue(product.is_safe_stored)
        else:
            self.assertFalse(product.is_safe_stored)

    def test_p1_s1_should_true(self):
        self.assert_compatible_storage('p1', 's1', True)

    def test_p1_s2_should_true(self):
        self.assert_compatible_storage('p1', 's2', True)

    def test_p1_s3_should_true(self):
        self.assert_compatible_storage('p1', 's3', True)

    def test_p1_s4_should_true(self):
        self.assert_compatible_storage('p1', 's4', True)

    def test_p1_s5_should_true(self):
        self.assert_compatible_storage('p1', 's5', True)

    def test_p1_s6_should_true(self):
        self.assert_compatible_storage('p1', 's6', True)

    def test_p2_s1_should_false_because_tmp_min(self):
        self.assert_compatible_storage('p2', 's1', False)

    def test_p2_s2_should_false_because_tmp_min(self):
        self.assert_compatible_storage('p2', 's2', False)

    def test_p2_s3_should_false_because_tmp_min(self):
        self.assert_compatible_storage('p2', 's3', False)

    def test_p2_s4_should_false_because_tmp_min(self):
        self.assert_compatible_storage('p2', 's4', False)

    def test_p2_s5_should_false_because_tmp_min(self):
        self.assert_compatible_storage('p2', 's5', False)

    def test_p2_s6_should_false_because_tmp_min(self):
        self.assert_compatible_storage('p2', 's6', False)

    def test_p3_s1_should_false_because_tmp_max(self):
        self.assert_compatible_storage('p3', 's1', False)

    def test_p3_s2_should_false_because_tmp_max(self):
        self.assert_compatible_storage('p3', 's2', False)

    def test_p3_s3_should_false_because_tmp_max(self):
        self.assert_compatible_storage('p3', 's3', False)

    def test_p3_s4_should_false_because_tmp_max(self):
        self.assert_compatible_storage('p3', 's4', False)

    def test_p3_s5_should_false_because_tmp_max(self):
        self.assert_compatible_storage('p3', 's5', False)

    def test_p3_s6_should_false_because_tmp_max(self):
        self.assert_compatible_storage('p3', 's6', False)

    def test_p4_s1_should_false_because_ventilated_cupboard(self):
        self.assert_compatible_storage('p4', 's1', False)

    def test_p4_s2_should_true(self):
        self.assert_compatible_storage('p4', 's2', True)

    def test_p4_s3_should_false_because_ventilated_cupboard(self):
        self.assert_compatible_storage('p4', 's3', False)

    def test_p4_s4_should_false_because_ventilated_cupboard(self):
        self.assert_compatible_storage('p4', 's4', False)

    def test_p4_s5_should_false_because_ventilated_cupboard(self):
        self.assert_compatible_storage('p4', 's5', False)

    def test_p4_s6_should_false_because_ventilated_cupboard(self):
        self.assert_compatible_storage('p4', 's6', False)

    def test_p5_s1_should_false_because_air(self):
        self.assert_compatible_storage('p5', 's1', False)

    def test_p5_s2_should_false_because_air(self):
        self.assert_compatible_storage('p5', 's2', False)

    def test_p5_s3_should_true(self):
        self.assert_compatible_storage('p5', 's3', True)

    def test_p5_s4_should_false_because_air(self):
        self.assert_compatible_storage('p5', 's4', False)

    def test_p5_s5_should_false_because_air(self):
        self.assert_compatible_storage('p5', 's5', False)

    def test_p5_s6_should_true(self):
        self.assert_compatible_storage('p5', 's6', True)

    def test_p6_s1_should_false_because_moisture(self):
        self.assert_compatible_storage('p6', 's1', False)

    def test_p6_s2_should_false_because_moisture(self):
        self.assert_compatible_storage('p6', 's2', False)

    def test_p6_s3_should_false_because_moisture(self):
        self.assert_compatible_storage('p6', 's3', False)

    def test_p6_s4_should_true(self):
        self.assert_compatible_storage('p6', 's4', True)

    def test_p6_s5_should_false_because_moisture(self):
        self.assert_compatible_storage('p6', 's5', False)

    def test_p6_s6_should_true(self):
        self.assert_compatible_storage('p6', 's6', True)

    def test_p7_s1_should_false_because_light(self):
        self.assert_compatible_storage('p7', 's1', False)

    def test_p7_s2_should_false_because_light(self):
        self.assert_compatible_storage('p7', 's2', False)

    def test_p7_s3_should_false_because_light(self):
        self.assert_compatible_storage('p7', 's3', False)

    def test_p7_s4_should_false_because_light(self):
        self.assert_compatible_storage('p7', 's4', False)

    def test_p7_s5_should_true(self):
        self.assert_compatible_storage('p7', 's5', True)

    def test_p7_s6_should_true(self):
        self.assert_compatible_storage('p7', 's6', True)
