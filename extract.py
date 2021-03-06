#!/usr/bin/python3

import re
import sys
import unicodedata
import urllib.request


def get_whats_new_page(version):
    url = "https://www.mamedev.org/releases/whatsnew_0" + version + ".txt"
    return urllib.request.urlopen(url).read()


def get_section(page, section):
    a = page.split(section)
    if len(a) == 1:
        return None
    b = a[1]
    c = b.split("\n\n")
    d = c[0]
    return d


def get_description_generic(section):
    # Remove any number of space at beginning of line
    d = re.sub("^ *", "", section, flags=re.M)

    # replace all new line not preceded by ']' by a space
    dd = re.sub(r'(?<!\])\n', ' ', d)

    # Every line should be "complete name [xxxx]"

    # remove [redump.org]
    d = re.sub(' \[[^\]]+\]', '', dd)

    # Every line should be "complete name"

    desc_list = re.split(r'\n', d)
    # split with ", " ignoring ',' placed in parenthesis
    # desc_list = re.split(r', (?!(?:[^(]*\([^)]*\))*[^()]*\))', d)

    escaped_list = []
    for d in desc_list:
        # escape for regex
        regex_escaped = re.escape(d)
        # escpae for bash
        e = regex_escaped.replace('!', '\!')
        escaped_list.append(e.replace('"', '\\\"'))

    print("\n\nFound", str(len(desc_list)), "entries")
    return escaped_list, desc_list


def get_description_softlist(section):
    # remove space at the beginning of line
    ddd = re.sub("^  ", "", section, flags=re.M)

    e = ddd.replace(']\n', '], ').replace(',\n', ', ').replace('\n', '').replace(',,', ',')
    # .replace('  ','').replace('   ', ' ')

    # remove [redump.org]
    dd = re.sub(' \[[^\]]+\]', '', e)
    d = re.sub('\[[^\]]+\]', '', dd)

    # remove last ', '
    # c = desc_list = d[:-2]

    # split with ", " ignoring ',' placed in parenthesis
    # ( re.sub(r', (?!(?:[^(]*\([^)]*\))*[^()]*\))', ':::', d))
    desc_list = re.split(r', (?!(?:[^(]*\([^)]*\))*[^()]*\))', d)

    escaped_list = []
    for d in desc_list:
        # escape for regex
        regex_escaped = re.escape(d)
        # escape for bash
        e = regex_escaped.replace('!', '\!')
        escaped_list.append(e.replace('"', '\\\"'))

    print("\nFound", str(len(desc_list)), "entries\n")
    return escaped_list, desc_list


def print_generic_command(title, escaped_list):
    print(
        "./randomame.py --title_text=\"     MAME  " + version + "     :::" + title + "\" --title_bg=\"/media/4To/emu/mame/mame.png\" --description=\"" + ":::".join(
            escaped_list) + "\" --all --allow_preliminary --timeout=60000 --window=1 --linear --quit --loose_search /media/4To/emu/mame/mame/mame")


def print_softlist_command(title, softlist_name, escaped_list):
    print(
        "./randomame.py --title_text=\"     MAME  " + version + "     :::" + title + ":::" + softlist_name + "\" --title_bg=\"/media/4To/emu/mame/mame.png\" --selected_softlist=" + softlist_name + " --allow_not_supported --description=\"" + ":::".join(
            escaped_list) + "\" --timeout=60000 --window=1 --linear --quit /media/4To/emu/mame/mame/mame")


def print_music(escaped_list, desc_list):
    index = 0
    for e in escaped_list:
        filename = desc_list[index].replace('/', '\\')
        print(
            "./randomame.py --music --allow_not_supported --description=\"" + e +
            "\" --timeout=120 --window=1 --linear --quit --start_command=\"./start_script.sh\" --end_command=\"./end_script.sh \'" + filename + "\'\" /media/4To/emu/mame/mame/mame\n")
        index = index + 1


generic_section = ["\nNew working machines\n--------------------\n", "\nNew working clones\n------------------\n",
                   "\nMachines promoted to working\n----------------------------\n",
                   "\nClones promoted to working\n--------------------------\n"]

p = get_whats_new_page(sys.argv[1]).decode("utf-8")
page = unicodedata.normalize("NFKD", p)

version = page[2] + page[3] + page[4]

for section in generic_section:
    section_page = get_section(page, section)
    if section_page is not None:
        escaped_list, desc_list = get_description_generic(section_page)
        print(section)
        title = re.split("\n", section)
        print_generic_command(title[1], escaped_list)

softlist_section = ["\nNew working software list additions\n-----------------------------------",
                    "\nSoftware list items promoted to working\n---------------------------------------"]

for section in softlist_section:
    print(section)

    title_split = re.split("\n", section)
    title = title_split[1]

    section_page = get_section(page, section)
    if section_page is not None:
        s = re.split("(\n[a-z])", section_page)
        softlist_section = []
        for i in range(1, len(s), 2):
            softlist_section.append(s[i].replace('\n', '') + s[i + 1])

        for s in softlist_section:
            softlist = re.split("(^.*?: |^.*:\n)", s)
            softlist_name = softlist[1].replace(': ', '').replace(':\n', '')
            print("\n" + softlist_name)

            escaped_list, desc_list = get_description_softlist(softlist[2])

            if softlist_name == "vgmplay":
                print_music(escaped_list, desc_list)
            else:
                print_softlist_command(title, softlist_name, escaped_list)
