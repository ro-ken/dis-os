mkdir ../result_exp
for((i=5;i<=20;i+=5))
do
    mkdir ../result_exp/min_$i
    for((j=1;j<=3;j++))
    do
        if [ $i -eq 5 ];then
	echo 'i == 5'
        python ../node.py $i 108.5
	elif [ $i -eq 10 ]; then
	python ../node.py $i 108.82
	echo 'i == 10 down'
        elif [ $i -eq 15 ]; then
	python ../node.py $i 111.3
	echo 'i == 15 done'
	else
        python ../node.py $i 111.52
	echo 'i == 20 done'
	fi
      #  python ../node.py $i
        cp ../output/smp_frame_task_time.txt ../result_exp/min_$i/smp_seq_$j.txt
        cp ../output/smp2_frame_task_time.txt ../result_exp/min_$i/smp2_seq_$j.txt
        cp ../output/server_*.txt ../result_exp/min_$i/server_seq_$j.txt  # 主节点本地时间
    done
done
