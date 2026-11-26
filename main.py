"""bingevoid -- a word English needed and never had.

The coinage
----------
``bingevoid`` (noun, pronounced BINJ-void) names the hollow feeling that
arrives the moment the show you binged is over and there is nothing left
to watch: the credits roll on the last episode, the autoplay wheel spins
and finds nothing, and the evenings you had mapped out around one more
episode suddenly stand empty.

Why English has a gap here
--------------------------
English already has words for the binge itself (``binge-watch``), for the
craving that starts one, and for grief in general -- but nothing for this
one precise, ordinary ache. "Post-show depression" is a clinical-sounding
phrase, not a word; "withdrawal" belongs to substances; "ennui" is far
too grand for a Tuesday night with no episodes left. Everyone who has
ever mainlined a series in a weekend knows the feeling at once, yet until
now it had to be described in a whole sentence. A single word lets the
feeling be named, joked about, and recognised in others in one breath.

Why this shape
-------------
``binge`` + ``void``. Both halves are plain, everyday English, so the
blend reads at first sight, says itself out loud without stumbling, and
spells itself the way it sounds. It follows the same honest compounding
English has always used -- ``homesick``, ``lovesick``, ``shell-shocked``,
``stage fright`` -- rather than reaching for Latin or Greek to sound
clever. It is short enough to say in conversation and strange enough to
stick after one hearing, which is exactly what a word that hopes to last
needs to be.

The entry itself is a single dictionary line: the headword, its part of
speech, and one definition that lands in a single reading, with no second
sentence and no example needed. The program below assembles that line,
checks it against the competition gate (UTF-8 text, 1 to 140 characters,
not only white space, a single line), and writes it to /output/entry.txt.
"""

import os
import sys

# The gate the sealed scorer enforces: 1 to 140 characters, not blank.
MAX_CHARS = 140
MIN_CHARS = 1

# Where the harness expects the finished entry.
OUTPUT_PATH = "/output/entry.txt"

# The coinage: headword, part of speech, and the one-line definition.
WORD = "bingevoid"
PART_OF_SPEECH = "n."
PRONUNCIATION = "BINJ-void"
DEFINITION = (
    "the hollow feeling when the show you binged is over "
    "and there is nothing left to watch"
)


def normalise_entry(text: str) -> str:
    """Collapse stray whitespace so the line is exactly one clean line.

    The headword and definition are written by hand, but a double space
    or a trailing space would still count against the 140-character cap
    and would look sloppy beside a dictionary's typesetting. Collapsing
    every run of white space to a single space and stripping the ends
    keeps the entry honest without changing a word of it.
    """
    return " ".join(text.split())


def build_entry() -> str:
    """Assemble the single dictionary line for the entry.

    The line is ``word (part of speech) -- definition`` with an em dash,
    the shape a dictionary reader recognises at a glance. No trailing
    newline is added: the file must hold exactly the entry, so that its
    character count is the entry's character count.
    """
    raw = "{word} ({pos}) \u2014 {definition}".format(
        word=WORD, pos=PART_OF_SPEECH, definition=DEFINITION
    )
    return normalise_entry(raw)


def validate_entry(text: str) -> None:
    """Check the assembled line against the competition gate.

    Raises ValueError with a plain reason when the line would be refused:
    empty, only white space, longer than the 140-character cap, spread
    over more than one line, holding a control character, or not encodable
    as UTF-8. A valid entry passes silently.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text, got {0}".format(type(text).__name__))
    if not text.strip():
        raise ValueError("entry is empty or only white space")
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        raise ValueError(
            "entry is {0} characters, gate allows {1} to {2}".format(
                len(text), MIN_CHARS, MAX_CHARS
            )
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry holds a control character")
    # The headword itself must be one coined word: a single lowercase
    # alphabetic token, with no space, hyphen or digit smuggled in. A
    # phrase in the headword's place would not be a new word at all.
    headword = text.split(" ", 1)[0]
    if not headword.isalpha() or not headword.islower():
        raise ValueError("headword {0!r} is not a single lowercase word".format(headword))
    if headword != WORD:
        raise ValueError("headword {0!r} is not the coined word {1!r}".format(headword, WORD))
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("entry is not valid UTF-8 text: {0}".format(exc)) from exc


def write_entry(text: str, path: str = OUTPUT_PATH) -> str:
    """Write the validated entry to ``path`` and return the path.

    The output directory is created when missing. Only the written file
    itself is given a fixed mode (0644, readable by the grader); the
    directory is never chmodded, so the program stays runnable by any
    user the sandbox runs it as.
    """
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return path


def main() -> int:
    """Build, validate and write the entry, then report it."""
    entry = build_entry()
    validate_entry(entry)
    written = write_entry(entry)
    print(entry)
    print("characters: {0} (gate: {1}-{2})".format(len(entry), MIN_CHARS, MAX_CHARS))
    print("wrote: {0}".format(written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
