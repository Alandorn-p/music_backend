from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed
from . import music_mod
import urllib.parse
from os.path import basename
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Song
from django.views.decorators.http import require_POST, require_GET
from django.utils.text import slugify
from django.shortcuts import render

MUSIC_PATH = 'music_files'
FILE = 'test_file.mp3'


def send_file(request, path):
    # return FileResponse(open(TEST_FILE, 'rb'))
    return read_file(path)


def get_file(request, id):
    obj = Song.objects.get(video_id=id)
    response = HttpResponse(obj.contents, content_type='application/mpeg')
    #response['Content-Disposition'] = 'attachment; filename="test_file.mp3"'
    late = f"{slugify(obj.title)[:10]}.mp3"
    response['Content-Disposition'] = fr"attachment; filename={late}"
    #response['Content-Disposition'] = fr"attachment; filename*=UTF-8''{obj.title[:20]}.mp3"

    #response['Content-Disposition'] = f'attachment; filename="{obj.title[:10]}.mp3"'
    print(response['Content-Disposition'])
    return response


def read_file(path):
    with open(path, 'rb') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='application/mpeg'
                            )
    response['Content-Disposition'] = f'attachment; filename="{basename(path)}"'

    return response


@require_GET
def search_results(request, query):
    # turns 'the%20tomorrow%20with%20you' into 'the tomorrow with you'
    query = urllib.parse.unquote(query)
    data = music_mod.search(query)
    return HttpResponse(data, content_type='application/json')


def test_file(request):
    url = "https://www.youtube.com/watch?v=cvTb1VgABw8&ab_channel=J.O.E.VGM"
    path = music_mod.download(url, MUSIC_PATH)
    return read_file(path)


def http_response(song_obj, dup):
    json_dict = {'id': song_obj.video_id, 'title': song_obj.title, 'new': dup}
    response_contents = json.dumps(json_dict, ensure_ascii=False)
    return HttpResponse(response_contents, content_type='application/json')


@csrf_exempt
@require_POST
def download_file(request):
    # if request.method != 'POST':
    #     return HttpResponseNotAllowed(('POST',))
    if request.body == b'':
        print("here")
        return HttpResponseBadRequest("Error: Empty body")
    data = json.loads(request.body)
    url = data.get('url')
    if not url:
        print("kmlwdka")
        return HttpResponseBadRequest("URL key not provided in body")
    id = music_mod.get_id(url)
    query_set = Song.objects.filter(video_id=id)
    if query_set.exists():
        song_obj = query_set.first()
        return http_response(song_obj, False)

    try:
        obj = music_mod.download(url, MUSIC_PATH)
    except music_mod.InvalidURLError:
        print("flefmsef")
        return HttpResponseBadRequest("Not a valid youtube URL")
    print("success?")
    song_obj = Song(
        video_id=obj.id, contents=obj.contents, title=obj.title)
    song_obj.save()
    return http_response(song_obj, True)


def index(request):
    return render(request, 'index.html')
# example post body:
# {"url":"https://www.youtube.com/watch?v=W3Wf_ljb2-k&ab_channel=%E4%BA%8C%E4%B9%83%E6%98%AF%E5%A4%A9%E5%8D%83%E6%A3%98%E6%98%AF%E5%AE%87%E5%AE%99%21%21%21%E5%82%99%E7%94%A8%E9%A0%BB%E9%81%93"}
