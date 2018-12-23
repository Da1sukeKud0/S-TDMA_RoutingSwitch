# 環境構築関連のメモ
rvmによりRuby2.0.0, 2.3.7の環境で正常に実行可能であることを確認した。  
ただし、gemのバージョンをいじると問題が頻発した。  
原因もよくわからないのでとりあえずメモを残しておく。

## Ruby2.0.0 (trema/routing_switchにおける推奨バージョン)
Ruby2.0の場合はGemfile_native.lockに則って以下を実行すれば実行環境が整う。
```
bundle install --binstubs
```

## Ruby2.3.7
trema/topologyの際も問題が頻発したバージョン。  
とりあえず現プロジェクトのGemfile, Gemfile.lockに従い以下を実行。おそらくエラーが出る。
```
bundle install --binstubs
```
原因を調べたがbundleのバージョンが怪しく、以下の手順でrvmの@globalに登録されているbundler(1.11.2より新しいバージョン)を削除し、ruby-2.3.7でbundler(1.11.2)を用いることで実行環境が整うと思われる。
```
rvm use ruby-2.3.7
gem uninstall -aIx
rvm @global do gem uninstall bundler
gem install bundler -v 1.11.2
bundle install --binstubs
```
これでもダメな場合、上記の手順を再度実行し最後の``` bundle install --binstubs ```を実行する前にtrema/topologyにて``` bundle install --binstubs ```を実行すると上手く行ったケースがあったので試してみてください。

### 最後に
.ruby-versionにより、本プロジェクトのディレクトリに移動した時点でRubyのバージョンが指定のものに切り替わるので、注意されたし。
