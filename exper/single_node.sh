mkdir ../result_exp
for((i=5;i<=20;i+=5))
do
    mkdir ../result_exp/min_$i
    for((j=1;j<=5;j++))
    do
        python ../node.py $i
        cp ../output/*_task_time.txt ../result_exp/min_$i/test_seq_$j.txt # 传输时间
        cp ../output/server_*.txt ../result_exp/min_$i/server_seq_$j.txt  # 主节点本地时间
    done
done

