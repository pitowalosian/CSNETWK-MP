#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "socket.h"

int createSocket() {
	int sockfd;
	int broadcast = 1;
	WSADATA wsaData;
	
	// Initialize Winsock
	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("WSAStartup failed. Error Code: %d\n", WSAGetLastError());
        return -1;
    }
	
	sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	if (sockfd < 0) {
		printf("Socket creation failed. Error Code: %d\n", WSAGetLastError());
		WSACleanup();
		return 1;
	}
	
	// Enable broadcast
	if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, (const char *)&broadcast, sizeof(broadcast)) > 0) {
		printf("Broadcast failed. Error Code: %d\n", WSAGetLastError());
        closesocket(sockfd);
        WSACleanup();
        return 1;
	}
	
	return sockfd;
}

void bindSocket(int sockfd) {
	struct sockaddr_in addr = {0};
	
	addr.sin_family = AF_INET;
	addr.sin_port = htons(PORT);
	addr.sin_addr.s_addr = INADDR_ANY;
	
	if (bind(sockfd, (struct sockaddr *)&addr, sizeof (addr)) < 0) {
		printf("Bind failed. Error Code: %d\n", WSAGetLastError());
        closesocket(sockfd);
        WSACleanup();
        return;
	}
}

void sendMessage(int sockfd, const char* message, const char* target_ip) {
	struct sockaddr_in target = {0};
    target.sin_family = AF_INET;
    target.sin_port = htons(PORT);
	target.sin_addr.s_addr = inet_addr(target_ip);

    sendto(sockfd, message, strlen(message), 0,
           (struct sockaddr *)&target, sizeof(target));
}

void listenLoop(int sockfd) {
    char buffer[2048];
    struct sockaddr_in senderAddr;
    int addrLen = sizeof(senderAddr);

    printf("Listening for LSNP messages on port 50999...\n");

    while (1) {
        ssize_t bytesReceived = recvfrom(sockfd, buffer, sizeof(buffer) - 1, 0,
                                         (struct sockaddr*)&senderAddr, &addrLen);
        if (bytesReceived < 0) {
            perror("recvfrom failed");
            break;
        }

        buffer[bytesReceived] = '\0';  // Null-terminate the message
        printf("Received message from %s:%d\n",
               inet_ntoa(senderAddr.sin_addr), ntohs(senderAddr.sin_port));
        printf("Message:\n%s\n", buffer);

        // TODO: Call your parser here to interpret key-value LSNP message
    }
}
