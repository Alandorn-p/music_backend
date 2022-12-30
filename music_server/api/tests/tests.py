from django.test import Client, TestCase
from json import loads


class TestResponse(TestCase):
    def test_get(self):
        # test for correct json structure
        c = Client()
        response = c.get('/search/liveandlearn/')
        assert response.status_code == 200
        json_t = loads(response.content)
        # has results key
        lst = json_t.get('results')
        # If None, it doesnt exist
        assert lst
        # access first element
        first = lst[0]
        attr_checked = ['title', 'author',
                        'watch_url', 'length', 'publish_date']
        for x in attr_checked:
            assert x in first
