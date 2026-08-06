from pathlib import Path
import re


INCLUDE_PATTERN = re.compile(
    r'#include\s+"([^"]+)"'
)

INCLUDE_DIR = (
    Path(__file__).parent /
    "shaders" /
    "includes"
)


def load_shader(path):
    path = Path(path)

    source = path.read_text()

    return resolve_includes(
        source,
        path.parent
    )


def resolve_includes(source, current_directory):

    def replace_include(match):

        include_name = match.group(1)

        include_path = current_directory / include_name

        if not include_path.exists():
            include_path = INCLUDE_DIR / include_name

        if not include_path.exists():
            raise FileNotFoundError(
                f'Could not find include "{include_name}"'
            )

        include_source = include_path.read_text()

        return resolve_includes(
            include_source,
            include_path.parent
        )


    return INCLUDE_PATTERN.sub(
        replace_include,
        source
    )