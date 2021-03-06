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
