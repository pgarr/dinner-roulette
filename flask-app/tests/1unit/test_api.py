import pytest


class TestSearchPaginatedAdapter:

    @pytest.fixture
    def adapter_class(self, test_client):
        from app.api.helpers import SearchAPIPaginatedAdapter
        return SearchAPIPaginatedAdapter

    def test_pages_result_is_integer(self, adapter_class):
        adapter = adapter_class([], 1, 10, 30)
        assert 3 == adapter.pages

    def test_pages_result_is_float_decimal_over_five(self, adapter_class):
        adapter = adapter_class([], 1, 10, 24)
        assert 3 == adapter.pages

    def test_pages_result_is_float_decimal_under_five(self, adapter_class):
        adapter = adapter_class([], 1, 10, 26)
        assert 3 == adapter.pages

    def test_has_next_false(self, adapter_class):
        adapter = adapter_class([], 3, 10, 24)
        assert not adapter.has_next

    def test_has_next_true(self, adapter_class):
        adapter = adapter_class([], 2, 10, 24)
        assert adapter.has_next

    def test_has_prev_false(self, adapter_class):
        adapter = adapter_class([], 1, 10, 24)
        assert not adapter.has_prev

    def test_has_prev_true(self, adapter_class):
        adapter = adapter_class([], 2, 10, 24)
        assert adapter.has_prev

    def test_pages_when_parameters_are_strings(self, adapter_class):
        adapter = adapter_class([], '2', '10', '24')
        assert 3 == adapter.pages

    def test_has_next_when_parameters_are_strings(self, adapter_class):
        adapter = adapter_class([], '2', '10', '24')
        assert adapter.has_next

    def test_has_prev_when_parameters_are_strings(self, adapter_class):
        adapter = adapter_class([], '2', '10', '24')
        assert adapter.has_prev
