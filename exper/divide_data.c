#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>

#define BUFFER_LEN 1024
#define PATH_MAX 1024
#define DIR_NAME "server_frame_time"

int out_turn = 2;
int inner_turn = 3;

char *toString(int iVal)
{

    char str[1024] = {
        '\0',
    };
    char *pos = NULL;
    int sign = 0; //正数 或者是 0

    int abs = iVal;

    pos = str + 1023; //移动指针,指向堆栈底部
    *pos-- = '\0';    // end

    if (iVal < 0)
    {
        sign = 1;
        abs = -abs;
    }

    int dit = 0;
    while (abs > 0)
    {
        dit = abs % 10;
        abs = abs / 10;

        *pos-- = (char)('0' + dit);
    }

    if (sign)
        *pos-- = '-';

    char *ret = (char *)malloc(1024 - (pos - str));

    if (iVal == 0) // 0的一个处理
        strcpy(ret, "0");
    else // iVal非0的拷贝
        strcpy(ret, pos + 1);

    return (ret);
}

char *index_filename(int index)
{
    switch (index)
    {
    case 0:
    {
        return "/min_5/";
    }
    case 1:
    {
        return "/min_10/";
    }
    case 2:
    {
        return "/min_15/";
    }
    case 3:
    {
        return "/min_20/";
    }
    }
}

int deleteAll(char *directory){
    DIR *dir = NULL;
    char dpath[PATH_MAX];
    char fpath[PATH_MAX];
    dir = opendir(directory);
    struct dirent *dirp;
    while((dirp = readdir(dir))!=NULL){
        if(dirp->d_type==DT_DIR){
            if(dirp->d_name[0]=='.'){
                continue;
            }
            snprintf(dpath,(size_t)PATH_MAX,"%s/%s",directory,dirp->d_name);
            deleteAll(dpath);
        }
        if(dirp->d_type==DT_REG){
            snprintf(fpath,(size_t)PATH_MAX,"%s/%s",directory,dirp->d_name);
            remove(fpath);
        }

    }
    closedir(dir);
    rmdir(directory);
    return 0;
}

void delete_old_dir(char *dirpath){
    int res;
     //如果文件夹存在，先删除原来文件夹
    if(access(dirpath,0)==0){
       deleteAll(dirpath);
    }
}

int main(int argc,char * argv[])
{
    char dir_name[1024] = DIR_NAME;
    strcat(dir_name,".txt");
    FILE *f = fopen(dir_name,"r");
    const char *c = ",";
    char readBuffer[BUFFER_LEN] ;
    int old = -1;
    int new;
    char tempp[1024];


    if (argc == 3){
    	out_turn = argv[1][0] - 48;
	inner_turn = argv[2][0] -48;
	printf("out:%d\n",out_turn);
	printf("inner:%d\n",inner_turn);
    }

    if (f == NULL)
    {
        printf("open file error!\n");
        exit(1);
    }
    delete_old_dir(DIR_NAME);
    mkdir(DIR_NAME,0777);
    for (int i = 0; i < out_turn; i++)
    {
        char d_name[1024] = DIR_NAME;
        strcat(d_name,index_filename(i));
        mkdir(d_name,0777);
        for (int j = 1; j <= inner_turn; j++)
        {
            char newFile[1024] = DIR_NAME;
            strcat(newFile, index_filename(i));
            char *temp = "server_seq_";
            strcat(newFile, temp);
            char *seq = toString(j);
            strcat(newFile, seq);
            strcat(newFile, ".txt");
            FILE *ff = fopen(newFile,"wt");
            fwrite(tempp, 1, strlen(tempp), ff);
            while (fgets(readBuffer, BUFFER_LEN, f) != NULL)
            {
                strcpy(tempp,readBuffer);
                char *ret = strtok(readBuffer, c);
                new = atoi(ret + 4);
                if (new > old)
                {   
                    fwrite(tempp, 1, strlen(tempp), ff);
                    memset(readBuffer, '\0', BUFFER_LEN);
                    old = new;
                }
                else
                {                    
                    old = -1;
                    memset(readBuffer, '\0', BUFFER_LEN);
                    break;
                }
               
            }
        }
   }

    return 0;
}
