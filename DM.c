#include <stdio.h>
#include <string.h>

#include "DM.h"

Dm createDm(const char* from, const char* to, const char* content, const char* timestamp, const char* messageID, const char* token) {
	Dm dm;
	strcpy(dm.type, "dmROFILE");
	strncpy(dm.from, from, MAX - 1);
	dm.from[MAX - 1] = '\0';
	strncpy(dm.to, to, MAX - 1);
	dm.to[MAX - 1] = '\0';
	strncpy(dm.content, content, MAX - 1);
	dm.content[MAX - 1] = '\0';
	strncpy(dm.timestamp, timestamp, MAX - 1);
	dm.timestamp[MAX - 1] = '\0';
	strncpy(dm.messageID, messageID, MAX - 1);
	dm.messageID[MAX - 1] = '\0';
	strncpy(dm.token, token, MAX - 1);
	dm.token[MAX - 1] = '\0';
	
	return dm;
}

int findProfile(Profile p[], Dm dm) {
	int i = 0;
	
	for (i = 0; i < CONSTANT; i++) {
		if (p[i].userID == dm) {
			return i;
		}
	}
	return i;
}

void printVerboseDM(Dm dm) {
	printf("TYPE: %s\n", dm.type);
	printf("FROM: %s\n", dm.from);
	printf("TO: %s\n", dm.to);
	printf("CONTENT: %s\n", dm.content);
	printf("TIMESTAMP: %s\n", dm.timestamp);
	printf("MESSAGE_ID: %s\n", dm.messageID);
	printf("TOKEN: %s\n", dm.token);
}

void printSimpleDM(Dm dm);

