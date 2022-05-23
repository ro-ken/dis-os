
for((j=0;j<4;j++))
do
    nice -n -18 taskset -c $j ./main $1 &
done
python ../dis/node.py
kill -9 `pidof main`

