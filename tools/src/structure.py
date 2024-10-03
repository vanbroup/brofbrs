import re
from pathlib import Path


def get_type(file: Path) -> str:
    return re.search("\_([A-Z]{2,8})(_|\.md)", file.name).group(1)


def get_section(file: Path) -> str:
    return ".".join([str(item).lstrip("0") for item in re.findall("(?<!_)([0-9]{3}|[0-9]{2}[A-Z])(?!_[A-Z])", file.resolve().__str__())])


def get_sections(input_dir: Path, sections: dict[str, dict[str, Path]]) -> None:
    for f in sorted(input_dir.glob("*.md")):
        rt = re.search("\_([A-Z]{2,8})(_|\.md)", f.name)
        if rt is None:
            print("Invalid filename {}".format(f.name))
            continue  # Skip invalid filenames

        type = rt.group(1)
        section = get_section(f)
        if section not in sections:
            sections[section] = {'BR': [], type: []}
        else:
            # Ensure 'type' key is present in the dictionary
            sections[section].setdefault(type, [])

        sections[section][type].append(f)

    # Process all files in the subdirectories
    for subdir in sorted(input_dir.iterdir()):
        if subdir.is_dir():
            sections = get_sections(subdir, sections)

    return sections
