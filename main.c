#include <stdio.h>
#include "socket.h"

int main() {
    int sockfd = createSocket();
    if (sockfd < 0) {
        fprintf(stderr, "Failed to create socket.\n");
        return 1;
    }

    bindSocket(sockfd);

    // Test: Send a message to yourself (loopback)
    const char* testMessage = "TYPE:LSNP\nUSER_ID:user123\nDISPLAY_NAME:Test User\nSTATUS:Online\n";
    const char* targetIP = "127.0.0.1";
    printf("Sending test message to %s...\n", targetIP);
    sendMessage(sockfd, testMessage, targetIP);

    printf("Listening for incoming messages on port %d...\n", PORT);
    listenLoop(sockfd);

    closesocket(sockfd);
    WSACleanup();
    return 0;
}