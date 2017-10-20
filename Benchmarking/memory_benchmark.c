
#include <stdio.h> 
#include <sys/time.h>
#include <string.h>
#include <memory.h>
#include <pthread.h>
#include <unistd.h> 
#include <stdlib.h>


char char1[419430400], char2[419430400], char3[419430400];
long max = 419430400, load_div, buffer_size;

/*char char1[838860800], char2[838860800], char3[838860800];
long max = 838860800, load_div, buffer_size;*/

struct timeval t;
pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;



void file(long max)
{
  printf("\nGenerating file in Memory...\n");
    int i;
    for (i = 0; i < max; ++i)
    
    {
        char1[i]= 'A';
       
    }
}


void *seq_write()
{
    
    long sw;
    pthread_mutex_lock( &mutex1 );

        
  for(sw = 0; sw < load_div; sw+= buffer_size)

    strncpy(char2, char1, buffer_size);

  pthread_mutex_unlock( &mutex1 );
}



void *ran_write()
{
    long rw1, rw2;
    
    pthread_mutex_lock( &mutex1 );

    for (rw1 = 0;rw1 < load_div; rw1 += buffer_size)
    { 
        rw2 = rand()% 100;
        strncpy(&char2[rw2], &char1[rw2], buffer_size);
    }
    pthread_mutex_unlock( &mutex1 );
}



void *read_write()
{
    
    long r, w;
    pthread_mutex_lock( &mutex1 );

    for(r = 0; r < load_div; r += buffer_size)
        memcpy(char2, char1, buffer_size);

    for(w = 0; w < load_div; w += buffer_size)
        strncpy(char3, char2, buffer_size);

    pthread_mutex_unlock(&mutex1);
}



int main()
{
  int th, a, b, c, d, e, g, choice;
  double start_th, stop_th, th_t, x, y, z;
    float th_tp[40];
     
    printf("\nHow many Threads you want to Create 1, 2, 4 or 8");
    printf("\nEnter Number of Threads: ");
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
   
   printf ("\nSelected Thread(s) = %d & Block Size = %li Byte(s)", th, buffer_size);

   file(max);

   load_div = max/th;




// Seq Write
  gettimeofday(&t,NULL);
  start_th = t.tv_sec+(t.tv_usec/1000000.0); 

    for(a = 0; a < th; a++)
    {
        pthread_create(&threads[a],NULL, &seq_write, NULL);
    }

    for(b =0; b < th; b++)
  {
    pthread_join(threads[b], NULL);
  }
    gettimeofday(&t,NULL);

  stop_th = t.tv_sec+(t.tv_usec/1000000.0);

  th_t = stop_th - start_th;

    //printf("Time for Threads: %lf Sec\n", th_t);

    z = (max/th_t)/(1024*1024);

    printf("\nThroughput for Sequential Memory Write: %lf MB/s", z);

    printf("\nLatency for Sequential Memory Write: %lf Micro Sec.\n", (th_t/max)*10000000);
   
   sleep(1);




   // Rand Write
    gettimeofday(&t, NULL);
    start_th = t.tv_sec+(t.tv_usec/1000000.0);

    for(c = 0; c < th; c++)
    {
        //printf("\nCreating Thread: %d \n\n", (l+1));
        pthread_create(&threads[a],NULL, &ran_write, NULL);
    }
    for(d =0; d < th; d++)
  {
    pthread_join(threads[d], NULL);
  }
    gettimeofday(&t, NULL);
  stop_th = t.tv_sec+(t.tv_usec/1000000.0);
  th_t = stop_th - start_th;

    //printf("Time for Threads: %lf Sec\n", th_t);
    y =(max/th_t)/(1024*1024);

    printf("\nThroughput for Random Memory Write: %lf MB/s", y);

    printf("\nLatency for Random Memory Write: %lf Micro Sec.\n", (th_t/max)*10000000);

    sleep(1);



    // Read Write
    gettimeofday(&t, NULL);
  start_th = t.tv_sec+(t.tv_usec/1000000.0);

    for( e=0; e<th; e++)
    {
        
        pthread_create(&threads[a],NULL, &read_write, NULL);
    } 

    for(g =0; g < th; g++)
   {
    pthread_join(threads[g], NULL);
  }
    gettimeofday(&t, NULL);
  stop_th = t.tv_sec+(t.tv_usec/1000000.0);
  th_t = stop_th - start_th;

   // printf("Time for Threads: %lf Sec\n", th_t);
    
    x = (max/th_t)/(1024*1024);

    printf("\nThroughput for Memory Read & Write: %lf MB/s", x);

    printf("\nLatency for Memory Read & Write: %lf Micro Sec.\n", (th_t/max)*10000000);

  
    
    return 0;
}


/* Reference:- 
               pthread:
               http://www.cs.cmu.edu/afs/cs/academic/class/15492-f07/www/pthreads.html
               https://randu.org/tutorials/threads/
               http://www.geeksforgeeks.org/multithreading-c-2/

               strncpy():
               https://www.tutorialspoint.com/c_standard_library/c_function_strncpy.htm
               https://www.programiz.com/c-programming/library-function/string.h/strcpy
               http://fresh2refresh.com/c-programming/c-strings/c-strncpy-function/

               memcpy():
               https://www.tutorialspoint.com/c_standard_library/c_function_memcpy.htm
               https://www.techonthenet.com/c_language/standard_library_functions/string_h/memcpy.php
               https://linux.die.net/man/3/memcpy
*/