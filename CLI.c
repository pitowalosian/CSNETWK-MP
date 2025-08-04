#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "socket.h"
#include "DM.h"

char* createProfileMessage(const char* userID, const char* displayName,
                           const char* status, const char* avatarType,
                           const char* avatarEncoding, const char* avatarData) {
    char* buffer = (char*)malloc(2048); // adjust size as needed
    if (!buffer) return NULL;

    sprintf(buffer,
        "TYPE: PROFILE\n"
        "USER_ID: %s\n"
        "DISPLAY_NAME: %s\n"
        "STATUS: %s\n",
        userID, displayName, status
    );

    // Optional avatar fields
    if (avatarType && avatarEncoding && avatarData) {
        strcat(buffer, "AVATAR_TYPE: ");
        strcat(buffer, avatarType);
        strcat(buffer, "\n");

        strcat(buffer, "AVATAR_ENCODING: ");
        strcat(buffer, avatarEncoding);
        strcat(buffer, "\n");

        strcat(buffer, "AVATAR_DATA: ");
        strcat(buffer, avatarData);
        strcat(buffer, "\n");
    }

    return buffer;
}

void handleProfileChoice() {
    int sockfd = createSocket();
    char userID[100], displayName[100], status[200], avatarType[100], avatarEncoding[100], avatarData[500];
    char* msg;
    printf("Enter your USER_ID: ");
    fgets(userID, sizeof(userID), stdin);
    userID[strcspn(userID, "\r\n")] = 0;

    printf("Enter your DISPLAY_NAME: ");
    fgets(displayName, sizeof(displayName), stdin);
    displayName[strcspn(displayName, "\r\n")] = 0;

    printf("Enter your STATUS: ");
    fgets(status, sizeof(status), stdin);
    status[strcspn(status, "\r\n")] = 0;

    printf("Enter your AVATAR_TYPE (press enter if none): ");
    fgets(avatarType, sizeof(avatarType), stdin);
    avatarType[strcspn(avatarType, "\r\n")] = 0;

    if (avatarType[0] != '\0') {
        printf("Enter your AVATAR_ENCODING (press enter if none): ");
        fgets(avatarEncoding, sizeof(avatarEncoding), stdin);
        avatarEncoding[strcspn(avatarEncoding, "\r\n")] = 0;

        printf("Enter your AVATAR_DATA (press enter if none): ");
        fgets(avatarData, sizeof(avatarData), stdin);
        avatarData[strcspn(avatarData, "\r\n")] = 0;
        msg = createProfileMessage(userID, displayName, status, avatarType, avatarEncoding, avatarData);
    } else {
        avatarType[0] = '\0';
        avatarEncoding[0] = '\0';
        avatarData[0] = '\0';
        msg = createProfileMessage(userID, displayName, status, NULL, NULL, NULL);
    }
    if (!msg) {
        printf("Failed to create PROFILE message.\n");
        return;
    }

    // Send message via UDP (reuse code from earlier)
    if (sockfd < 0) {
        perror("socket");
        free(msg);
        return;
    }

    int broadcast = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, (const char*)&broadcast, sizeof(broadcast));

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(50999);
    addr.sin_addr.s_addr = inet_addr("255.255.255.255");

    sendto(sockfd, msg, strlen(msg), 0, (struct sockaddr*)&addr, sizeof(addr));
    printf("PROFILE message sent.\n");

    free(msg);
}

int printMenu() {
    printf("C:\\User\\User\\Desktop\\CLI> ");

    char input[100];
    if (fgets(input, sizeof(input), stdin) == NULL) {
        return 0;
    }

    // Remove trailing newline
    input[strcspn(input, "\r\n")] = 0;

    // If input is empty after removing newline, call printMenu again
    if (strlen(input) == 0) {
        printMenu();
        return 0;
    }

    if (strcmp(input, "help") == 0) {
        printf("Available commands:\n");
        printf("help - Show this menu\n");
        printf("exit - Exit the CLI\n");
        printf("verbose - Show verbose information\n");
        printf("simple - Show simple information\n");
        printf("PROFILE - Create a profile\n");
        printf("POST - Post a message\n");
        printf("DM - Send a direct message\n");
        return 0; // Continue in CLI
    } else if (strcmp(input, "PROFILE") == 0) {
        printf("Connecting to server...\n");
        handleProfileChoice();
        return 0;
    } else if (strcmp(input, "exit") == 0) {
        printf("Exiting CLI...\n");
        return 1; // Signal to main to exit
    } else if (strcmp(input, "DM") == 0) {
        Dm dm = createDm("11", "22", "Hello", "2023-10-01T12:00:00Z", "msg123", "token123");
        return 0;
    } else if (strcmp(input, "verbose") == 0) { 
        printf("Unknown command: %s\n", input);
    }
    return 0;
}

int main() {
    int exit = 0;

    while (!exit) {
        exit = printMenu();
    }
    return 0;
}
