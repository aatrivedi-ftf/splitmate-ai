import re
import spacy

nlp = spacy.load("en_core_web_sm")
LOGGED_IN_USER_NAME = "Aastha"

TRAILING_KEYWORDS = {"unevenly", "evenly", "equally", "randomly", "fairly"}

def clean_participant_name(name: str) -> str:
    name = name.strip().rstrip(",.")
    if name.lower() == "me":
        return LOGGED_IN_USER_NAME
    for keyword in TRAILING_KEYWORDS:
        if name.lower().endswith(" " + keyword):
            name = name[: -len(keyword)].strip()
    return name

def parse_command_conversational(command):
    print(f"👂 You said: \"{command}\"")

    result = {
        "user_id": "u001",
        "total_amount": 0.0,
        "participants": [],
        "splits": {},
        "raw_text": command
    }

    doc = nlp(command)

    # Step 1: Detect amount
    print("🔍 Looking for total amount to split...")
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            amount_str = ent.text.replace("$", "").replace("Rs", "").strip()
            try:
                result["total_amount"] = float(re.sub(r'[^\d.]', '', amount_str))
                print(f"✅ Found amount: {result['total_amount']}")
            except ValueError:
                print("⚠️ Couldn't parse amount from MONEY entity.")

    if result["total_amount"] == 0.0:
        match = re.search(r'split\s+(\d+(?:\.\d+)?)', command, re.IGNORECASE)
        if match:
            result["total_amount"] = float(match.group(1))
            print(f"✅ Found amount using fallback: {result['total_amount']}")

    # Step 2: Extract people
    print("🧠 Trying to figure out who's involved...")
    person_names = {clean_participant_name(ent.text) for ent in doc.ents if ent.label_ == "PERSON"}

    name_block_match = re.search(r'between\s+(.+)', command, flags=re.IGNORECASE)
    if name_block_match:
        raw_names = name_block_match.group(1)
        split_names = re.split(r'\band\b|,', raw_names, flags=re.IGNORECASE)
        for name in split_names:
            cleaned = clean_participant_name(name)
            if cleaned:
                person_names.add(cleaned)

    result["participants"] = list(dict.fromkeys(person_names))

    if result["participants"]:
        print(f"👥 Participants: {', '.join(result['participants'])}")
    else:
        print("⚠️ I couldn't figure out who should split this.")

    if result["total_amount"] == 0.0:
        print("⚠️ I couldn't detect any amount to split.")

    return result
