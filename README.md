# python-odpt-train-info
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

ODPT形式で提供される鉄道運行情報を集約して提供するモジュールです。
ダウンロードした運行情報をキャッシュとして保存することで、短時間に多数のAPIアクセスが発生するのを防ぎます。

## Support APIs

公共交通オープンデータセンター https://developer.odpt.org/ja/info<br>
東京メトロオープンデータ https://developer.tokyometroapp.jp/

## Installation

このリポジトリを直接インストールします。
```bash
pip install git+https://github.com/friuli-jokyo/python-odpt-train-info
```

## Example

ソースコードは[/example.py](/example.py)に記載。

```python
>>> import odpttraininfo as odpt

# キャッシュの保存先を指定(デフォルトは"./__odptcache__/")
>>> odpt.config.set_cache_dir("./path/to/cache/directory/")

# 各サービスへのconsumerKeyをセット
>>> odpt.Distributor.ODPT_CENTER.set_consumer_key("xxxxxxxxxxxx")
>>> odpt.Distributor.TOKYO_METRO.set_consumer_key("xxxxxxxxxxxx")

# キャッシュファイルを更新
>>> odpt.refresh_cache()

# キャッシュから運行情報を取得
# キャッシュが生成から80秒以上経っているときはインターネットリソースから取得
>>> info = odpt.fetch_info()
>>> print(info[0].to_json(indent=4))
{
    "@id": "urn:uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "@type": "odpt:TrainInformation",
    "dc:date": "0000-00-00T00:00:00+09:00",
    "@context": "http://vocab.odpt.org/context_odpt.jsonld",
    "dct:valid": "0000-00-00T00:00:00+09:00",
    "owl:sameAs": "odpt.TrainInformation:TWR.Rinkai",
    "odpt:railway": "odpt.Railway:TWR.Rinkai",
    "odpt:operator": "odpt.Operator:TWR",
    "odpt:trainInformationText": {
        "ja": "平常通り運転しています。"
    }
}
>>> print(info[0].train_information_text.ja)
平常通り運転しています。
>>> print(info[0].train_information_status)
None

# 時刻とUUIDはオブジェクトとして格納されます
>>> print(info[0].date.date())
000-00-00
```

## Important Notes

公共交通オープンデータセンターからの情報において他言語に対応しているキー(`odpt:trainInformationText`,`odpt:trainInformationStatus`など)は、東京メトロオープンデータにおいて日本語テキストのみ配信されていますが、後者をキー`ja`に移動しています。以下に例を示しています。

Some keys of data (which have multi-language expression at ODPT-center, e.g.`odpt:trainInformationText`,`odpt:trainInformationStatus`) only have Japanese text at Tokyo Metro open data, so these data are moved to key `ja`. An example is below.


東京メトロオープンデータから配信される生のデータ例
Example raw data from Tokyo Metro Open data.
```json
{
    "@context": "http://vocab.tokyometroapp.jp/context_odpt_TrainInformation.json",
    "@id": "urn:ucode:_00000000000000000000000000000000",
    "dc:date": "0000-00-00T00:00:00+00:00",
    "dct:valid": "0000-00-00T00:00:00+00:00",
    "odpt:operator": "odpt.Operator:TokyoMetro",
    "odpt:railway": "odpt.Railway:TokyoMetro.Fukutoshin",
    "odpt:timeOfOrigin": "0000-00-00T00:00:00+00:00",
    "odpt:trainInformationText": "現在、平常どおり運転しています。",
    "@type": "odpt:TrainInformation"
}
```

当ライブラリで取得できるデータ例
Example data from this library.
```json
{
    "@context": "http://vocab.tokyometroapp.jp/context_odpt_TrainInformation.json",
    "@id": "urn:ucode:_00000000000000000000000000000000",
    "dc:date": "0000-00-00T00:00:00+00:00",
    "dct:valid": "0000-00-00T00:00:00+00:00",
    "odpt:operator": "odpt.Operator:TokyoMetro",
    "odpt:railway": "odpt.Railway:TokyoMetro.Fukutoshin",
    "odpt:timeOfOrigin": "0000-00-00T00:00:00+00:00",
    "odpt:trainInformationText":{
        "ja": "現在、平常どおり運転しています。"
    },
    "@type": "odpt:TrainInformation"
}
```

## License

[MIT](LICENSE)