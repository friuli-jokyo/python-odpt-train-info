from datetime import datetime, timedelta, timezone
import json
import os
from .errors import TooOldCacheError
from .odpt_client import download
from .odpt_components import Distributor, TrainInformation


_JST = timezone(timedelta(hours=+9), 'JST')

_cache_dir = os.path.join("./__odptcache__/")


def set_cache_dir(dir: str) -> None:
    """Set directory to save cache.

    If dir is not exist, make directories recursively.
    """

    os.makedirs(dir, exist_ok=True)
    if os.path.isdir(dir):
        global _cache_dir
        _cache_dir = dir
    else:
        raise ValueError("Not a directory or failed to make directory.")

def _build_cache_path(distributor: Distributor) -> str:
    return os.path.join( _cache_dir, distributor.name+".json" )

def _load(distributor: Distributor, expire_second: int = 40) -> list[TrainInformation] | None:
    """Load cache

    Return List of train information if cache is younger than expire_second, None otherwise.

    Parameters
    ----------
    distributor : Distributor
    expire_second : int, optional
        (default 40)

    Returns
    -------
    list[TrainInformation] | None
        List of train information which is loaded from cache.
    """

    cache_path = _build_cache_path(distributor=distributor)

    try:
        cache_age = datetime.now(_JST) - datetime.fromtimestamp(os.path.getmtime(cache_path), _JST)
    except FileNotFoundError:
        return None

    if cache_age > timedelta(seconds=expire_second):
        return None

    try:
        with open(cache_path, encoding='utf-8') as loadedCacheJSON:
            return json.load(loadedCacheJSON)
    except FileNotFoundError:
        return None


def _set(distributor: Distributor, max_try : int) -> list[TrainInformation]|None:
    """Download information and save it to cache.

    Parameters
    ----------
    distributor : Distributor
    max_try : int
        Try to download information up to max_try times.

    Returns
    -------
    list[TrainInformation]|None
        List of train information which is downloaded from distributor, or None if failed to download max_try times.
    """

    get_dict = download(distributor=distributor, max_try=max_try)

    if get_dict == None:
        return None
    else:
        cache_path = _build_cache_path(distributor=distributor)

        os.makedirs(_cache_dir, exist_ok=True)

        with open(cache_path, "w", encoding='utf-8') as saveCacheJSON:
            saveCacheJSON.write(json.dumps(get_dict,ensure_ascii=False))

        return get_dict

def refresh_cache() -> None:
    """Refresh caches which is older than 40sec.

    If Failed to download information, it tries to download up to 4 times.
    """

    for distributor in Distributor:
        if _load(distributor=distributor, expire_second=40) in [None, {}]:
            _set(distributor=distributor, max_try=4)

def fetch_info(max_try:int = 1) -> list[TrainInformation]:
    """Load and Concat train information.

    Information are loaded from cache basically.
    If cache is old, it tries to download information.
    Nonetheless if failed to download, it loads cache forcibly.
    If cache is too old, it raises TooOldCache Error.


    Parameters
    ----------
    max_try : int, optional
        Try to download information up to max_try times, by default 1

    Returns
    -------
    list[TrainInformation]
        List of train information.

    Raises
    ------
    TooOldCacheError
        Load cache forcibly but it was too old.
    """

    result: list[TrainInformation] = []

    for distributor in Distributor:
        cache = _load(distributor=distributor, expire_second=80)
        if cache != None:
            result += cache
            continue

        get = _set(distributor=distributor, max_try=max_try)
        if get != None:
            result += get
            continue

        cache_force = _load(distributor=distributor, expire_second=140)
        if cache_force != None:
            result += cache_force
        else:
            raise TooOldCacheError

    return result
