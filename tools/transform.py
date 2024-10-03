import os
import re
import argparse
from pathlib import Path
from src import structure


def main():
    parser = argparse.ArgumentParser(
        description='Convert a CA/Browser Forum RFC 3647 document into small documents structured by section.')
    parser.add_argument('document', type=str, help='e.g., ../docs/BR.md')
    parser.add_argument('-a', '--abbreviation', type=str,
                        help='abbreviation used in filenames')
    parser.add_argument('-d', '--depth', default=4, type=int,
                        help='only create directories for N levels')
    parser.add_argument('-o', '--output', default='../structured/', type=str,
                        help='output directory')
    parser.add_argument('-t', '--truncate', default=35, type=int,
                        help='truncate the tile at N')
    args = parser.parse_args()

    # Long titles can exceed the max path length, using these settings you
    # can control the title truncation and until how many levels deep we
    # create directories.
    depth = args.depth
    truncate = args.truncate
    abbreviation = os.path.splitext(os.path.basename(args.document))[0]

    if args.abbreviation != None:
        abbreviation = args.abbreviation

    os.chdir(args.output)
    output = os.getcwd()
    os.makedirs("./APPENDIX", exist_ok=True)

    # Read existing directory structure and map to sections to
    # avoid name mismatches.
    sections = {}
    p = Path('../structured')
    objects = sorted(p.rglob("*"))
    for o in objects:
        if o.is_dir():
            section = structure.get_section(o)
            sections[section] = o.resolve()

    # Parse the given document
    with open(args.document, 'r', encoding="utf-8") as f:
        file = open(os.fsencode("000_{}.md".format(
            abbreviation)), "w", encoding="utf-8")

        appendix = ""
        for line in f:
            if line.startswith("#"):
                file.close()

                # Remove duplicate spaces, special characters and section numbers
                t = re.sub('\s+', ' ', line).split(" ", 2)
                title = re.sub('[^a-zA-Z0-9\- ]', ' ', t[2].strip())
                title = re.sub('[0-9]{3}', '', title)
                title = re.sub('\s+', ' ', title)
                title = (title[:truncate]) if len(title) > truncate else title
                title = title.strip(".")
                title = title.strip("-")
                title = title.strip()

                section = t[1].strip(".").upper()

                # Some titles include a duplicate space, remove them as this has no function
                line = re.sub('\s+', ' ', line).strip() + "\n"

                if appendix != "":
                    section = "{}.{}".format(appendix, section)

                n = section.split(".")

                if section.__contains__("APPENDIX"):
                    os.chdir("{}/APPENDIX".format(output))

                    regex = r"APPENDIX\s+([A-Z])"
                    match = re.search(regex, line.upper())
                    if match:
                        appendix = match.group(1)
                        section = appendix
                        n = appendix.split(".")
                        title = re.sub('^[A-Z]{1}\s+', '', title)

                elif section in sections:
                    os.chdir(sections[section])

                    # open file for writing
                    file = open(os.fsencode("000_{}_{}.md".format(
                        abbreviation, title)), "w", encoding="utf-8")
                    file.write(line)
                    continue

                elif section.count('.') == 0:
                    os.chdir(output)

                elif section.count('.') >= depth:
                    # change to directory of X sections deep
                    os.chdir(sections[".".join(n[:depth])])

                    # add a prefix to each file, indicating the section if we create
                    # multiple sections in one directory
                    si = "-".join([str(item).zfill(3) for item in n[depth:]])
                    file = open(os.fsencode("{}_000_{}_{}.md".format(
                        si, abbreviation, title)), "w", encoding="utf-8")
                    file.write(line)
                    continue

                elif ".".join(n[:-1]) in sections:
                    os.chdir(sections[".".join(n[:-1])])

                elif ".".join(n[:-2]) in sections:
                    # this looks two levels back, required for the appendix that skips one level
                    os.chdir(sections[".".join(n[:-2])])

                else:
                    print(
                        "error, don't know where I'm - {} | {} -- {}\n".format(section, appendix, title))
                    print(sections)
                    exit

                prefix = n[-1].zfill(3)
                dirname = "./{} {}".format(prefix, title)

                try:
                    os.makedirs(dirname, exist_ok=True)
                    os.chdir(dirname)
                except Exception as e:
                    print("failed to create directory: {} in {}\n{}\n".format(
                        dirname, os.getcwd(), e))

                sections[section] = os.getcwd()

                print("{} ## {} -- {} :: {} ** {}".format(
                    n[-1].zfill(3), section, title, dirname, section.__len__()))

                # open file for writing
                file = open(os.fsencode("000_{}_{}.md".format(
                    abbreviation, title)), "w", encoding="utf-8")

                # the appendixes seem to be document specific for now
                # if appendix != "":
                #     file.write(
                #         "---\ntargets:\n    included:\n        - {}\n---\n\n".format(abbreviation))

                file.write(line)

            elif line.strip().startswith("No stipulation"):
                # do not include no stipulation statements, these can automatically be generated
                # if none of the layers stipulate any requirements
                continue

            else:
                file.write(line)


if __name__ == '__main__':
    main()
