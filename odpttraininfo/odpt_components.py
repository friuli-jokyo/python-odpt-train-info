from datetime import datetime
from enum import Enum
from typing import Optional, TypedDict
from uuid import UUID

MultiLanguageString = TypedDict("MultiLanguageString", {
    "ja": str,
    "en": Optional[str],
    "ko": Optional[str],
    "zh-Hans": Optional[str],
    "zh-Hant": Optional[str],
    "ja-Hrkt": Optional[str],
})

TrainInformation = TypedDict("OdptTrainInformation", {
    # Common keys
    "@context": str,
    "@id": UUID|str,
    "@type": str,
    "dc:date": datetime,
    "dct:valid": Optional[datetime],
    "odpt:operator": str,
    "odpt:timeOfOrigin": datetime,
    "odpt:railway": Optional[str],
    "odpt:trainInformationStatus": Optional[MultiLanguageString],
    "odpt:trainInformationText": MultiLanguageString,

    # Only appear in odpt-center
    "owl:sameAs": Optional[str],
    "odpt:railDirection": Optional[str],
    "odpt:trainInformationArea": Optional[MultiLanguageString],
    "odpt:trainInformationKind": Optional[MultiLanguageString],
    "odpt:stationFrom": Optional[str],
    "odpt:stationTo": Optional[str],
    "odpt:trainInformationRange": Optional[MultiLanguageString],
    "odpt:trainInformationCause": Optional[MultiLanguageString],
    "odpt:transferRailways": Optional[list[str]],
    "odpt:resumeEstimate": Optional[datetime]
})

multilanguage_str_keys = [
    "odpt:trainInformationStatus",
    "odpt:trainInformationText",
    "odpt:trainInformationArea",
    "odpt:trainInformationKind",
    "odpt:trainInformationRange",
    "odpt:trainInformationCause",
]


class Distributor(Enum):
    """Enumerates of API distributor.

    Parameters
    ----------
    Enum : str
        Value is an endpoint URL.
    """

    TOKYO_METRO = ("https://api.tokyometroapp.jp/api/v2/datapoints")
    ODPT_CENTER = ("https://api.odpt.org/api/v4/odpt:TrainInformation")

    def __init__(self, URL:str) -> None:
        self.URL = URL
        self.consumer_key: str|None = None

    def set_consumer_key(self, key: str) -> None:
        """Set consumerKey

        Parameters
        ----------
        key : str
        """

        self.consumer_key = key

    def is_valid(self) -> bool:
        """True if consumerKey is set, False otherwise.

        Returns
        -------
        bool
        """

        if self.consumer_key == None:
            return False
        else:
            return True
