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
    b = a[1]
    c = b.split("\n\n")
    d = c[0]
    return d


def get_description(section):
    e = section.replace(']\n', '], ').replace(',\n', ', ').replace('\n', '').replace(',,', ',').replace('  ',
                                                                                                        '').replace(
        '   ', ' ')

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
        # escpae for bach
        e = regex_escaped.replace('!', '\!')
        escaped_list.append(e.replace('"', '\\\"'))

    print("Found", str(len(desc_list)), "entry")
    return ":::".join(escaped_list)


def print_generic_command(description):
    print(
        "./randomame.py --description=\"" + description + "\" --all --allow_preliminary --timeout=60000 --window=1 --linear --quit --loose_search /media/4To/emu/mame/mame/mame")


def print_softlist_command(softlist_name, description):
    print(
        "./randomame.py --selected_softlist=" + softlist_name + " --allow_not_supported --description=\"" + description + "\" --timeout=60000 --window=1 --linear --quit /media/4To/emu/mame/mame/mame")


def print_music(description):
    for d in description.split(":::"):
        print(
            "./randomame.py --music --allow_not_supported --description=\"" + d + "\" --timeout=120 --window=1 --linear --quit --start_command=\"xdotool key ctrl+shift+alt+r\" --end_command=\"xdotool key ctrl+shift+alt+r\" /media/4To/emu/mame/mame/mame\n")


generic_section = ["\nNew working machines\n--------------------\n", "\nNew working clones\n------------------\n",
                   "\nMachines promoted to working\n----------------------------\n",
                   "\nClones promoted to working\n--------------------------\n"]

p = get_whats_new_page(sys.argv[1]).decode("utf-8")
page = unicodedata.normalize("NFKD", p)

for section in generic_section:
    section_page = get_section(page, section)
    section_description = get_description(section_page)
    print(section)
    print_generic_command(section_description)

softlist_section = ["\nNew working software list additions\n-----------------------------------",
                    "\nSoftware list items promoted to working\n---------------------------------------"]

for section in softlist_section:
    print(section)

    section_page = get_section(page, section)
    s = re.split("(\n[a-z])", section_page)
    softlist_section = []
    for i in range(1, len(s), 2):
        softlist_section.append(s[i].replace('\n', '') + s[i + 1])

    for s in softlist_section:
        softlist = re.split("(^.*?: |^.*:\n)", s)
        softlist_name = softlist[1].replace(': ', '').replace(':\n', '')
        print("\n" + softlist_name)

        softlist_description = get_description(softlist[2])

        if softlist_name == "vgmplay":
            print_music(softlist_description)
        else:
            print_softlist_command(softlist_name, softlist_description)
