#include <stdlib.h>
#include <stdio.h>

int main() {
    int a,i;
   
    a = 0; i = 0;
    srand(0);

    for (i=0; i<20; i++) {
      a = rand() % 2;
      printf("a = %d\n", a);
    }
}
