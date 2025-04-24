from utils.helper import load_data


class DataCache:
    def __init__(self):
        self.cache = None

    async def get_data(self):
        if self.cache is None:
            self.cache = await load_data()
        return self.cache
