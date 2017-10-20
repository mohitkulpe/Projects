#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
void *iops(void *c);
void *gflops(void *a1);
void main()
{
 clock_t start, end;
 clock_t start1,end1;
 int i;
 long double cpu_gflops;
 long double cpu_iops;
 int nthreads;
 //long int a=5; 
 //long double flops=75;
 printf("enter the number of threads\n");
 scanf("%d",&nthreads); 
 pthread_t thread_id[nthreads];
 pthread_t thread[nthreads];
 //clock started for Gflops
 start=clock();
 
 
 for(i=0;i< nthreads;i++)
  { 
   pthread_create(&thread_id[i],NULL,&gflops,(void *)(long)nthreads); 
     
  }
 //Joining the threads to main thread
 for(i=0;i<nthreads;i++)
   {
  
  pthread_join(thread_id[i],NULL);
   }

 end=clock();
 cpu_gflops=((double) (end-start))/CLOCKS_PER_SEC;
 printf("\n Time used = %Lf ",cpu_gflops);
 double flopscpu= 10000000/ (double)cpu_gflops;
 double gflopscpu= (double)flopscpu/100000000UL;
 printf("\n Gflops : %f",gflopscpu);
 start1=clock();
 
 for(i=0;i< nthreads;i++)
  { 
   pthread_create(&thread[i],NULL,&iops,(void *)(long)nthreads); 
  }
 for(i=0;i<nthreads;i++)
   {
   pthread_join(thread[i],NULL);
   }
 end1=clock();
 cpu_iops=((double) (end1-start1))/CLOCKS_PER_SEC;
 printf("\n Time used iops = %Lf ",cpu_iops);
 double iops= 10000000/ (double)(cpu_iops);
 double giopscpu= (double)iops/100000000UL;
 printf("\n Iops : %f",giopscpu);
 }

}
void *iops(void *c)
{
 long int result;
 long int a=1;
 int it1=10000000/(int)(long)c;
 for(int j=0;j<=it1;j++)
  {
   a+=a;

  }
}
void *gflops(void *a1)
{
  double j=1.02;
  //long double flops=5;
  int it=10000000/(int)(long)a1;
  for(int i = 0; i <= it; i++)
  {
    j+=j;
  }
}




