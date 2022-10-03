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
  float *DATA, *DATA1, *DATA_DOWN; 
  int XSIZE,YSIZE;
  int XSIZE_DOWN,YSIZE_DOWN;
  double X,Y;
  double DX,X0;
  double DY,Y0;
  double DX_DOWN,X0_DOWN;
  double DY_DOWN,Y0_DOWN;
  int i_DOWN,j_DOWN;
  int i,j,k;
  int jrev;

  /*** Argument Value ***/
  if( argc < 2 ){
    fprintf( stderr, "Usage: %s [InputData] [OutputData]\n", argv[0] );
    exit(0);
  }
  sprintf(indata,"%s",argv[1]); 
  sprintf(outdata,"%s",argv[2]);
  /* original
  sscanf(argv[3],"%d",&XSIZE); 
  sscanf(argv[4],"%d",&YSIZE);
   upscaled grid 
  sscanf(argv[5],"%d",&XSIZE_DOWN); 
  sscanf(argv[6],"%d",&YSIZE_DOWN);
  */
  /*------------------*/
  /* Read binary data */
  /*------------------*/
  XSIZE_DOWN=1500;  
  YSIZE_DOWN=1320;  
  X0_DOWN=123;
  Y0_DOWN=24;
  XSIZE=65;
  YSIZE=56;
  X0=122;
  Y0=23.8;
  printf("Input File is %s\n", indata);
  printf("XSIZE = %d\n", XSIZE);
  printf("YSIZE = %d\n", YSIZE);
  printf("XSIZE_DOWN = %d\n", XSIZE_DOWN);
  printf("YSIZE_DOWN = %d\n", YSIZE_DOWN);

  /*
  DATA = (float *)malloc(XSIZE*YSIZE*ZSIZE*sizeof(float));
  if( DATA == NULL ){
    fprintf(stderr, "MALLOC Failure : DATA");
    exit(1);
  }
  */
  DATA1 = (float *)malloc( sizeof(float)*XSIZE*YSIZE);
  if( DATA1 == NULL ){
    fprintf(stderr, "MALLOC Failure : DATA1");
    exit(1);
  }
  DATA_DOWN = (float *)malloc( sizeof(float)*XSIZE_DOWN*YSIZE_DOWN);
  if( DATA_DOWN == NULL ){
    fprintf(stderr, "MALLOC Failure : DATA_DOWN");
    exit(1);
  }

  if( (fp=fopen(indata,"rb")) == NULL ){
    fprintf(stderr, "Open Error : %s\n", indata);
    exit(1);
  }
  fread(DATA1, sizeof(float), YSIZE*XSIZE, fp);
  fclose(fp);
  /*
  k=0;
  for( j=0; j<YSIZE; j++ ){
    for( i=0; i<XSIZE; i++ ){
      jrev = YSIZE - 1 - j;
      DATA[ k*XSIZE*YSIZE + jrev*XSIZE + i ]=DATA1[j*XSIZE+i];
    }
  }
  */
  k=0;
  DX_DOWN=1.0/60.0;
  DX=0.4;
  DY_DOWN=1.0/60.0;
  DY=0.4;
  i=0;
  j=0;
  for( j_DOWN=0; j_DOWN<YSIZE_DOWN; j_DOWN++ ){
    Y=Y0_DOWN+DY_DOWN*((double)j_DOWN+0.5);
    j=(Y-Y0)/DY;
    /*    j=(Y-Y0)/DY+1.0;
	  if( Y == Y0+(j-1)*DY ) { j=j-1; } */
    /* printf("Y=%lf j=%d\n",Y,j); */
    for( i_DOWN=0; i_DOWN<XSIZE_DOWN; i_DOWN++ ){
      X=X0_DOWN+DX_DOWN*((double)i_DOWN+0.5);
      i=(X-X0)/DX; 
/*      i=(X-X0)/DX+1.0;
	if( X == X0+(i-1)*DX ) { i=i-1; } */
      /*      printf("X=%lf i=%d\n",X,i); */
      DATA_DOWN[j_DOWN*XSIZE_DOWN+i_DOWN]=DATA1[j*XSIZE+i];
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
  fwrite(DATA_DOWN, sizeof(float), ZSIZE*YSIZE_DOWN*XSIZE_DOWN, fp);
  fclose(fp);

  /*** Finish ***/
  /*  free(DATA);*/
  free(DATA1);
  free(DATA_DOWN);
  return 0;
}


