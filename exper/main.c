 
#include <stdio.h> 
#include <stdlib.h> 
#include <time.h>
#include <unistd.h>
#include <sys/time.h>
 
int main(int argc, char ** argv) 
{ 
	int percent = 50;
	if(argc > 1)
		percent = atoi(argv[1]);
	
	printf("set cpu usage: %d%\n", percent);
	
	int worktime = percent;//ms
	int sleeptime = 100 - percent;
 
    struct timeval tv; 
    long long start_time,end_time; 
    while(1) 
    { 
        gettimeofday(&tv,NULL); 
        start_time = tv.tv_sec*1000000 + tv.tv_usec; 
        end_time = start_time; 
     
        while((end_time - start_time) < worktime * 1000) //60000
        { 
            gettimeofday(&tv,NULL); 
            end_time = tv.tv_sec*1000000 + tv.tv_usec; 
        } 
        usleep( sleeptime  *1000); //60ms
    } 
    return 0; 
} 
