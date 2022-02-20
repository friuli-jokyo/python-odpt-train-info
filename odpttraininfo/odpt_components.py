from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from typing import Optional, TypedDict
from uuid import UUID

output_with_none: bool = False

class MultiLanguageString():

    ja: str
    """Japanese"""
    en: Optional[str] = None
    """English"""
    ko: Optional[str] = None
    """Korean"""
    zh_hans: Optional[str] = None
    """Simplified Chinese"""
    zh_hant: Optional[str] = None
    """Traditional Chinese"""
    ja_hrkt: Optional[str] = None
    """Japanese Hiragana/Katakana (no kanji)"""

    def __init__(self, dic:dict[str,str]) -> None:
        self.ja = dic["ja"]
        if "en" in dic: self.en = dic["en"]
        if "ko" in dic: self.ko = dic["ko"]
        if "zh-Hans" in dic: self.zh_hans = dic["zh-Hans"]
        if "zh-Hant" in dic: self.zh_hant = dic["zh-Hant"]
        if "ja-Hrkt" in dic: self.ja_hrkt = dic["ja-Hrkt"]

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            return self.to_dict() == __o.to_dict()
        if __o == None:
            return False
        raise NotImplementedError

    def to_dict(self) -> dict[str,str]:
        result:dict[str,str] = {}
        result["ja"] = self.ja
        if self.en: result["en"] = self.en
        if self.ko: result["ko"] = self.ko
        if self.zh_hans: result["zh-Hans"] = self.zh_hans
        if self.zh_hant: result["zh-Hant"] = self.zh_hant
        if self.ja_hrkt: result["ja-Hrkt"] = self.ja_hrkt
        return result

_TrainInfo_json_required = TypedDict("OdptTrainInformation", {
    # Common keys
    "@context": str,
    "@id": str,
    "@type": str,
    "dc:date": str,
    "odpt:operator": str,
    "odpt:trainInformationText": dict[str,str]
})

_TrainInfo_json_optional = TypedDict("OdptTrainInformation", {
    # Common keys
    "dct:valid": str,
    "odpt:timeOfOrigin": str, # Required in both distributor, but sometimes missing.
    "odpt:railway": str,
    "odpt:trainInformationStatus": dict[str,str],

    # Only appear in odpt-center
    "owl:sameAs": str,
    "odpt:railDirection": str,
    "odpt:trainInformationArea": dict[str,str],
    "odpt:trainInformationKind": dict[str,str],
    "odpt:stationFrom": str,
    "odpt:stationTo": str,
    "odpt:trainInformationRange": dict[str,str],
    "odpt:trainInformationCause": dict[str,str],
    "odpt:transferRailways": list[str],
    "odpt:resumeEstimate": str
}, total=False)

_TrainInfo_attribute2key:dict[str,str] = {
    # Common
    "context": "@context",
    "id": "@id",
    "type": "@type",
    "date": "dc:date",
    "valid": "dct:valid",
    "operator": "odpt:operator",
    "time_of_origin": "odpt:timeOfOrigin",
    "railway": "odpt:railway",
    "train_information_status": "odpt:trainInformationStatus",
    "train_information_text": "odpt:trainInformationText",

    # Only ODPT-center
    "same_as": "owl:sameAs",
    "rail_direction": "odpt:railDirection",
    "train_information_area": "odpt:trainInformationArea",
    "train_information_kind": "odpt:trainInformationKind",
    "station_from": "odpt:stationFrom",
    "station_to": "odpt:stationTo",
    "train_information_range": "odpt:trainInformationRange",
    "train_information_cause": "odpt:trainInformationCause",
    "transfer_railways": "odpt:transferRailways",
    "resume_estimate": "odpt:resumeEstimate"
}

_TrainInfo_key2attribute:dict[str,str] = {
    _TrainInfo_attribute2key[key]:key for key in _TrainInfo_attribute2key
}

def to_json_default(o: object):
    if isinstance(o, MultiLanguageString):
        return o.to_dict()
    if isinstance(o, TrainInformation):
        return o.to_dict()
    if isinstance(o, datetime):
        return o.isoformat()
    if isinstance(o, UUID):
        return o.urn
    raise TypeError( repr(o) + " is not serializable." )

