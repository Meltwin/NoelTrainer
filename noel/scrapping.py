from typing import List
from requests import get
from xml.dom.minidom import parseString, Element
from .types import Film, Channel, TVProgram

def __get_tag_value(node:Element) -> str:
    if len(node.childNodes) > 0:
        return node.childNodes[0].nodeValue
    return node.nodeValue

def __get_associated_channel(id, channels: List[Channel]) -> Channel:
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
    else: return node.nodeValue

def __parseProgram(node: Element, channels: List[Channel]) -> Film:
    film = Film()

    # Parse attributes
    film.start = node.getAttribute("start")
    film.stop = node.getAttribute("stop")
    film.channel = __get_associated_channel(node.getAttribute("channel"), channels)

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
                film.length = __parse_length(__get_tag_value(child), child.getAttribute("units"))
            case "icon":
                film.icon = child.getAttribute("src")
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
    channel.id = node.getAttribute("id")

    # Parse childs
    for child in node.childNodes:
        if type(child) is not Element:
            continue
        elif child.tagName == "display-name":
            channel.name = __get_tag_value(child)
        elif child.tagName == "icon":
            channel.icon = child.getAttribute("src")
    return channel


def __parseTV(node: Element) -> TVProgram:
    program = TVProgram()
    for child in node.childNodes:
        if type(child) is not Element:
            continue
        elif child.tagName == "channel":
            program.channels.append(__parseChannel(child))
        elif child.tagName == "programme":
            program.films.append(__parseProgram(child, program.channels))
    return program

def parse_xml_distant(xml_url: str):
    data = get(xml_url)
    data = parseString(data.content)
    program = None
    for node in data.childNodes:
        if type(node) is Element:
            program = __parseTV(node)
            break
    return program