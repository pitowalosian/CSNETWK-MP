#ifndef SOCKET_H
#define SOCKET_H

#define PORT 50999
#define MAXBUF 65536

#include <winsock2.h>
#include "parse.h"

int createSocket();
void bindSocket(int sockfd);
void sendMessage(int sockfd, const char* message, const char* target_ip);
void listenLoop(int sockfd);

#endif // SOCKET_H