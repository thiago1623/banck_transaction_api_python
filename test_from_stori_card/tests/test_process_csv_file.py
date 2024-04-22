import os

from django.test import TestCase
from transaction_management_api.utils.csv_processor import CSVProcessor


class CSVProcessorTestCase(TestCase):
    def test_process(self):
        """
            method that called `process` of CSVProcessor and save the result
        :return:
        """
        file_path = os.path.join(os.path.dirname(__file__), '../file_testing_data.csv')
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            result = CSVProcessor.process(csv_file)
        self.assertIsInstance(result, list)


class GenerateSummaryTestCase(TestCase):
    def test_generate_summary_returns_dict(self):
        """
        method that called `generate_summary` of CSVProcessor and save the result
        """
        result = CSVProcessor.generate_summary()

        # Verifica que el resultado sea un diccionario
        self.assertIsInstance(result, dict)

    def test_generate_summary_keys_exist(self):
        # Llama al método `generate_summary` de CSVProcessor y guarda el resultado
        result = CSVProcessor.generate_summary()

        # Verifica que las claves 'total_balance' y 'detailed_info' existan en el resultado
        self.assertIn('total_balance', result)
        self.assertIn('detailed_info', result)

