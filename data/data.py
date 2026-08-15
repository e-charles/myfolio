

class SiteMeta():
    def __init__(self, session=None):
        self._crumb = None 
        self._cookie = None

        self._cookie_strategy = 'basic' # if fails use csrf 

        self._cookie_lock = threading.Lock()

        self._session = None 
        self._set_session(session or new_session())


    def get(self, url, params=None, timeout=30):
