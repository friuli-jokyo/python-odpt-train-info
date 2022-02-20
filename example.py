import odpttraininfo as odpt

# キャッシュの保存先を指定(デフォルトは"./__odptcache__/")
odpt.config.set_cache_dir("./path/to/cache/directory/")

# 各サービスへのconsumerKeyをセット
odpt.Distributor.ODPT_CENTER.set_consumer_key("xxxxxxxxxxxx")
odpt.Distributor.TOKYO_METRO.set_consumer_key("xxxxxxxxxxxx")

# キャッシュファイルを更新
odpt.refresh_cache()

# キャッシュから運行情報を取得
# キャッシュが生成から80秒以上経っているときはインターネットリソースから取得
info = odpt.fetch_info()
print(info)