#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <pthread.h>
#include <arpa/inet.h>
#include <socket.h>
#include <time.h>

#include "Client.h"

int verbose = 1;

void log_debug(const char *msg) {
    if (verbose) {
        printf("[DEBUG] %s\n", msg);
    }
}

void add_peer(const char *user_id, const char *display_name) {
    for (int i = 0; i < peer_count; i++) {
        if (strcmp(known_peers[i].user_id, user_id) == 0) {
            return; // already known
        }
    }
    if (peer_count < MAX_PEERS) {
        strncpy(known_peers[peer_count].user_id, user_id, sizeof(known_peers[peer_count].user_id));
        strncpy(known_peers[peer_count].display_name, display_name, sizeof(known_peers[peer_count].display_name));
        peer_count++;
    }
}

void add_message(const char *from, const char *content, const char *type) {
    if (message_count < MAX_MESSAGES) {
        strncpy(messages[message_count].from, from, sizeof(messages[message_count].from));
        strncpy(messages[message_count].content, content, sizeof(messages[message_count].content));
        strncpy(messages[message_count].type, type, sizeof(messages[message_count].type));
        message_count++;
    }
}

void print_known_peers() {
    printf("Known Peers:\n");
    for (int i = 0; i < peer_count; i++) {
        printf("- %s (%s)\n", known_peers[i].display_name, known_peers[i].user_id);
    }
}

void print_messages() {
    printf("Messages:\n");
    for (int i = 0; i < message_count; i++) {
        printf("[%s] %s: %s\n", messages[i].type, messages[i].from, messages[i].content);
    }
}

void parse_message(const char *buffer) {
    char lines[20][256];
    int line_count = 0;

    char temp[BUF_SIZE];
    strncpy(temp, buffer, BUF_SIZE);
    char *line = strtok(temp, "\n");
    while (line != NULL && line_count < 20) {
        strncpy(lines[line_count++], line, 256);
        line = strtok(NULL, "\n");
    }

    char type[32] = "", user_id[64] = "", display_name[64] = "", content[1024] = "";

    for (int i = 0; i < line_count; i++) {
        if (strncmp(lines[i], "TYPE:", 5) == 0)
            sscanf(lines[i], "TYPE: %[^"]s", type);
        else if (strncmp(lines[i], "USER_ID:", 8) == 0)
            sscanf(lines[i], "USER_ID: %[^"]s", user_id);
        else if (strncmp(lines[i], "DISPLAY_NAME:", 13) == 0)
            sscanf(lines[i], "DISPLAY_NAME: %[^"]s", display_name);
        else if (strncmp(lines[i], "CONTENT:", 8) == 0)
            sscanf(lines[i], "CONTENT: %[^"]s", content);
    }

    if (strlen(user_id) > 0 && strlen(display_name) > 0) {
        add_peer(user_id, display_name);
    }
    if (strlen(user_id) > 0 && strlen(content) > 0) {
        add_message(user_id, content, type);
    }

    char debug_msg[BUF_SIZE];
    snprintf(debug_msg, sizeof(debug_msg), "Parsed message: TYPE=%s USER_ID=%s DISPLAY_NAME=%s CONTENT=%s",
             type, user_id, display_name, content);
    log_debug(debug_msg);
}

int sock;
struct sockaddr_in server_addr;
char user_id[64], display_name[64];

void *receive_loop(void *arg) {
    char buffer[BUF_SIZE];
    while (1) {
        socklen_t len = sizeof(server_addr);
        int n = recvfrom(sock, buffer, BUF_SIZE - 1, 0, NULL, NULL);
        if (n > 0) {
            buffer[n] = '\0';
            log_debug("Received message.");
            parse_message(buffer);
        }
        usleep(100000);
    }
    return NULL;
}

void send_profile() {
    char message[BUF_SIZE];
    snprintf(message, sizeof(message),
        "TYPE: PROFILE\nUSER_ID: %s\nDISPLAY_NAME: %s\nSTATUS: Available\n\n",
        user_id, display_name);
    sendto(sock, message, strlen(message), 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
    log_debug("Sent PROFILE.");
}

void send_post(const char *content) {
    char message[BUF_SIZE];
    snprintf(message, sizeof(message),
        "TYPE: POST\nUSER_ID: %s\nCONTENT: %s\n\n",
        user_id, content);
    sendto(sock, message, strlen(message), 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
    log_debug("Sent POST.");
}
