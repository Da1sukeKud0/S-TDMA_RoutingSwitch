def ave_number_of_executions(turn)
  # 連続実行回数=turnのとき、initial_phase=0でtrueになる場合の最短経路探索回数
  # turnが十分大きいケース(tsl=60)だと平均19.25
  # turn=5だとせいぜい10.5回程度
  number_of_executions = []
  1000.times do
    array = []
    tmp = []
    turn.times do
      period = rand(2..5)
      array.push(period)
      tmp.push(array.inject(:lcm) / period)
    end
    number_of_executions.push(tmp)
  end
  eachturn = []
  turn.times do
    eachturn.push([])
  end
  for noe in number_of_executions
    for i in Range.new(0, turn - 1)
      eachturn[i].push(noe[i])
    end
  end
  for et in eachturn
    puts 1.0 * et.inject(:+) / et.size
  end
end

if __FILE__ == $0
  ARGV[0] = 20 unless ARGV[0]
  ave_number_of_executions(ARGV[0].to_i)
end
