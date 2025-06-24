#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

int sameStrings(char* s1, char* s2)
{
  char* curr1, * curr2;
  curr1 = s1;
  curr2 = s2;

  while (*s1 != '\0' || *s2 != '\0')
  {
    if (*s1 != *s2)
      return 0;

    s1++;
    s2++;
  }

  return 1;
}

int split(char*** array, char* str, char seperator)
{
  int lines = 0;
  char * ptr = str;
  while (*ptr)
  {
    if (*ptr == seperator) lines++;
    ptr++;
  }
  lines++; // for null terminator
  
  *array = malloc(sizeof(char*) * lines);

  int strIndex = 0;
  for (int line = 0; line < lines; line++)
  {
    /* For each line:
     *   Create a temp array
     *   Read until seperator or null terminator
     *   set array[line] = temp array
     */
    char* tmp = malloc(1024);
    int index = 0;
    while (1)
    {
      if (str[strIndex] == seperator || str[strIndex] == '\0')
      {
        tmp[index] = '\0';
        strIndex++;
        break;
      }
      else {
        tmp[index] = str[strIndex];     
        strIndex++;
        index++;
      }
    }
    (*array)[line] = tmp;
  }

  return lines;
}

int main()
{
  char str[] = "Hello Everybody and me!";
  char** arr;
  char seperator = ' ';

  int lines = split(&arr, str, seperator);

  for (int i = 0; i < lines; i++)
  {
    printf("%s\n", arr[i]);
    free(arr[i]);
  }
  free(arr);
  
  return 0;
}
