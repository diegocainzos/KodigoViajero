import spacy
from spacy.matcher import Matcher, PhraseMatcher

nlp = spacy.load("en_core_web_md")

# Matcher for generic patterns
matcher = Matcher(nlp.vocab)

# Climate
matcher.add("CLIMATE", [[{"LOWER": {"IN": [
            "hot", "warm", "sunny", "cold", "snowy", "rainy", "tropical", "mild"]}}]])

# Activities
matcher.add("ACTIVITY", [[{"LOWER": {"IN": ["beach", "hiking", "skiing",
            "nightlife", "party", "museum", "festival", "surfing", "diving", "cycling"]}}]])

# Type of tourism
matcher.add("TRAVEL_TYPE", [[{"LOWER": {"IN": [
            "cultural", "adventure", "relax", "romantic", "family", "nature", "luxury", "budget"]}}]])

# PhraseMatcher for compound expressions
phrase_matcher = PhraseMatcher(nlp.vocab)
activities = ["street food", "local food",
              "car rental", "live music", "wine tasting"]
patterns = [nlp(text) for text in activities]
phrase_matcher.add("PHRASE_ACTIVITY", patterns)


def extract_tourism_info(text):
    doc = nlp(text)
    extracted = {
        "locations": [],
        "dates": [],
        "budget": [],
        "duration": [],
        "climate": [],
        "activities": [],
        "travel_type": []
    }

    # 1. Extract with NER
    for ent in doc.ents:
        if ent.label_ == "GPE":
            extracted["locations"].append(ent.text)
        elif ent.label_ == "LOC":
            extracted["locations"].append(ent.text)
        elif ent.label_ == "DATE":
            extracted["dates"].append(ent.text)
        elif ent.label_ == "MONEY":
            extracted["budget"].append(ent.text)
        elif ent.label_ == "CARDINAL":
            extracted["duration"].append(ent.text)

    # 2. Extract with Matcher
    matches = matcher(doc)
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        span = doc[start:end]
        if label == "CLIMATE":
            extracted["climate"].append(span.text)
        elif label == "ACTIVITY":
            extracted["activities"].append(span.text)
        elif label == "TRAVEL_TYPE":
            extracted["travel_type"].append(span.text)

    # 3. Extract with PhraseMatcher
    phrase_matches = phrase_matcher(doc)
    for match_id, start, end in phrase_matches:
        extracted["activities"].append(doc[start:end].text)

    return extracted
