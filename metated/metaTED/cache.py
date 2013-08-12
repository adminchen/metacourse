import os
from shove import Shove
from shove.store.file import FileStore


cached_storage = Shove(
    store=FileStore(os.path.expanduser('~/.metaTED/cache')),
    cache='simplelru://',
    sync=1 # Minimizes data loss on various processing errors
)

cache = cached_storage._cache
