#!/usr/bin/python3

import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ElementTree
import subprocess

soft_list_extra_command = {
    "32x": "--force_driver=32x --extra=\"-artpath / -snapsize 320x224\"",
    "a2600": "--force_driver=a2600 --extra=\"-artpath /\"",
    "a7800": "--force_driver=a7800 --extra=\"-artpath /\"",
    "a800": "--force_driver=a800 --extra=\"-artpath /\"",
    "a800_flop": "--force_driver=a800 --extra=\"-artpath /\"",
    "amigaaga_flop": "--force_driver=a1200 --extra=\"-artpath /\"",
    "amigaecs_flop": "--force_driver=a600 --extra=\"-artpath /\"",
    "amigaocs_flop": "--force_driver=a500 --extra=\"-artpath /\"",
    "amiga_workbench": "--force_driver=a400030n --extra=\"-artpath /\"",
    "apple2_flop_clcracked": "--force_driver=apple2e --extra=\"-artpath /\"",
    "apple2_flop_misc": "--force_driver=apple2e --extra=\"-artpath /\"",
    "apple2_flop_orig": "--force_driver=apple2e --extra=\"-artpath /\"",
    "apple2gs_flop_orig": "--force_driver=apple2gs --extra=\"-artpath /\"",
    "apple2gs_flop_clcracked": "--force_driver=apple2gs --extra=\"-artpath /\"",
    "bbc_rom": "--force_driver=bbcb --extra=\"-artpath /\"",
    "c64_cass": "--force_driver=c64 --extra=\"-artpath /\"",
    "c64_cart": "--force_driver=c64 --extra=\"-artpath /\"",
    "casloopy": "--force_driver=casloopy --extra=\"-artpath /\"",
    "cdi": "--force_driver=cdimono1 --extra=\"-artpath /\"",
    "cgenie_cass": "--force_driver=cgenie --extra=\"-artpath / -snapsize 768x512\"",
    "coleco": "--force_driver=coleco --extra=\"-artpath / \"",
    "coleco_homebrew": "--force_driver=coleco --extra=\"-artpath / \"",
    "cpc_cass": "--force_driver=cpc6128 --extra=\"-artpath / -snapsize 704x288\"",  # -snapsize 704x432 ?
    "cpc_flop": "--force_driver=cpc6128 --extra=\"-artpath / -snapsize 704x288\"",
    "ctvboy": "--force_driver=ctvboy --extra=\"-artpath /\"",
    "ekara_cart": "--force_driver=ekara --extra=\"-artpath /\"",
    "ekara_japan": "--force_driver=epitch --extra=\"-artpath /\"",
    "famibox": "--force_driver=nes --extra=\"-artpath /\"",
    "famicom_flop": "--force_driver=fds --extra=\"-artpath /\"",
    "fmtowns_cd": "--force_driver=fmtowns --allow_preliminary --extra=\"-artpath / -snapsize 768x512\"",
    "fmtowns_flop_orig": "--force_driver=fmtowns --allow_preliminary --extra=\"-artpath / -snapsize 768x512\"",
    "gamate": "--force_driver=gamate",
    "gameboy": "--force_driver=gameboy",
    "gamecom": "--force_driver=gamecom",
    "gameking": "--force_driver=gameking",
    "gameking3": "--force_driver=gamekin3",
    "gba": "--force_driver=gba",
    "gbcolor": "--force_driver=gbcolor",
    "gx4000": "--force_driver=gx4000 --extra=\"-artpath / -snapsize 704x288\"",
    "hp98x6_rom": "--force_driver=hp9816a --extra=\"-ramsize 1M \"",
    "ibm5150": "--force_driver=ct486 --extra=\"-artpath /\"",
    "ibm5170": "--force_driver=ct486 --extra=\"-artpath /\"",
    "ibm5170_cdrom": "--force_driver=ct486 --extra=\"-artpath /\"",
    "lynx": "--force_driver=lynx",
    "mac_cdrom": "--force_driver=macqd800 --extra=\"-hard mac761 -ramsize 16M -video opengl\"",
    "mac_flop_clcracked": "--force_driver=mac512k",
    "mac_flop_orig": "--force_driver=mac512k",
    "megadriv": "--force_driver=megadriv --extra=\"-snapsize 320x224 -video opengl -artpath /\"",
    "megacdj": "--force_driver=megacdj --extra=\"-snapsize 320x224 -artpath /\"",
    "mo5_cass": "--force_driver=mo5 --extra=\"-artpath /\"",
    "monon_color": "--force_driver=mononcol --extra=\"-artpath /\"",
    "msx1_cass": "--force_driver=mlf80 --extra=\"-artpath /\"",
    "msx1_cart": "--force_driver=mlf80 --extra=\"-artpath /\"",
    "msx1_flop": "--force_driver=hbf1xv --extra=\"-artpath /\"",
    "msx1_flop_525": "--force_driver=\"mlf80 -cart1 mfd001\" --extra=\" -artpath /\"",
    "msx1_softcard": "--force_driver=\"mlf80 -cartslot1 softcard\" --extra=\" -artpath /\"",
    "msx2_cart": "--force_driver=fsa1fx --extra=\"-artpath /\"",
    "msx2_flop": "--force_driver=hbf700p --extra=\"-artpath /\"",
    "n64": "--force_driver=n64",
    "neogeo": "--force_driver=neogeo --extra=\"-artpath /\"",
    "nes": "--force_driver=nes --extra=\"-artpath /\"",
    "ngpc": "--force_driver=ngpc --extra=\"-snapsize 904x568\"",
    "oric1_cass": "--force_driver=oric1 ",
    "pc6001_cart": "--force_driver=pc6001 ",
    "pc8801_flop": "--force_driver=pc8801mk2sr --extra=\"-artpath /\"",
    "pc98": "--force_driver=pc9821ce2 --extra=\"-ramsize 14M -artpath /\" --allow_preliminary",
    "pc98_cd": "--force_driver=pc9821ce2 --extra=\"-ramsize 14M -artpath /\" --allow_preliminary",
    "pda600": "--force_driver=pda600 --allow_preliminary",
    "psion_ssd": "--force_driver=psion3a --allow_preliminary",
    "psx": "--force_driver=psj --allow_preliminary",
    "pv1000": "--force_driver=pv1000 --allow_preliminary",
    "pv2000": "--force_driver=pv2000 --allow_preliminary",
    "rx78_cass": "--force_driver=rx78 --allow_preliminary --extra=\"-artpath /\"",
    "rx78_cart": "--force_driver=rx78 --allow_preliminary --extra=\"-artpath /\"",
    "samcoupe_flop": "--force_driver=samcoupe",
    "sc3000_cass": "--force_driver=sc3000 --extra=\"-cart basic3e\"",
    "scv": "--force_driver=scv",
    "sega_beena_cart": "--force_driver=beena",
    "segaai": "--force_driver=segaai --extra=\"-artpath /\"",
    "segacd": "--force_driver=segacd --extra=\"-snapsize 320x224 -artpath /\"",
    "sms": "--force_driver=sms --extra=\"-artpath /\"",
    "snes": "--force_driver=snes --extra=\"-artpath /\"",
    "spectrum_cass": "--force_driver=spec128 --extra=\"-artpath /\"",
    "specpls3_flop": "--force_driver=sp3e8bit --extra=\"-artpath /\"",
    "spectrum_betadisc_flop": "--force_driver=pent1024 --extra=\"-artpath /\"",
    "supracan": "--force_driver=supracan ",
    "svision": "--force_driver=svision ",
    "vic10": "--force_driver=c64 --extra=\"-artpath /\"",
    "vidbrain": "--force_driver=vidbrain --extra=\"-artpath /\"",
    "videoart": "--force_driver=videoart --extra=\"-artpath /\"",
    "videopac": "--force_driver=odyssey2 --extra=\"-artpath /\"",
    "vsmile_cart": "--force_driver=vsmile --extra=\"-artpath /\"",
    "x68k_flop": "--force_driver=x68000 --extra=\"-artpath /\"",
    "zx81_cass": "--force_driver=zx81 --extra=\"-artpath /\"",
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


def get_bugs(page):
    result = []
    line = re.split(r'\n', page)
    for l in line:
        result_line = {}
        line_split = re.split(r': ', l)

        # Extract bug ID
        result_line["bug"] = line_split[0][2:]

        # Extract type of bug and driver
        type_and_driver = re.split(r'] ', line_split[1])
        result_line["type"] = type_and_driver[0][1:]
        result_line["driver"] = type_and_driver[1].replace(') ', ' - ').replace('(', '')

        # Extract comment
        if len(line_split) > 2:
            result_line["comment"] = line_split[2]
        else:
            result_line["comment"] = ""

        result.append(result_line)

    return result


def print_bug(result):
    index = 2
    for r in result:
        file_name = "{0:03}".format(index)
        print(file_name)
        print("https://mametesters.org/view.php?id=" + r["bug"] + "\n")

        with open(file_name + ".srt", 'w') as f:
            f.write("1\n")
            f.write("00:00:00,000 --> 00:00:10,000\n")
            f.write(r["comment"] + "\n")
            f.write("<b>" + r["driver"] + "</b>\n")
        with open(file_name + ".srt2", 'w') as f:
            f.write("1\n")
            f.write("00:00:00,000 --> 00:00:10,000\n")
            f.write("<b>" + r["type"] + "</b>\n")

        index = index + 2


def get_description_generic(section):
    # Remove any number of space at beginning of line
    d = re.sub("^ *", "", section, flags=re.M | re.UNICODE)

    # replace all new line not preceded by ']' by a space
    dd = re.sub(r'(?<!\])\n', ' ', d)

    # Every line should be "complete name [xxxx]"

    # remove [redump.org]
    d = re.sub(r' \[[^\]]+\]', '', dd)

    # Every line should be "complete name"

    desc_list = re.split(r'\n', d)
    # split with ", " ignoring ',' placed in parentheses
    # desc_list = re.split(r', (?!(?:[^(]*\([^)]*\))*[^()]*\))', d)

    escaped_list = []
    for d in desc_list:
        # escape for regex
        regex_escaped = re.escape(d)
        # escape for bash
        e = regex_escaped.replace('!', r'\!')
        f = e.replace("'", r"\'")
        escaped_list.append(f.replace(r'"', '\\\"'))

    print("\n\nFound", str(len(desc_list)), "entries")
    return escaped_list, desc_list


def get_description_softlist(section):
    # remove space at the beginning of line
    ddd = re.sub("^  ", "", section, flags=re.M)

    e = ddd.replace(']\n', '], ').replace(',\n', ', ').replace('\n', '').replace(',,', ',')
    # .replace('  ','').replace('   ', ' ')

    # remove [redump.org]
    dd = re.sub(r' \[[^\]]+\]', '', e)
    d = re.sub(r'\[[^\]]+\]', '', dd)

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
        e = regex_escaped.replace('!', r'\!')
        f = e.replace("'", r"\'")
        escaped_list.append(f.replace('"', '\\\"'))

    print("\nFound", str(len(desc_list)), "entries\n")
    return escaped_list, desc_list


def print_generic_command(title, escaped_list):
    print(
        "./randomame.py --title_text=\"     MAME " + version + "      ::: " + title + " :::                       " + str(
            len(escaped_list)) + " software                       \" --title_bg=\"/media/4To/emu/mame/mame.png\" --description=\"" + ":::".join(
            escaped_list) + "\" --all --allow_preliminary --timeout=60000 --window=1 --linear --quit --loose_search " +
        sys.argv[2] + " mame")


def print_softlist_command(title, softlist_name, escaped_list):
    global softlist_xml

    long_name = None

    for list in softlist_xml:
        if list.attrib['name'] == softlist_name:
            long_name = list.attrib['description']

    if long_name is None:
        print("**************************************")
        print("**************************************")
        print("Can't find", softlist_name, "softlist")
        print("**************************************")
        print("**************************************")
        return

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


p = get_whats_new_page(sys.argv[1]).decode("utf-8")
# page = unicodedata.normalize("NFKD", p)
# page = unicodedata.normalize("NFC", p)
# page = unicodedata.normalize("NFD", p)
page = unicodedata.normalize("NFKC", p)

version = page[2] + page[3] + page[4]

parse_soft_list()

generic_section = [
    "\nNew working systems\n-------------------\n", "\nNew working clones\n------------------\n",
    "\nSystems promoted to working\n---------------------------\n",
    "\nClones promoted to working\n--------------------------\n",
    "\nNew systems marked not working\n------------------------------\n",
    "\nNew clones marked not working\n-----------------------------\n"]

for section in generic_section:
    section_page = get_section(page, section)
    if section_page is not None:
        escaped_list, desc_list = get_description_generic(section_page)
        print(section)
        title = re.split("\n", section)
        print_generic_command(title[1], escaped_list)

softlist_section = ["\nNew working software list items\n-------------------------------",
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

bug_section = ["\nMAME Testers bugs fixed\n-----------------------\n"]

for section in bug_section:
    section_page = get_section(page, section)
    if section_page is not None:
        result = get_bugs(section_page)
        print_bug(result)
    # if section_page is not None:
    #    escaped_list, desc_list = get_description_generic(section_page)
    #    print(section)
    #    title = re.split("\n", section)
    #    print_generic_command(title[1], escaped_list)
