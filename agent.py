from app.voice_input import get_voice_text
from app.parser import parse_command_conversational
from app.recommender import recommend_friends
from app.splitter import calculate_split

def run_agent():
    print("🎙️ Listening for command...")
    voice = get_voice_text()
    print("You said:", voice)

    parsed = parse_command_conversational(voice)
    print("Parsed:", parsed)

    friends = recommend_friends(parsed["user_id"])
    print("Suggested friends:", friends)

    split = calculate_split(parsed)
    print("Final split:", split)
