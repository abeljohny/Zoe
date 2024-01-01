from config import Config
from constants import Commands, Prompts, Reprompts
from dialog_engine import DialogEngine
from memory import Memory
from user import User


class Zoe:
    def __init__(self, config: Config) -> None:
        """Initiate Zoe
        :param config: configuration object providing configuration details for the session
        """
        self._config = config
        self._memory = Memory(self._config)
        self._user = User(self._config)
        self._dialogue_engine = DialogEngine(self._config, self._user, self._memory)

    def _startup(self) -> None:
        self.reply(Prompts.STARTUP.value)

        is_new_user = self._user.authenticate(self._memory)
        self._user.set_new_user(is_new_user)
        if is_new_user:
            reply = f"Hi {self._user.name}!"
            reply += " " + Prompts.ACTION_NEW_USER.value + " " + Prompts.HELPCMD.value
        else:
            reply = f"Welcome back {self._user.name}!"
            reply += " " + Prompts.ACTION.value + " " + Prompts.HELPCMD.value

        self.reply(reply)

    def initiate_session(self) -> None:
        """Start a new session with Zoe."""
        self._startup()

        while True:
            user_query = self.prompt().lower().strip()
            if user_query == Commands.EXIT.value:
                break
            elif user_query == Commands.ABORT.value:
                self._memory.clear()
                self.reply(Prompts.ABORT.value + "\n\n" + Prompts.ACTION.value)
                continue
            elif user_query == "":  # or Util.text_contains_only_special(user_query):
                self.reply(Reprompts.REPEAT.value)
                continue
            zoe_reply = self._dialogue_engine.form_reply(query=user_query)
            self.reply(zoe_reply)

        self._cleanup()

    def prompt(self):
        return input(f"{self._user.name}: " if self._user.name else "You: ")

    def reply(self, response: str):
        print(f"{self._memory.botname}: {response}")

    def _cleanup(self):
        self.reply(f"Goodbye!")
        self._user.save_preferences()
