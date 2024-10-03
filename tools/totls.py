import re
import os
import argparse
from pathlib import Path
from diff_match_patch import diff_match_patch
from src import structure

# Define document types as constants
output_folder = '../output/'
DOCUMENT_TYPES = sorted([os.path.splitext(file)[0] for file in os.listdir(output_folder) if file.endswith('.md')])

brtls = ['3.2.2.3','3.2.2.4','3.2.2.5','3.2.2.6','3.2.2.7','3.2.2.8','7.1.2']

def process_files(input_dir: Path, sections: dict[str, dict[str, Path]]) -> None:
    for f in sorted(input_dir.glob("*.md")):
        rt = re.search("\_([A-Z]{2,8})(_|\.md)", f.name)
        if rt is None:
            print("Invalid filename {}".format(f.name))
            continue  # Skip invalid filenames

        type = rt.group(1)
        section = structure.get_section(f)
        if type == 'BR':
            if "APPENDIX" in str(f):
                os.rename(f, str(f).replace('_BR_', '_TLS_'))
                print(f, section)
                type = 'TLS'
            else:
                for sec in brtls:
                    if section.startswith(sec):
                        os.rename(f, str(f).replace('_BR_', '_TLS_'))
                        print(f, section, sec)
                        type = 'TLS'

        if section not in sections:
            sections[section] = {'BR': [], type: []}
        else:
            # Ensure 'type' key is present in the dictionary
            sections[section].setdefault(type, [])

        sections[section][type].append(f)

    # Process all files in the subdirectories
    for subdir in sorted(input_dir.iterdir()):
        if subdir.is_dir():
            sections = process_files(subdir, sections)

    return sections

def find_added_sections(diffs):
    # Define the pattern for sections
    section_pattern = re.compile(r'^#+\s(\d+(\.\d+)*)')

    # Initialize lists to hold the added and deleted sections
    added_sections = []
    deleted_sections = []

    # Iterate over the diffs
    for op, data in diffs:
        # Check if the data matches the section pattern
        matches = section_pattern.findall(data)
        if matches:
            # Extract only the full section numbers
            full_matches = [match[0] for match in matches]
            # Check if the operation was an addition
            if op == 1:
                added_sections.extend(full_matches)
            # Check if the operation was a deletion
            elif op == -1:
                deleted_sections.extend(full_matches)

    # Iterate over the added sections
    for section in added_sections[:]:
        # Check if the section also appears in the deleted sections
        if section in deleted_sections:
            # If it does, remove it from the added sections list
            added_sections.remove(section)

    # Return the list of added sections
    return added_sections

def main():
    parser = argparse.ArgumentParser(
        description='Change Baseline Requirements files to TLS that should end up in the other documents')
    parser.add_argument('-in', '--input', default='../structured/', type=str,
                        help='input directory')
    args = parser.parse_args()

    sections = {}
    sections = process_files(Path(args.input), sections)

    # Writing a document diff between docs source and final build
    dmp = diff_match_patch()

    for dt in DOCUMENT_TYPES:
        try:
            with open('../docs/'+ dt + '.md', 'r', encoding='utf-8') as source_file:
                with open('../output/'+ dt + '.md', 'r', encoding='utf-8') as build_file:
                    source_content = source_file.read()
                    build_content = build_file.read()
                    if source_content != build_content:
                        diffs = dmp.diff_main(source_content, build_content)
                        dmp.diff_cleanupSemantic(diffs)

                        # Find sections in the BR document that or not in the other documents
                        added_sections = find_added_sections(diffs)
                        for section in added_sections:
                            if section in sections:
                                for sf in sections[section]['BR']:
                                    if os.path.exists(sf):
                                        # If it does, rename it
                                        os.rename(sf, str(sf).replace('_BR_', '_TLS_'))
                                        print(dt, section, sf)
                                    else:
                                        print(dt, section, sf, "** already renamed")

        except FileNotFoundError as e:
            print(f"File not found: {e.filename}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()
