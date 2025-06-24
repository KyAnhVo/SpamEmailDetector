#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <pthread.h>

#include <sys/socket.h>
#include <sys/unistd.h>
#include <netinet/in.h>

#include <sqlite3.h>
#include <sqlite3ext.h>

#define HTTP_PORT 80
#define MAX_THREAD 64

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
int activeThreads = 0;

void* comm(void* arg)
{
  int clientSocket = * ((int*) arg);
  free(arg);

  char buffer[1024];
  read(clientSocket, buffer, sizeof(buffer));
  printf("Client says: %s\n", buffer);
  write(clientSocket, "Hello from Server!\n", 30);

  return NULL;  
}



int main(int argc, char** argv)
{
  int serverFd = socket(AF_INET, SOCK_STREAM, 0);

  struct sockaddr_in address;
  address.sin_family = AF_INET;
  address.sin_port = htons(HTTP_PORT);
  address.sin_addr.s_addr = INADDR_ANY;

  if (!bind(serverFd, (struct sockaddr*) &address, sizeof(address)))
    return 1;
  listen(serverFd, 10);

  while (1)
  {
    socklen_t addresslen = sizeof(address);
    int* newSocket = malloc(sizeof(int));
    * newSocket = accept(serverFd, (struct sockaddr*) &address, &addresslen);
    
    pthread_mutex_lock(&lock);
    if (activeThreads < MAX_THREAD)
    {
      activeThreads++;
      pthread_t tid;
      pthread_create(&tid, NULL, comm, newSocket);
      pthread_detach(tid);
    }
    else {
      write(*newSocket, "Server busy, please try again later\n", 30);
      close(*newSocket);
      free(newSocket);
    }

    pthread_mutex_unlock(&lock);
  }

  close(serverFd);
  return 0;
}
