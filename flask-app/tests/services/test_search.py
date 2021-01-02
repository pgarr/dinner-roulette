from unittest.mock import Mock

from app.services.search import search_recipe


def test_search_recipe_convert_strings_to_ints(test_client, database):
    from app.models.mixins import search
    search.query_index = Mock(return_value=([1], 2))
    search_recipe('test', '1', '1')
    search.query_index.assert_called_once_with('recipe', 'test', 1, 1)
