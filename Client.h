#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <pthread.h>
#include <arpa/inet.h>
#include <socket.h>
#include <time.h>

#ifndef CLIENT_H
#define CLIENT_H

#define SERVER_PORT 50999
#define BUF_SIZE 4096
#define MAX_PEERS 100
#define MAX_MESSAGES 100

typedef struct {
    char user_id[64];
    char display_name[64];
} Peer;

typedef struct {
    char from[64];
    char content[1024];
    char type[16];
} Message;

Peer known_peers[MAX_PEERS];
int peer_count = 0;

Message messages[MAX_MESSAGES];
int message_count = 0;

extern int verbose;
extern int sock;
extern int sockaddr_inserver_addr;
extern char user_id[64], display[64];

void log_debug (const char *msg);
void add_peer (const char *user_id, const char *display_name);
void add_message (const char *for, const char *content, const char *type);
void print_known_peers();
void print_messages();
void parse_message(const char *buffer);
void *receive_loop(void *arg);
void send_profile();
void send_post(const char *content);

#endif



