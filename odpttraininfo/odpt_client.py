import json
import time
from urllib.error import HTTPError

import urllib.request
import urllib.parse

from .errors import Forbidden, InvalidConsumerKeyError, InvalidParameterError, NotFound, OdptServerError, UnknownHTTPError

from .odpt_components import TrainInformation_jsondict, Distributor, TrainInformation, multilanguage_str_keys


def download(distributor: Distributor, max_try:int = 4) -> list[TrainInformation]|None:
    """Download train information from distributor.

    If response status code was 500-599, this function retries up to max_try times.

    Parameters
    ----------
    distributor : Distributor
        Distributor of infomation source.
    max_try : int, optional
        If response status code was 500-599, it retries up to this value.(default = 4)

    Returns
    -------
    list[TrainInformation]|None
        List of train information which is downloaded from web, or None if consumerKey is unset.

    Raises
    ------
    InvalidParameterError
        HTTP status code was 400.
    InvalidConsumerKeyError
        HTTP status code was 401.
    Forbidden
        HTTP status code was 403.
    NotFound
        HTTP status code was 404.
    OdptServerError
        HTTP status code was 500-599.
    UnknownHTTPError
        HTTP status code was unexpected.
    """

    if not distributor.is_valid():
        return None

    query = {}
    query["acl:consumerKey"] = distributor.consumer_key
    if distributor == Distributor.TOKYO_METRO:
        query["rdf:type"] = "odpt:TrainInformation"

    json_dict:list[TrainInformation_jsondict] = []

    for try_count in range(max_try):
        try:
            with urllib.request.urlopen("%s?%s" % (distributor.URL, urllib.parse.urlencode(query))) as f:
                json_text = f.read().decode("utf-8")
            json_dict = json.loads(json_text)
            break
        except HTTPError as e:
            match e.code:
                case 400:
                    raise InvalidParameterError(e)
                case 401:
                    raise InvalidConsumerKeyError(e)
                case 403:
                    raise Forbidden(e)
                case 404:
                    raise NotFound(e, distributor.value)
                case code if 500 <= code < 600:
                    if try_count == max_try-1:
                        raise OdptServerError(e)
                    else:
                        time.sleep(1+try_count)
                        continue
                case _:
                    raise UnknownHTTPError(e)

    # Tokyo Metro open data don't suppert multi-language text.
    # So move these information to "ja".
    if distributor == Distributor.TOKYO_METRO:
        for single_dict in json_dict:
            for key in multilanguage_str_keys:
                if key in single_dict:
                    single_dict[key] = { "ja": single_dict[key] }

    return [TrainInformation(single_dict) for single_dict in json_dict]
