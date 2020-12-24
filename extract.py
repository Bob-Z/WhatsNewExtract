#!/usr/bin/python3

import re
import sys

f = open(sys.argv[1], "r")
data = f.read()

e = data.replace(']\n', '], ').replace(',\n', ', ').replace('\n', '').replace(',,', ',').replace('  ', ' ').replace('   ', ' ')

# remove [redump.org]
d = re.sub(' \[[^\]]+\]', '', e)

# remove last ', '
c = desc_list = d[:-2]

# split with ", " ignoring ',' placed in parenthesis
# ( re.sub(r', (?!(?:[^(]*\([^)]*\))*[^()]*\))', ':::', d))
desc_list = re.split(r', (?!(?:[^(]*\([^)]*\))*[^()]*\))', c)

escaped_list = []
for d in desc_list:
    # escape for regex
    regex_escaped = re.escape(d)
    # escpae for bach
    e = regex_escaped.replace('!', '\!')
    escaped_list.append(e.replace('"', '\\\"'))

print(":::".join(escaped_list))
