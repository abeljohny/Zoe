from config import config
from semantic_search import SemanticSearch


def evaluate():
    test_set = [
        {
            "query": "how have you been doing?",
            "correct_reply": "I am functioning optimally, thank you for asking. Would you like me to book, reschedule, "
            "cancel, or lookup an appointment for you today?",
        },
        {
            "query": "have you been sleeping well?",
            "correct_reply": "I am functioning optimally, thank you for asking. Would you like me to book, reschedule, "
            "cancel, or lookup an appointment for you today?",
        },
        {"query": "shout my name", "correct_reply": "Your name is <placeholder:name>"},
        {
            "query": "shout your name",
            "correct_reply": "My name is <placeholder:botname>",
        },
        {
            "query": "tell me moi name",
            "correct_reply": "Your name is <placeholder:name>",
        },
        {
            "query": "address me by a different name",
            "correct_reply": "Sure, what would you like to change it to?<tags:user>",
        },
        {
            "query": "I wish you a different name",
            "correct_reply": "Sure, what would you like to change it to?<tags:bot>",
        },
        {
            "query": "can I call you by a different name?",
            "correct_reply": "Sure, what would you like to change it to?<tags:bot>",
        },
    ]

    search_engine = SemanticSearch(config())
    num_of_correct_answers = 0

    for item in test_set:
        reply = search_engine.search(item["query"])
        if reply == item["correct_reply"]:
            num_of_correct_answers += 1

    accuracy = num_of_correct_answers / len(test_set)
    print(f"Search Accuracy: {accuracy}")
