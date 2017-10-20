

#include <stdio.h> 
#include <sys/time.h>
#include <string.h>
#include <memory.h>
#include <pthread.h>
#include <unistd.h> 
#include <stdlib.h>


#define max_size 671088640



char char1[max_size], char2[max_size];
long buffer_size, size_div;
struct timeval t;
pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;
int th;



void file()
{
  printf("\nGenerating data in the memory...");
    int i;
    for (i = 0; i < max_size; ++i)
    
    {
        char1[i]= 'A';
       
    }
}



void *read_write()
{
    long j,k;
    
    pthread_mutex_lock( &mutex1 );

      
  FILE *f = fopen("Disk_Benchmark.txt","w+");

  size_div = ((max_size/buffer_size)/th);

  for(j=0;j<size_div;j++) 
  
{ 
  fwrite(char1,buffer_size,1,f);

}

fseek(f, 0, SEEK_SET);


for(int k=0;k<size_div;k++) 
{
    fread(char2,buffer_size,1,f); 
  }

  fclose (f); 

 pthread_mutex_unlock( &mutex1 );
}


void *seq_read()
{
    //long int j, size_div;
    
    pthread_mutex_lock( &mutex1 );

        
  FILE *f = fopen("Disk_Benchmark.txt","r");

  size_div = ((max_size/buffer_size)/th);

  fseek(f, 0, SEEK_SET);
  
for(int l=0;l<size_div;l++) 
{
    fread(char2, buffer_size, 1, f); 
}

fclose (f);

 pthread_mutex_unlock( &mutex1 );
}


//Random Read
void *ran_read()
{
    long m, rr;
        
    pthread_mutex_lock( &mutex1 );

    
  FILE *f = fopen("Disk_Benchmark.txt","r");

  size_div = ((max_size/buffer_size)/th);

  for(m=0;m<size_div;m++) 

{
  rr = rand()%100;

  fseek(f,rr,SEEK_SET);
  
  fread(char2, buffer_size, 1, f);
}

 fclose (f);

 pthread_mutex_unlock( &mutex1 );
}


int main()
{
  int  a, b, choice, c, d, e, g;
  double start_th, stop_th, th_t, x, y, z;
    float th_tp[40];
     
    printf("How many Threads you want to Create 1, 2, 4 or 8\n");
    printf("Enter Number of Threads: ");
    scanf("%d",&th);
    
    pthread_t threads[th];
  printf("\nSelect Block size: \n 1. 8B\t2. 8KB\t3. 8MB\t4. 80MB");
  printf("\nEnter Your Choice: ");


      scanf("%d", &choice);

    if (choice == 1)
    {
      buffer_size = 8;
    }

    else if (choice == 2)
    {
      buffer_size = 8192;
    }
    else if (choice == 3)
    {
      buffer_size = 8388608;
    }
    else if (choice == 4)
    {
      buffer_size = 83886080;
    }
    else
    {
      printf("Wrong Choice\n");
    }
   
   printf ("\nSelected Thread(s) = %d & Block Size = %li Byte(s)\n", th, buffer_size);

   file();

       printf("\nWriting and Reading File into disk...\n");

   


// Seq Read Write
  gettimeofday(&t,NULL);
  start_th = t.tv_sec+(t.tv_usec/1000000.0);    
    for(a = 0; a < th; a++)
    {
        //printf("\nCreating Thread: %d \n\n", (j+1));
        pthread_create(&threads[a],NULL, &read_write, NULL);
    }
    for(b =0; b < th; b++)
  {
    pthread_join(threads[b], NULL);
  }
    gettimeofday(&t,NULL);
  stop_th = t.tv_sec+(t.tv_usec/1000000.0);
  th_t = stop_th - start_th;

   //printf("Time for Threads: %lf Sec\n", th_t);
   z = ((max_size)/th_t)/(1024*1024);
   
   printf("\nThroughput for Disk Read & Write: %lf MB/s\n", z);

   printf("Latency for Disk Read & Write: %lf Micro Sec.\n", (th_t/max_size)*10000000);


    sleep(1);


// Seq Disk Read
  gettimeofday(&t,NULL);
  start_th = t.tv_sec+(t.tv_usec/1000000.0);    
    for(c = 0; c < th; c++)
    {
        
        pthread_create(&threads[c],NULL, &seq_read, NULL);
    }
    for(d =0; d < th; d++)
  {
    pthread_join(threads[d], NULL);
  }
    gettimeofday(&t,NULL);
  stop_th = t.tv_sec+(t.tv_usec/1000000.0);
  th_t = stop_th - start_th;

    //printf("Time for Threads: %lf Sec\n", th_t);
    y = ((max_size)/th_t)/(1024*1024);
   
   printf("\nThroughput for Sequential Disk Read: %lf MB/s\n", y);

     printf("Latency for Sequential Disk Read: %lf Micro Sec.\n", (th_t/max_size)*10000000);

         sleep(1);



     // Random Disk Read
  gettimeofday(&t,NULL);
  start_th = t.tv_sec+(t.tv_usec/1000000.0);    
    for(e = 0; e < th; e++)
    {
        
        pthread_create(&threads[a],NULL, &ran_read, NULL);
    }
    for(g =0; g < th; g++)
  {
    pthread_join(threads[b], NULL);
  }
    gettimeofday(&t,NULL);
  stop_th = t.tv_sec+(t.tv_usec/1000000.0);
  th_t = stop_th - start_th;

    //printf("Time for Threads: %lf Sec\n", th_t);
    
    x = ((max_size)/th_t)/(1024*1024);
   
   printf("\nThroughput for Random Disk Read: %lf MB/s\n", x);

     printf("Latency for Random Disk Read: %lf Micro Sec.\n", (th_t/max_size)*10000000);

    

    return 0;
}



/* Reference:- 
               pthread:
               http://www.cs.cmu.edu/afs/cs/academic/class/15492-f07/www/pthreads.html
               https://randu.org/tutorials/threads/
               http://www.geeksforgeeks.org/multithreading-c-2/

               fwrite():
               https://www.tutorialspoint.com/c_standard_library/c_function_fwrite.htm
               http://www.tutorialdost.com/C-Programming-Tutorial/C-file-io-fread-fwrite-function.aspx

               fread():
               https://www.tutorialspoint.com/c_standard_library/c_function_memcpy.htm
               http://www.tutorialdost.com/C-Programming-Tutorial/C-file-io-fread-fwrite-function.aspx
*/