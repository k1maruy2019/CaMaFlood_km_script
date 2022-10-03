#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>

/* #define XSIZE 1500
   #define YSIZE 1320 */
#define ZSIZE 1

/********************/
/*** Main Process ***/
/********************/
int main(int argc, char *argv[]){
  /*** Variable Declaration ***/
  FILE *fp;
  char indata[256], outdata[256];
  float *DATA, *DATA1; 
  int XSIZE,YSIZE;
  int i,j,k;
  int jrev;

  /*** Argument Value ***/
  if( argc < 4 ){
    fprintf( stderr, "Usage: %s [InputData] [OutputData]\n", argv[0] );
    exit(0);
  }
  sprintf(indata,"%s",argv[1]); 
  sprintf(outdata,"%s",argv[2]);
  sscanf(argv[3],"%d",&XSIZE); 
  sscanf(argv[4],"%d",&YSIZE);
  /*------------------*/
  /* Read binary data */
  /*------------------*/
  printf("Input File is %s\n", indata);
  printf("XSIZE = %d\n", XSIZE);
  printf("YSIZE = %d\n", YSIZE);
  DATA = (float *)malloc(XSIZE*YSIZE*ZSIZE*sizeof(float));
  if( DATA == NULL ){
    fprintf(stderr, "MALLOC Failure : DATA");
    exit(1);
  }
  DATA1 = (float *)malloc( sizeof(float)*XSIZE*YSIZE);
  if( DATA1 == NULL ){
    fprintf(stderr, "MALLOC Failure : DATA1");
    exit(1);
  }

  if( (fp=fopen(indata,"rb")) == NULL ){
    fprintf(stderr, "Open Error : %s\n", indata);
    exit(1);
  }
  fread(DATA1, sizeof(float), YSIZE*XSIZE, fp);
  fclose(fp);
  k=0;
  for( j=0; j<YSIZE; j++ ){
    for( i=0; i<XSIZE; i++ ){
      jrev = YSIZE - 1 - j;
      DATA[ k*XSIZE*YSIZE + jrev*XSIZE + i ]=DATA1[j*XSIZE+i];
    }
  }
  /* Reverse meridional grid */
  /*  for( j=0; j<YSIZE; j++ ){
    for( i=0; i<XSIZE; i++ ){
      jrev = YSIZE - 1 - j;
      REV[ j*XSIZE + i ] = DATA[ k*XSIZE*YSIZE + jrev*XSIZE + i ];
    }
    } */
  /* Reverse meridional grid */
  
  /*----------------*/
  /* Write data out */
  /*----------------*/
  printf("Output File is %s\n", outdata);

  if( (fp=fopen(outdata,"wb")) == NULL ){
    fprintf(stderr, "Open Error : %s\n", outdata);
    exit(1);
  }
  fwrite(DATA, sizeof(float), ZSIZE*YSIZE*XSIZE, fp);
  fclose(fp);

  /*** Finish ***/
  free(DATA);
  free(DATA1);
  return 0;
}


