
for((i=0;i<=100;i+=10))
do
    for((j=0;j<4;j++))
    do
        nice -n -18 taskset -c $j ./main $i &
    done
    python ../exper_test.py $i
    kill -9 `pidof main`
done