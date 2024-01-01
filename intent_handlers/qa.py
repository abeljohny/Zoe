import re
from datetime import datetime

from constants import Intent, Tags
from intent_handlers.intentABC import IntentABC
from semantic_search import SemanticSearch


class QA(IntentABC):
    def __init__(self, config, memory, user):
        super().__init__()
        self._config = config
        self._memory = memory
        self._user = user
        self._search_engine = SemanticSearch(self._config)

    def replace_placeholders(self, response):
        placeholder_token = "<placeholder:"

        def replace_token(text: str, token: str, replacement: str) -> str:
            return text.replace(placeholder_token + token + ">", replacement)

        while placeholder_token in response:
            placeholder = re.search(r"<placeholder:(\w+)>", response).group(1)
            match placeholder:
                case "name":
                    response = replace_token(response, placeholder, self._user.name)
                case "botname":
                    response = replace_token(
                        response, placeholder, self._memory.botname
                    )
                case "gm":
                    now = datetime.now()
                    if now.hour >= 12:
                        reply = f"Hey {self._user.name}. By the way, it's {now.strftime('%H:%M')}."
                    else:
                        reply = f"Good morning, {self._user.name}"
                    response = replace_token(response, placeholder, reply)
                case "ga":
                    now = datetime.now()
                    if now.hour >= 17 or now.hour < 12:
                        reply = f"Hey {self._user.name}. By the way, it's {now.strftime('%H:%M')}."
                    else:
                        reply = f"Good afternoon, {self._user.name}"
                    response = replace_token(response, placeholder, reply)
                case "ge":
                    now = datetime.now()
                    if now.hour < 17:
                        reply = f"Hey {self._user.name}. By the way, it's {now.strftime('%H:%M')}."
                    else:
                        reply = f"Good evening, {self._user.name}"
                    response = replace_token(response, placeholder, reply)
        return response

    @staticmethod
    def _replace_tags(text):
        tags_token = "<tags:"
        tag = None
        if tags_token in text:
            tag = re.search(r"<tags:(\w+)>", text).group(1)
            text = text.replace(tags_token + tag + ">", "")
        return tag, text

    def handle(self, request, intent):
        reply = self.replace_placeholders(self._search_engine.search(request))
        if intent == Intent.NAMEOPS.value:
            tag, reply = self._replace_tags(reply)
            dialog_state = self._memory.initialize_dialog_state(intent=intent, tag=tag)
            self._memory.enqueue_dialog_state(dialog_state)
        return reply

    def continue_conversation(self, request, intent) -> str:
        recent_dialog_state = self._memory.dequeue_dialog_state()
        name = request.title()
        if not name:
            name = self.Util.read_info("[Name] ").title()

        match recent_dialog_state["data"]["tag"]:
            case Tags.USER.value:
                self._user.update_name(name)
            case Tags.BOT.value:
                self._memory.update_botname(name)

        return "Updated."
