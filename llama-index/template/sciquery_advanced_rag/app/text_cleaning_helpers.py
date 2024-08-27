# Code taken from the Unstructured library https://github.com/Unstructured-IO/unstructured/blob/main/unstructured/cleaners/core.py

import re

UNICODE_BULLETS = [
    "\u0095",
    "\u2022",
    "\u2023",
    "\u2043",
    "\u3164",
    "\u204C",
    "\u204D",
    "\u2219",
    "\u25CB",
    "\u25CF",
    "\u25D8",
    "\u25E6",
    "\u2619",
    "\u2765",
    "\u2767",
    "\u29BE",
    "\u29BF",
    "\u002D",
    "",
    "\*", 
    "\x95",
    "·",
]

BULLETS_PATTERN = "|".join(UNICODE_BULLETS)

UNICODE_BULLETS_RE = re.compile(f"(?:{BULLETS_PATTERN})(?!{BULLETS_PATTERN})")

PARAGRAPH_PATTERN = r"\s*\n\s*"  # noqa: W605 NOTE(harrell)

PARAGRAPH_PATTERN_RE = re.compile(
    f"((?:{BULLETS_PATTERN})|{PARAGRAPH_PATTERN})(?!{BULLETS_PATTERN}|$)",
)
DOUBLE_PARAGRAPH_PATTERN_RE = re.compile("(" + PARAGRAPH_PATTERN + "){2}")

E_BULLET_PATTERN = re.compile(r"^e(?=\s)", re.MULTILINE)


def clean_non_ascii_chars(text) -> str:
    """Cleans non-ascii characters from unicode string.

    Example
    -------
    \x88This text contains non-ascii characters!\x88
        -> This text contains non-ascii characters!
    """
    en = text.encode("ascii", "ignore")
    return en.decode()

def clean_bullets(text: str) -> str:
    """Cleans unicode bullets from a section of text.

    Example
    -------
    ●  This is an excellent point! -> This is an excellent point!
    """
    search = UNICODE_BULLETS_RE.match(text)
    if search is None:
        return text

    cleaned_text = UNICODE_BULLETS_RE.sub(" ", text, 1)
    return cleaned_text.strip()

def clean_extra_whitespace(text: str) -> str:
    """Cleans extra whitespace characters that appear between words.

    Example
    -------
    ITEM 1.     BUSINESS -> ITEM 1. BUSINESS
    """
    cleaned_text = re.sub(r"[\xa0\n]", " ", text)
    cleaned_text = re.sub(r"([ ]{2,})", " ", cleaned_text)
    return cleaned_text.strip()

def group_broken_paragraphs(
    text: str,
    line_split: re.Pattern[str] = PARAGRAPH_PATTERN_RE,
    paragraph_split: re.Pattern[str] = DOUBLE_PARAGRAPH_PATTERN_RE,
) -> str:
    """Groups paragraphs that have line breaks for visual/formatting purposes.
    For example:

    '''The big red fox
    is walking down the lane.

    At the end of the lane
    the fox met a bear.'''

    Gets converted to

    '''The big red fox is walking down the lane.
    At the end of the land the fox met a bear.'''
    """
    paragraphs = paragraph_split.split(text)
    clean_paragraphs = []
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
        para_split = line_split.split(paragraph)
        all_lines_short = all(len(line.strip().split(" ")) < 5 for line in para_split)
        if UNICODE_BULLETS_RE.match(paragraph.strip()) or E_BULLET_PATTERN.match(paragraph.strip()):
            clean_paragraphs.extend(group_bullet_paragraph(paragraph))
        elif all_lines_short:
            clean_paragraphs.extend([line for line in para_split if line.strip()])
        else:
            clean_paragraphs.append(re.sub(PARAGRAPH_PATTERN, " ", paragraph))

    return "\n\n".join(clean_paragraphs)

def merge_hyphenated_words(text):
    """
    Merges incorrectly hyphenated words in a given text.

    This function uses a regular expression to identify occurrences where a word has been split by
    a hyphen followed by whitespace, such as in 'import- ant'. It merges these split parts into a
    single word, effectively correcting the text to appear as 'important'.

    Parameters:
        text (str): The text containing hyphenated words to be merged.

    Returns:
        str: The corrected text with all hyphenated words merged.

    Example:
        corrected_text = merge_hyphenated_words("The document was import- ant for the meeting.")
        print(corrected_text)  # Output: "The document was important for the meeting."
    """
    # Regular expression to find hyphenated words
    pattern = r'(\w+)-\s+(\w+)'
    # Replace the found patterns by merging the two groups
    corrected_text = re.sub(pattern, r'\1\2', text)
    return corrected_text

remove_citations = lambda text: re.sub("\[\d{1,3}\]", "", text)

def clean(
    text: str,
    extra_whitespace: bool = False,
    broken_paragraphs: bool = False,
    bullets: bool = False,
    ascii: bool = False,
    lowercase: bool = False,
    citations: bool = False,
    merge_split_words: bool = False,

) -> str:
    """Cleans text.

    """

    cleaned_text = text.lower() if lowercase else text
    cleaned_text = (
        clean_non_ascii_chars(cleaned_text) if ascii else cleaned_text
    )
    cleaned_text = remove_citations(cleaned_text) if citations else cleaned_text
    cleaned_text = clean_extra_whitespace(cleaned_text) if extra_whitespace else cleaned_text
    cleaned_text = clean_bullets(cleaned_text) if bullets else cleaned_text
    cleaned_text = merge_hyphenated_words(cleaned_text) if merge_split_words else cleaned_text
    return cleaned_text.strip()