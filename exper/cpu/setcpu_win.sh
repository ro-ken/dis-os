
for((j=0;j<8;j++))
do
    taskset -c $j ./main $1 &
done

