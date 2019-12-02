from tests.base_test import TestAppSetUp


class TestSearchPaginatedAdapter(TestAppSetUp):

    def setUp(self):
        super(TestSearchPaginatedAdapter, self).setUp()
        from app.api.helper_fun import SearchAPIPaginatedAdapter
        self.adapter = SearchAPIPaginatedAdapter

    def test_pages_result_is_integer(self):
        adapter = self.adapter([], 1, 10, 30)
        self.assertEqual(3, adapter.pages)

    def test_pages_result_is_float_decimal_over_five(self):
        adapter = self.adapter([], 1, 10, 24)
        self.assertEqual(3, adapter.pages)

    def test_pages_result_is_float_decimal_under_five(self):
        adapter = self.adapter([], 1, 10, 26)
        self.assertEqual(3, adapter.pages)

    def test_has_next_false(self):
        adapter = self.adapter([], 3, 10, 24)
        self.assertFalse(adapter.has_next)

    def test_has_next_true(self):
        adapter = self.adapter([], 2, 10, 24)
        self.assertTrue(adapter.has_next)

    def test_has_prev_false(self):
        adapter = self.adapter([], 1, 10, 24)
        self.assertFalse(adapter.has_prev)

    def test_has_prev_true(self):
        adapter = self.adapter([], 2, 10, 24)
        self.assertTrue(adapter.has_prev)

    def test_pages_when_parameters_are_strings(self):
        adapter = self.adapter([], '2', '10', '24')
        self.assertEqual(3, adapter.pages)

    def test_has_next_when_parameters_are_strings(self):
        adapter = self.adapter([], '2', '10', '24')
        self.assertTrue(adapter.has_next)

    def test_has_prev_when_parameters_are_strings(self):
        adapter = self.adapter([], '2', '10', '24')
        self.assertTrue(adapter.has_prev)
