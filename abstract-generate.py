from xml.dom import minidom

# read each line, search for lines starting with <abstract> and whose text doesn't start with '|', as
# these are not usable abstracts

with open("wiki-abstract.xml", "r") as fin:
    with open("wiki-abstracts-only.txt", "w") as fout:
        for line in fin:
            if (line.startswith("<abstract>")) and not(line.startswith("<abstract>|")):
                p = minidom.parseString(line)
                fout.write(p.getElementsByTagName('abstract')[0].firstChild.data)
                fout.write("\n")
