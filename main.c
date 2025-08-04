#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include "socket.h"       // for socket functions
#include "parse.h"            // your parseProfile(), parseDm(), etc.

#define PORT 50999
#define BUFFER_SIZE 2048

void startServer() {
    int sockfd;
    struct sockaddr_in serverAddr, clientAddr;
    int addrLen = sizeof(clientAddr);
    char buffer[BUFFER_SIZE];

    // 1. Create socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Failed to create socket");
        exit(1);
    }

    // 2. Bind to port 50999
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(PORT);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    if (bind(sockfd, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        perror("Bind failed");
        closesocket(sockfd);
        return;
    }

    printf("LSNP Server listening on port %d...\n", PORT);

    // 3. Listening loop
    while (1) {
        memset(buffer, 0, BUFFER_SIZE);
        int bytesReceived = recvfrom(sockfd, buffer, BUFFER_SIZE - 1, 0,
                                     (struct sockaddr*)&clientAddr, &addrLen);

        if (bytesReceived < 0) {
            perror("recvfrom failed");
            return;
        }

        buffer[bytesReceived] = '\0';  // Null-terminate the buffer

        // 4. Print source
        printf("\nReceived from %s:%d\n",
               inet_ntoa(clientAddr.sin_addr),
               ntohs(clientAddr.sin_port));

        // 5. Parse message type
        if (strstr(buffer, "TYPE: PROFILE")) {
            Profile p = parseProfile(buffer);
            printSimpleProfile(p);
            printVerboseProfile(p);
        }
        else if (strstr(buffer, "TYPE: DM")) {
            Dm dm = parseDm(buffer);
            printDMVerbose(dm);
            // printDMSimple(profiles, profileCount, dm); // Assuming profiles and profileCount are defined
        }
        else {
            printf("Unknown or unsupported message:\n%s\n", buffer);
        }
    }

    closesocket(sockfd);
}

int main() {
    // Initialize Winsock
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        perror("WSAStartup failed");
        return 1;
    }

    startServer();

    // Cleanup Winsock
    WSACleanup();
    return 0;
}
