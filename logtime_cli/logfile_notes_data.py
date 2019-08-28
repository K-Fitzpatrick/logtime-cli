"""
Responsibilities:
    Represent logfile notes section

Allows one to gather information about the Notes section of a logfile.
This class assumes these sections are written using markdown-style headers.
"""

from builtins import object
import re

class LogfileNotesSection(object):
    """A section of a logfile, defined by a markdown header section"""
    def __init__(self, name, full_text, header_level=1):
        self.name = name
        self.full_text = full_text
        self.header_level = header_level

    def get_text(self):
        """The text that exists before any sections"""
        # Match all text from the beginning up unto a newline starting with #
        match = re.match('^(.*?)((^#)|\n#)', self.full_text, re.DOTALL)
        if match:
            return match.group(1)
        return self.full_text

    def get_subsections(self):
        """A list of the next-level headers and their contents"""
        subsection_header = '#' * (self.header_level+1)

        # skip all text until the the first example of the next-level header
        text_remainder_regex = '(?:\n|^){} (.*?)\n(.*)'.format(subsection_header)
        text_remainder_match = re.search(text_remainder_regex, self.full_text, re.DOTALL)
        if text_remainder_match:
            current_subsection_name = text_remainder_match.group(1)
            text_remainder = text_remainder_match.group(2)
        else:
            return []

        subsections = []
        current_subsection_lines = []
        for line in text_remainder.split('\n'):
            current_header_match = re.match('^(#+) (.*)$', line)
            if current_header_match:
                current_header = current_header_match.group(1)
                if len(current_header) == len(subsection_header):
                    # store the previous lines as a new subsection
                    subsections.append(
                        LogfileNotesSection(
                            name=current_subsection_name,
                            full_text='\n'.join(current_subsection_lines),
                            header_level=len(subsection_header),
                        )
                    )

                    # reset the buffer for the next subsection
                    current_subsection_name = current_header_match.group(2)
                    current_subsection_lines = []

                elif len(current_header) < len(subsection_header):
                    # stop, as we've reached the end of this section
                    break
                else:
                    # any larger header is part of the full text of this subsection
                    current_subsection_lines.append(line)
            else:
                current_subsection_lines.append(line)

        # store the current buffer as the last subsection
        subsections.append(
            LogfileNotesSection(
                name=current_subsection_name,
                full_text='\n'.join(current_subsection_lines),
                header_level=len(subsection_header),
            )
        )

        return subsections
