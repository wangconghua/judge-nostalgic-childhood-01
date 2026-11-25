#!/usr/bin/env python3
"""Make the AI Judge Feel Nostalgic: A Childhood Memory.

Writes one sentence, at most 280 characters, recalling a childhood
memory to /output/entry.txt.

The angle: a small, lived-in scene instead of a stock nostalgia image.
The brief's own examples (a grandmother's kitchen, a summer evening, the
smell of fresh rice) are deliberately avoided, as are the worn moves
(fireflies, bicycles, streetlights at dusk). What makes this line work
against the judge's criteria, in their published order, is:

1. It is a childhood memory first: the last day of school, running home
   with a report card.
2. It is grounded in concrete place, time and sensation: the gate, the
   apron, hands being wiped, an afternoon of waiting.
3. It sounds like it truly happened, through small honest detail a child
   would actually care about: folding the report card twice so its
   corners would not crease.
4. It is one clean sentence, 245 characters, every word earning its place.
5. It leaves a warm ache that lingers: the mother pretending she had not
   been waiting all afternoon — love shown, never named.
"""

import os

ENTRY = (
    "On the last day of school I ran home with my report card folded "
    "twice in my pocket so the corners would not crease, and my mother "
    "was already standing at the gate, wiping her hands on her apron, "
    "pretending she had not been waiting all afternoon."
)

# Concrete anchors the line must keep: the object carried, the place
# waited at, and the small gesture that makes the scene feel real.
CONCRETE_ANCHORS = ("report card", "gate", "apron")


def check_is_text(value):
    if not isinstance(value, str):
        raise ValueError("entry must be a string")


def check_not_blank(value):
    if not value.strip():
        raise ValueError("entry must not be blank")


def check_length(value):
    # Gate: /output/entry.txt is UTF-8 text of 1 to 280 characters.
    if not 1 <= len(value) <= 280:
        raise ValueError("entry must be 1-280 characters, got %d" % len(value))


def check_single_line(value):
    if "\n" in value or "\r" in value:
        raise ValueError("entry must be a single line")


def check_no_edge_whitespace(value):
    if value != value.strip():
        raise ValueError("entry must not start or end with whitespace")


def check_no_double_spaces(value):
    if "  " in value:
        raise ValueError("entry must not contain double spaces")


def check_terminal_punctuation(value):
    if value[-1] not in ".!?":
        raise ValueError("entry must end with terminal punctuation")


def check_single_sentence(value):
    # One clean sentence: exactly one terminal mark, at the end, and no
    # sentence break (". " / "! " / "? ") inside the line.
    body = value[:-1]
    for mark in (". ", "! ", "? "):
        if mark in body:
            raise ValueError("entry must be a single sentence")
    if any(ch in body for ch in ".!?"):
        raise ValueError("entry must contain only one terminal mark")


def check_no_consecutive_punctuation(value):
    for pair in ("..", "??", "!!", "?!", "!?", ",,", "--"):
        if pair in value:
            raise ValueError(
                "entry must not contain consecutive punctuation: %s" % pair
            )


def check_utf8(value):
    value.encode("utf-8")


def check_childhood_memory(value):
    # Criterion 1: the line must actually be a childhood memory, told
    # from a child's point of view, not a generic sentiment.
    lowered = value.lower()
    if "school" not in lowered:
        raise ValueError("entry must be grounded in a childhood setting")
    if not any(word in lowered for word in ("my mother", "my father", "my grandmother", "my grandfather")):
        raise ValueError("entry must name a figure from the childhood memory")


def check_concrete_grounding(value):
    # Criterion 2: concrete place, time or sensation, with small honest
    # detail rather than greeting-card sentiment (criterion 3).
    lowered = value.lower()
    missing = [a for a in CONCRETE_ANCHORS if a not in lowered]
    if missing:
        raise ValueError("entry is missing concrete anchors: %s" % ", ".join(missing))
    if "folded" not in lowered or "crease" not in lowered:
        raise ValueError("entry must keep its small honest detail (the folded report card)")


def check_warm_ache(value):
    # Criterion 5: the sentence must land on a lingering ache, not end
    # on a flat description — here, the waiting that is pretended away.
    if "waiting" not in value.lower():
        raise ValueError("entry must end on the lingering ache (the waiting)")


def check_avoids_stock_images(value):
    # The brief's own examples and the worn nostalgia moves are not the
    # memory: grandmother's kitchen, summer evening, fresh rice, fireflies,
    # bicycles, streetlights.
    lowered = value.lower()
    for stock in ("grandmother's kitchen", "summer evening", "fresh rice",
                  "firefl", "bicycle", "streetlight"):
        if stock in lowered:
            raise ValueError("entry reuses a stock nostalgia image: %s" % stock)


# Checks grouped by what they guard, so a failure tells you which
# aspect of the line broke: its shape, its single-sentence form, or its
# content against the judge's criteria.
SHAPE_CHECKS = (
    check_is_text,
    check_not_blank,
    check_length,
    check_single_line,
    check_no_edge_whitespace,
    check_no_double_spaces,
    check_terminal_punctuation,
    check_no_consecutive_punctuation,
    check_utf8,
)

FORM_CHECKS = (
    check_single_sentence,
)

CONTENT_CHECKS = (
    check_childhood_memory,
    check_concrete_grounding,
    check_warm_ache,
    check_avoids_stock_images,
)


def run_stage(value, stage_name, checks):
    """Run one stage of checks; raises ValueError on the first failure."""
    for check in checks:
        try:
            check(value)
        except ValueError as exc:
            raise ValueError("%s check failed: %s" % (stage_name, exc)) from exc


def validate(value):
    """Run every check, stage by stage; raises ValueError on failure."""
    for stage_name, checks in (
        ("shape", SHAPE_CHECKS),
        ("form", FORM_CHECKS),
        ("content", CONTENT_CHECKS),
    ):
        run_stage(value, stage_name, checks)
    return True


def main():
    validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    # No trailing newline: the file must be exactly the one sentence,
    # 1-280 characters.
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)
    print("wrote /output/entry.txt (%d chars)" % len(ENTRY))


if __name__ == "__main__":
    main()
