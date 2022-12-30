import pytube
import os
import sys
from json import dumps
from django.utils.text import slugify

ATTRIBUTES = ['title', 'author', 'watch_url', 'length', 'publish_date']
MAX_ELEMENTS = 10

# Code to disable print, since search is bugged?

InvalidURLError = pytube.exceptions.RegexMatchError


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def search(query):
    """Returns a json 
    Precondition: query is a string
    """
    with HiddenPrints():
        s = pytube.Search(query)
        acc = []
        for ele in s.results[:MAX_ELEMENTS]:
            dict_t = {attr: getattr(ele, attr) for attr in ATTRIBUTES}
            # change publish_date to string so its serializable
            dict_t['publish_date'] = dict_t['publish_date'].strftime(
                "%b %d, %Y")
            acc.append(dict_t)
        json_dict = {'results': acc}
        # ascii to False so
        return dumps(json_dict, ensure_ascii=False)


def name_converter(str):
    from django.utils.text import slugify
    temp = slugify(str, allow_unicode=True)
    return temp.replace('-', ' ')


def download(url, path, filename=None):
    """ Downloads a youtube video from `url` in the given `path` to an mp3.
    Returns the path to the downloaded file
    Precondition: url is a string, the url of the video that is downloaded
    Precondition: path is a string, relative path that the video is saved
    Precondition: filename (Optional) is a string to name the file (NOT including extension)
    """
    link_in = url
    yt = pytube.YouTube(link_in)
    if not filename:
        filename = name_converter(yt.title)
    # check that file doesnt exist already
    file_exist_path = f'{path}\{filename}.mp3'
    if os.path.exists(file_exist_path):
        return file_exist_path
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=path, filename=f'{filename}.mp3')
    return out_file
    # print(type(out_file))
    # base, ext = os.path.splitext(out_file)
    # new_file = base+'.mp3'
    # os.rename(out_file, new_file)
    # return new_file
# while True:
#     link_in = input("enter URL: ")
#     if link_in in ['q', 'quit', 'exit']:
#         break
#     if not os.path.exists(filepath):
#         os.mkdir(filepath)
#     yt = YouTube(str(link_in))
#     dest = filepath
#     video = yt.streams.filter(only_audio=True).first()
#     out_file = video.download(output_path=dest)
#     if not mp4_true:
#         base, ext = os.path.splitext(out_file)
#         new_file = base+'.mp3'
#         os.rename(out_file, new_file)
#     print("success")
