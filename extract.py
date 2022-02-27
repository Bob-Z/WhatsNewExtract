#!/usr/bin/python3

import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ElementTree
import subprocess

soft_list_extra_command = {
    "32x": "--force_driver=32x --extra=\"-artpath / -snapsize 320x224\"",
    "a800_flop": "--force_driver=a800 --extra=\"-artpath /\"",
    "apple2_flop_clcracked": "--force_driver=apple2e --extra=\"-artpath /\"",
    "apple2_flop_orig": "--force_driver=apple2e --extra=\"-artpath /\"",
    "apple2gs_flop_orig": "--force_driver=apple2gs --extra=\"-artpath /\"",
    "c64_cass": "--force_driver=c64 --extra=\"-artpath /\"",
    "cdi": "--force_driver=cdimono1 --extra=\"-artpath /\"",
    "cgenie_cass": "--force_driver=cgenie --extra=\"-artpath / -snapsize 768x512\"",
    "cpc_cass": "--force_driver=cpc6128 --extra=\"-artpath / -snapsize 704x288\"",  # -snapsize 704x432 ?
    "cpc_flop": "--force_driver=cpc6128 --extra=\"-artpath / -snapsize 704x288\"",
    "fmtowns_cd": "--force_driver=fmtowns --allow_preliminary --extra=\"-artpath / -snapsize 768x512\"",
    "fmtowns_flop_orig": "--force_driver=fmtowns --allow_preliminary --extra=\"-artpath / -snapsize 768x512\"",
    "gameboy": "--force_driver=gameboy",
    "gba": "--force_driver=gba",
    "gbcolor": "--force_driver=gbcolor",
    "ibm5150": "--force_driver=ct486 --extra=\"-artpath /\"",
    "ibm5170": "--force_driver=ct486 --extra=\"-artpath /\"",
    "ibm5170_cdrom": "--force_driver=ct486 --extra=\"-artpath /\"",
    "lynx": "--force_driver=lynx",
    "megadriv": "--force_driver=megadriv --extra=\"-snapsize 320x224 -artpath /\"",
    "nes": "--force_driver=nes --extra=\"-artpath /\"",
    "ngpc": "--force_driver=ngpc --extra=\"-snapsize 904x568\"",
    "pc98": "--force_driver=pc9821ce2 --extra=\"-ramsize 14M -artpath /\" --allow_preliminary",
    "rx78_cart": "--allow_preliminary --extra=\"-artpath /\"",
    "sms": "--force_driver=sms --extra=\"-artpath /\"",
    "snes": "--force_driver=snes --extra=\"-artpath /\"",
    "spectrum_cass": "--force_driver=spectrum --extra=\"-artpath /\"",
}

softlist_xml = None


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
    d = re.sub("^ *", "", section, flags=re.M | re.UNICODE)

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
        "./randomame.py --title_text=\"     MAME  " + version + "     ::: " + title + " :::                       " + str(
            len(escaped_list)) + " software                       \" --title_bg=\"/media/4To/emu/mame/mame.png\" --description=\"" + ":::".join(
            escaped_list) + "\" --all --allow_preliminary --timeout=60000 --window=1 --linear --quit --loose_search " +
        sys.argv[2] + " mame")


def print_softlist_command(title, softlist_name, escaped_list):
    global softlist_xml
    for list in softlist_xml:
        if list.attrib['name'] == softlist_name:
            long_name = list.attrib['description']

    if softlist_name in soft_list_extra_command:
        extra_command = soft_list_extra_command[softlist_name]
    else:
        extra_command = ""

    print(
        "./randomame.py --title_text=\"     MAME  " + version + "     ::: " + long_name + " ::: " + title + " :::                       " + str(
            len(escaped_list)) + " software                       \" --title_bg=\"/media/4To/emu/mame/mame.png\" --selected_softlist=" + softlist_name + " --allow_not_supported --description=\"" + ":::".join(
            escaped_list) + "\" --timeout=60000 --window=1 --linear --quit --loose_search " +
        extra_command + " " + sys.argv[2] + " mame")


def print_music(escaped_list, desc_list):
    index = 0
    for e in escaped_list:
        f = desc_list[index].replace('/', '\\')
        filename = f.replace('\"', '\\\"')
        print(
            "./randomame.py --music --allow_not_supported --description=\"" + e +
            "\" --timeout=120 --window=1 --linear --quit --start_command=\"./start_script.sh\" --final_command=\"./final_script.sh \\\"" + filename + "\\\"\" mame\n")
        index = index + 1


def get_version():
    args = ["mame"]
    args += ['-version']

    out = subprocess.run(args, capture_output=True)
    return out.stdout.decode('utf-8')


def get_softlist_file_name():
    mame_version = get_version()
    print("MAME verion:", mame_version)
    return "/tmp/" + "softlist_" + mame_version + ".txt"


def parse_soft_list():
    print("Parsing software list XML")
    tree = ElementTree.parse(get_softlist_file_name())
    print("")
    print("")

    global softlist_xml
    softlist_xml = tree.getroot()


generic_section = ["\nNew working machines\n--------------------\n", "\nNew working clones\n------------------\n",
                   "\nMachines promoted to working\n----------------------------\n",
                   "\nClones promoted to working\n--------------------------\n",
                   "\nNew machines marked as NOT_WORKING\n----------------------------------\n",
                   "\nNew clones marked as NOT_WORKING\n--------------------------------\n"]

p = get_whats_new_page(sys.argv[1]).decode("utf-8")
page = unicodedata.normalize("NFKD", p)

version = page[2] + page[3] + page[4]

parse_soft_list()

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
        s = re.split("(\n[a-z0-9])", section_page)
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
