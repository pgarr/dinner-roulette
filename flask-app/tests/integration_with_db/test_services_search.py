from unittest.mock import Mock

from app.services import search_recipe
from tests.base_test import TestAppSetUp


class TestServices(TestAppSetUp):
    def test_search_recipe_called_with_strings(self):
        from app import models
        models.query_index = Mock(return_value=([1], 2))
        search_recipe('test', '1', '1')
        models.query_index.assert_called_once_with('recipe', 'test', 1, 1)
