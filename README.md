S-TDMA_RoutingSwitch
========
<!--
[![Build Status](http://img.shields.io/travis/Da1sukeKud0/topology/develop.svg?style=flat)][travis]
[![Code Climate](http://img.shields.io/codeclimate/github/Da1sukeKud0/topology.svg?style=flat)][codeclimate]
[![Coverage Status](http://img.shields.io/codeclimate/coverage/github/Da1sukeKud0/topology.svg?style=flat)][codeclimate]
[![Dependency Status](http://img.shields.io/gemnasium/Da1sukeKud0/topology.svg?style=flat)][gemnasium]

[travis]: https://travis-ci.org/Da1sukeKud0/topology
[codeclimate]: https://codeclimate.com/github/Da1sukeKud0/topology
[gemnasium]: https://gemnasium.com/trema/topology
-->

実行環境
-------------
* [Ruby 2.3.7][rvm] (on rvm)
* [Open vSwitch][openvswitch] (`git clone git@github.com:openvswitch/ovs.git`).  

[rvm]: https://rvm.io/
[openvswitch]: https://openvswitch.org/


インストール
-------
実行環境としてrvmによりRuby2.0.0(or 2.3.7)をインストールすることを推奨します。  
またopenvswitchはnative sourceよりインストールすることを推奨します。  
install.shを実行してください。以下と同様の作業がおこなわれます。
```
mkdir -p ~/trema
cd ~/trema
git clone https://github.com/Da1sukeKud0/S-TDMA_RoutingSwitch.git
mv S-TDMA_RoutingSwitch routing_switch
cd routing_switch
bundle install --binstubs
```
※bundle installに失敗する場合はenvironment/SETUP.mdを参照してください。

実時間通信管理機構: RTCManagerについて
----
TopologyControllerで検知したトポロジ情報と実時間通信要求(送信元/宛先および通信周期)を元にスケジューリングの可否判定および通信経路・タイムスロットの割り当てをおこなう機構です。  
Tremaを起動せずlib/rtc_manager.rbの動作テストを行う方法
```
ruby lib/test/rtc_manager_test.rb bamax
```
起動時の引数によりテストモードを指定できます。  
+ ba  
BAモデルのトポロジ(スイッチ数100,複雑度2)に対し5回の実時間通信要求を実行
+ baloop  
スイッチ数,複雑度を様々なパターンに変化させ生成したBAモデルのトポロジに対し連続した5回の実時間通信要求を実行
+ tree  
ツリートポロジ(深さ4,拡散4)に対し5回の実時間通信要求を実行
+ treeloop  
スイッチ数,複雑度を様々なパターンに変化させ生成したツリートポロジに対し連続した5回の実時間通信要求を実行
+ lineprof  
bamaxと同様のテストを実行しスクリプトの実行時間を行単位で計測

<!-- HTML CODE-->
<!--[if IE]><meta http-equiv="X-UA-Compatible" content="IE=5,IE=9" ><![endif]-->
<!DOCTYPE html>
<html>
<head>
<title>system_architecture</title>
<meta charset="utf-8"/>
</head>
<body><div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile modified=\&quot;2019-01-30T16:44:58.125Z\&quot; host=\&quot;www.draw.io\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36\&quot; etag=\&quot;3ptVO-gnCUnxk7GMQQOz\&quot; version=\&quot;10.1.6-2\&quot; type=\&quot;google\&quot;&gt;&lt;diagram id=\&quot;34816958-5deb-473d-bc54-1e750b01d824\&quot; name=\&quot;Page-1\&quot;&gt;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&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://www.draw.io/js/viewer.min.js"></script>
</body>
</html>

サポートスクリプトについて
----
BAモデルに基づくランダムトポロジの生成(標準入力よりスイッチ数と複雑さを指定)
```
util/createRandomTopology.py
```
testディレクトリに.conf、test/topo_image/にトポロジのグラフ画像が生成される。

コアトポロジ、リニアトポロジの生成(引数にスイッチ数を指定)
```
util/createLinearTopology.py 10
util/createCoreTopology.py 10
```
testディレクトリに.confが生成される。

Tremaのsend_packetsコマンドを一括実行するスクリプト(引数にホスト数と追加実行したいpacket_Inの数を指定)
```
util/send_packets.py 6 3
```

OpenFlowコントローラの使用方法
----
コントローラの起動（`-c`オプションにより任意の初期トポロジを設定）
```
./bin/trema run ./lib/routing_switch.rb -c test/linear.conf
```

スイッチの起動/停止
```
./bin/trema stop 0x1
./bin/trema start 0x1
```

スイッチポートの起動/停止
```
./bin/trema port_down --switch 0x1 --port 1
./bin/trema port_up --switch 0x1 --port 1
```

ホストをスイッチに追加（実際にはスイッチもポートも存在するが以下によるPacket_Inでリンクが検出される）
```
./bin/trema send_packets -n 1 -s h1 -d h2
```
