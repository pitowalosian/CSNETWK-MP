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
	char buffer[MAXBUF];
	struct sockaddr_in sender;
	int addrlen = sizeof(sender);
	
	while(1) {
		ssize_t recvlen = recvfrom(sockfd, buffer, MAXBUF - 1, 0,
							(struct sockaddr *)&sender, &addrlen);
		if (recvlen > 0) {
			buffer[recvlen] = '\0';
			printf("Received from %s:\n%s\n", inet_ntoa(sender.sin_addr), buffer);
			
			if (strstr(buffer, "TYPE: LNSP")) {
				Profile p = parseProfile(buffer);
				printVerboseProfile(p);
			}
		}
	}
}