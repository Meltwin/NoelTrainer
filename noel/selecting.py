from noel.types import Film, TVProgram
from typing import List, Tuple
from requests import get
from unidecode import unidecode

def __download_stop_words(url: str) -> List[str]:
    return [unidecode(w).lower() for w in get(url).content.decode("utf-8").split("\r\n")]

def __download_custom_stopwords(url: str) -> Tuple[List[str], List[str]]:
    try:
        data = get(url).json()
        return (data["stopwords"], data["blacklist"])
    except:
        return ([], [])

def __replace_ponctuation(value: str) -> str:
    value = value.replace(",", " ")
    value = value.replace(".", " ")
    value = value.replace(";", " ")
    value = value.replace(":", " ")
    value = value.replace("!", " ")
    value = value.replace("?", " ")
    value = value.replace("'", " ")
    return value

def __get_import_words_in_string(value: str, stopwords: List[str]) -> List[str]:
    words = __replace_ponctuation(value).split(" ")
    out = []
    for w in words:
        assert(type(w) is str)
        if len(w) <= 2:
            continue
        n_w = unidecode(w).lower()
        if n_w not in stopwords:
            out.append(n_w)
    return out

def __get_important_words(film: Film, stopwords: List[str]) -> List[str]:
    out = []
    if film.title != None:
        out.extend(__get_import_words_in_string(film.title, stopwords))
    if film.subtitle != None:
        out.extend(__get_import_words_in_string(film.subtitle, stopwords))
    if film.desc != None:
        out.extend(__get_import_words_in_string(film.desc, stopwords))
    return out


def select_programs(tv: TVProgram, stopword_url: str, custom_stopword_url: str) -> List[Film]:
    stopwords, blacklist = __download_custom_stopwords(custom_stopword_url)
    stopwords += __download_stop_words(stopword_url)
    film_filtered = []
    next = False
    for f in tv.films:
        words = __get_important_words(f, stopwords)
        for w in words:
            if w in blacklist:
                next = True
                break
        if next:
            next = False
            continue
        if "noel" in words:
            film_filtered.append(f)

    return film_filtered