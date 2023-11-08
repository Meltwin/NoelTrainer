from typing import List
from requests import get
from xml.dom.minidom import parseString, Element
from .types import Film, Channel, TVProgram

def __format_text(text: str) -> str:
    return text.strip("\r\n").strip().replace("\"", "\\\"")

def __get_tag_value(node:Element) -> str:
    if len(node.childNodes) > 0:
        return __format_text(node.childNodes[0].nodeValue)
    return __format_text(node.nodeValue)

def __get_associated_channel(id, channels: List[Channel]) -> Channel|None:
    for ch in channels:
        if ch.id == id:
            return ch
    return None

def __parse_length(value: str, unit: str) -> int:
    match unit:
        case "minutes":
            return int(value)
        case "hours":
            return int(value)*60
    return 0

def __get_audio(node: Element) -> str:
    if len(node.childNodes) > 0:
        return __get_tag_value(node.childNodes[0])
    else: return __format_text(node.nodeValue)

def __parseFilm(node: Element, channels: List[Channel]) -> Film:
    film = Film()

    # Parse attributes
    film.start = Film.make_date(__format_text(node.getAttribute("start")))
    film.stop = Film.make_date(__format_text(node.getAttribute("stop")))
    film.channel = __get_associated_channel(__format_text(node.getAttribute("channel")), channels)

    # Parse childs
    for child in node.childNodes:
        if type(child) is not Element:
            continue

        match child.tagName:
            case "title":
                film.title = __get_tag_value(child)
            case "sub-title":
                film.subtitle = __get_tag_value(child)
            case "desc":
                film.desc = __get_tag_value(child)
            case "length":
                film.length = __parse_length(__get_tag_value(child), __format_text(child.getAttribute("units")))
            case "icon":
                film.icon = __format_text(child.getAttribute("src"))
            case "audio":
                film.audio = __get_audio(child)
            case "rating":
                film.rating = __get_tag_value(child.childNodes[0])
            case "episode-num":
                film.episode_num = __get_tag_value(child)
            case "category":
                film.category = __get_tag_value(child)
            case "date":
                film.date = __get_tag_value(child)
    return film

def __parseChannel(node: Element) -> Channel:
    channel = Channel()

    # Parse attributes
    channel.id = __format_text(node.getAttribute("id"))

    # Parse childs
    for child in node.childNodes:
        if type(child) is not Element:
            continue
        elif child.tagName == "display-name":
            channel.name = __get_tag_value(child)
        elif child.tagName == "icon":
            channel.icon = __format_text(child.getAttribute("src"))
    return channel


def __parseTVProgram(node: Element) -> TVProgram:
    program = TVProgram()
    for child in node.childNodes:
        if type(child) is not Element:
            continue
        elif child.tagName == "channel":
            program.channels.append(__parseChannel(child))
        elif child.tagName == "programme":
            program.films.append(__parseFilm(child, program.channels))
    return program

def parse_xml_distant(xml_url: str) -> TVProgram:
    data = get(xml_url)
    data = parseString(data.content)
    program = TVProgram()
    for node in data.childNodes:
        if type(node) is Element:
            program = __parseTVProgram(node)
            break
    return program