class TrainInformation_jsondict(_TrainInfo_json_required, _TrainInfo_json_optional):
    pass

class TrainInformation():

    # Common
    context: str
    id: UUID|str
    type: str
    date: datetime
    valid: Optional[datetime] = None
    operator: str
    time_of_origin: Optional[datetime] = None # Required in both distributor, but sometimes missing.
    railway: Optional[str] = None
    train_information_status: Optional[MultiLanguageString] = None
    train_information_text: MultiLanguageString

    # Only ODPT-center
    same_as: Optional[str] = None
    rail_direction: Optional[str] = None
    train_information_area: Optional[MultiLanguageString] = None
    train_information_kind: Optional[MultiLanguageString] = None
    station_from: Optional[str] = None
    station_to: Optional[str] = None
    train_information_range: Optional[MultiLanguageString] = None
    train_information_cause: Optional[MultiLanguageString] = None
    transfer_railways: Optional[list[str]] = None
    resume_estimate: Optional[datetime] = None

    def __init__(self, dic:TrainInformation_jsondict|dict[str,object]) -> None:

        for key in dic:
            if key in _TrainInfo_key2attribute:
                attribute = _TrainInfo_key2attribute[key]
                match dic[key]:
                    case str(value):
                        try:
                            date_time = datetime.fromisoformat(value)
                            self.__setattr__(attribute,date_time)
                            continue
                        except ValueError:
                            pass
                        try:
                            # @id
                            uuid = UUID(value)
                            self.__setattr__(attribute,uuid)
                            continue
                        except ValueError:
                            pass
                        self.__setattr__(attribute,value)
                    case list(value):
                        # odpt:transferRailways
                        self.__setattr__(attribute,value)
                    case dict(value):
                        multi_lang = MultiLanguageString(value)
                        self.__setattr__(attribute,multi_lang)
                    case None:
                        self.__setattr__(attribute,None)
                    case _:
                        ValueError("Dictionary has invalid type object.")
            else:
                raise RuntimeWarning("Dictionary has unknown key '%s'." % key)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            for attribute in _TrainInfo_attribute2key.keys():
                if attribute in ["id","date","valid","time_of_origin"]:
                    continue
                if self.__getattribute__(attribute) != __o.__getattribute__(attribute):
                    return False
            return True
        if __o == None:
            return False
        raise NotImplementedError

    @classmethod
    def from_jsonlist(cls, string:str) -> list[TrainInformation]:

        dic = json.loads(string)
        return cls.from_list(dic)

    @classmethod
    def from_list(cls, list_: list[dict[str,object]|TrainInformation_jsondict]) -> list[TrainInformation]:

        return [TrainInformation(single) for single in list_]

    @classmethod
    def list_diff(cls, new: list[TrainInformation], old: list[TrainInformation]) -> tuple[list[TrainInformation], list[TrainInformation]]:

        added = [info_new for info_new in new if info_new not in old]
        removed = [info_old for info_old in old if info_old not in new]

        return added, removed

    def to_dict(self) -> dict[str,object]:

        result:dict[str,object] = {}

        for attribute in _TrainInfo_attribute2key:
            key = _TrainInfo_attribute2key[attribute]
            value = self.__getattribute__(attribute)
            if output_with_none or value != None:
                if isinstance(value, MultiLanguageString):
                    result[key] = value.to_dict()
                    continue
                result[key] = value

        return result

    def to_json(self, indent: int|None = None) -> str:

        dic = self.to_dict()
        return json.dumps(dic, default=to_json_default, indent=indent)

    def get_company(self) -> str:
        """Return ID of company.

        Returns
        -------
        str
            Company ID like "TWR"
        """

        return self.operator.replace("odpt.Operator:","")

    def get_line(self) -> str:
        """Return ID of line or company.

        Returns
        -------
        str
            Line ID like "TWR.Rinkai" basically.
            Company ID if information is about whole of railway company.

        Raises
        ------
        ValueError
            If there is no information of line or company.
        """

        if self.same_as:
            return self.same_as.replace("odpt.TrainInformation:","")
        if self.railway:
            return self.railway.replace("odpt.Railway:","")
        if self.operator:
            return self.operator.replace("odpt.Operator:","")
        raise ValueError("Can't find Line or Company.")

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
