import unittest
from unittest.mock import Mock, patch
from cat_fact import (
    CatFactProcessor,
    ApiError,
)
from requests.exceptions import HTTPError
import json


class TestCatFactProcessor(unittest.TestCase):
    # get_fact

    @patch("cat_fact.requests.get")
    def test_get_fact_success(self, mock_get):
        """Позитивный тест: успешное получение факта"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"fact": "Cats sleep 70% of their lives"}
        mock_get.return_value = mock_response

        processor = CatFactProcessor()
        result = processor.get_fact()

        self.assertEqual(result, "Cats sleep 70% of their lives")
        self.assertEqual(processor.last_fact, result)
        mock_get.assert_called_once_with("https://catfact.ninja/fact")

    @patch("cat_fact.requests.get")
    def test_get_fact_http_error(self, mock_get):
        """Отрийательный тест: HTTP ошибка 500"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Server error")
        mock_get.return_value = mock_response

        processor = CatFactProcessor()

        with self.assertRaises(ApiError) as context:
            processor.get_fact()

        self.assertIn("Server error", str(context.exception))
        self.assertEqual(processor.last_fact, "")

    @patch("cat_fact.requests.get")
    def test_get_fact_invalid_json(self, mock_get):
        """Отрицательный тест: невалидный JSON в ответе"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = json.JSONDecodeError("Error", "doc", 0)
        mock_get.return_value = mock_response

        processor = CatFactProcessor()

        with self.assertRaisesRegex(ApiError, "Ошибка при обработке ответа"):
            processor.get_fact()

        self.assertEqual(processor.last_fact, "")

    @patch("cat_fact.requests.get")
    def test_get_fact_missing_key(self, mock_get):
        """Отрицательный тест: отсутствие ключа fact в ответе"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"wrong_key": "value"}
        mock_get.return_value = mock_response

        processor = CatFactProcessor()

        with self.assertRaisesRegex(ApiError, "Ошибка при обработке ответа"):
            processor.get_fact()

        self.assertEqual(processor.last_fact, "")

    # ------------------------------------------------------------------------

    # get_fact_analysis

    def test_analysis_empty_fact(self):
        """Отрицательный тест: анализ при отсутствии факта"""
        processor = CatFactProcessor()
        result = processor.get_fact_analysis()

        self.assertEqual(result, {"length": 0, "letter_frequencies": {}})

    def test_analysis_normal_case(self):
        """Позитивный тест: анализ обычного факта"""
        processor = CatFactProcessor()
        processor.last_fact = "Cats have 32 muscles in each ear"

        result = processor.get_fact_analysis()

        self.assertEqual(result["length"], 30)
        self.assertEqual(result["letter_frequencies"]["c"], 2)
        self.assertEqual(result["letter_frequencies"][" "], 6)

    # ------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()
