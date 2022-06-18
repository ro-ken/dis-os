mkdir ../result_exp
for((i=5;i<=30;i+=5))
do
    mkdir ../result_exp/min_$i
    for((j=1;j<=10;j++))
    do
        python ../node.py $i
        cp ../output/*_task_time.txt ../result_exp/min_$i/test_seq_$j.txt
    done
done

