from datetime import datetime

from file_manager import FileManager
from util import Util


class User(object):
    USERS_FILEPATH = "assets/pickles/users.pkl"

    def __init__(self, config):
        self._name = None
        self._new_user = False
        self._config = config
        self._users = {}
        self.load_preferences()

    @property
    def name(self):
        return self._name

    @property
    def is_new_user(self):
        return self._new_user

    def set_new_user(self, new_user):
        self._new_user = new_user

    def update_name(self, name):
        self._users.update(
            {
                f"{name}": {
                    "last_login_datetime": self._users[self._name][
                        "last_login_datetime"
                    ],
                    "preferences": {
                        "bot_name": self._users[self._name]["preferences"]["bot_name"]
                    },
                }
            }
        )
        del self._users[self._name]
        self._name = name

    def authenticate(self, bot_memory):
        is_new_user = False
        self._name = Util.read_info("[Name] ").title()
        if not self._users or self._name not in self._users:
            is_new_user = True
            self._users.update(
                {
                    f"{self._name}": {
                        "last_login_datetime": None,
                        "preferences": {"bot_name": None},
                    }
                }
            )

        self._users[self._name]["last_login_datetime"] = datetime.now()

        preferred_bot_name = self._users[self._name]["preferences"]["bot_name"]
        if preferred_bot_name is not None:
            bot_memory.set_bot_name(preferred_bot_name)

        return is_new_user

    def save_preferences(self):
        FileManager.save_pickle(self._users, self.USERS_FILEPATH, self._config.quiet)

    def load_preferences(self):
        users = FileManager.load_pickle(self.USERS_FILEPATH, self._config.quiet)
        if users:
            self._users = users
