from django.http import FileResponse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed
from . import music_mod
import urllib.parse
from os.path import basename
from django.views.decorators.csrf import csrf_exempt
import json

MUSIC_PATH = 'music_files'
FILE = 'test_file.mp3'


def send_file(request, path):
    # return FileResponse(open(TEST_FILE, 'rb'))
    return read_file(path)


def read_file(path):
    with open(path, 'rb') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='application/mpeg')
    response['Content-Disposition'] = f'attachment; filename="{basename(path)}"'

    return response


def search_results(request, query):
    query = urllib.parse.unquote_plus(query)
    data = music_mod.search(query)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def download_file(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))
    data = json.loads(request.body)
    url = data.get('url')
    if not url:
        return HttpResponseBadRequest("URL key not provided in body")
    try:
        path = music_mod.download(url, MUSIC_PATH)
        return read_file(path)
    except music_mod.InvalidURLError:
        return HttpResponseBadRequest("Not a valid youtube URL")
