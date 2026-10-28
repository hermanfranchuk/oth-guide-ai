# imports
from rapidfuzz import fuzz
import data


# remove punctuation
def normalize_text(text):
    return (
        text.lower()
        .replace("?", " ")
        .replace("!", " ")
        .replace(".", " ")
        .replace(",", " ")
        .replace(":", " ")
        .replace(";", " ")
        .replace("/", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace("-", " ")
    )


# collect all language variants of one term
def get_term_variants(term):
    variants = []

    if "german" in term:
        variants.append(term["german"])

    if "english" in term:
        variants.append(term["english"])

    if "abbreviation" in term:
        abbreviations = term["abbreviation"].split(",")

        for abbreviation in abbreviations:
            variants.append(abbreviation.strip())

    normalized_variants = []

    for variant in variants:
        normalized_variant = normalize_text(variant).strip()

        if normalized_variant and normalized_variant not in normalized_variants:
            normalized_variants.append(normalized_variant)

    return normalized_variants


# build reusable language variant list
def prepare_language_term_variants():
    if data.LANGUAGE_TERM_VARIANTS is not None:
        return data.LANGUAGE_TERM_VARIANTS

    language_term_variants = []

    for term in data.LANGUAGE_TERMS:
        variants = get_term_variants(term)

        if variants:
            language_term_variants.append(variants)

    data.LANGUAGE_TERM_VARIANTS = language_term_variants

    return data.LANGUAGE_TERM_VARIANTS


# make user input easier to match with keywords
def expand_user_input_with_language_terms(user_input):
    normalized_input = normalize_text(user_input)
    words = normalized_input.split()

    expanded_parts = [normalized_input]
    language_term_variants = prepare_language_term_variants()

    for variants in language_term_variants:
        term_found = False

        for variant in variants:
            if " " in variant:
                if variant in normalized_input:
                    term_found = True
            else:
                if variant in words:
                    term_found = True

        if term_found:
            expanded_parts.extend(variants)

    expanded_input = " ".join(expanded_parts)
    expanded_words = expanded_input.split()

    return expanded_input, expanded_words


# detect a keyword match in user_input
def keyword_match(user_input, tag, threshold=85):
    keywords = data.SKILL_KEYWORDS[tag]

    expanded_input, words = expand_user_input_with_language_terms(user_input)

    for keyword in keywords:
        keyword = normalize_text(keyword).strip()

        if " " in keyword:
            if keyword in expanded_input or fuzz.partial_ratio(keyword, expanded_input) >= threshold:
                return True
        else:
            if keyword in words:
                return True

            for word in words:
                if fuzz.ratio(word, keyword) >= threshold:
                    return True

    return False