#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "profile.h"
#include "DM.h"

Dm createDm(const char *from, const char *to, const char *content,
	const char *timestamp, const char *messageID, const char *token) {
	Dm dm;
	strcpy(dm.type, "DM");
	strncpy(dm.from, from, MAX_STRING_SIZE - 1); dm.from[MAX_STRING_SIZE - 1] = '\0';
	strncpy(dm.to, to, MAX_STRING_SIZE - 1); dm.to[MAX_STRING_SIZE - 1] = '\0';
	strncpy(dm.content, content, MAX_STRING_SIZE - 1); dm.content[MAX_STRING_SIZE - 1] = '\0';
	strncpy(dm.timestamp, timestamp, MAX_STRING_SIZE - 1); dm.timestamp[MAX_STRING_SIZE - 1] = '\0';
	strncpy(dm.messageID, messageID, MAX_STRING_SIZE - 1); dm.messageID[MAX_STRING_SIZE - 1] = '\0';
	strncpy(dm.token, token, MAX_STRING_SIZE - 1); dm.token[MAX_STRING_SIZE - 1] = '\0';

	return dm;
}

void printDMVerbose(Dm dm) {
	printf("TYPE: %s\n", dm.type);
	printf("FROM: %s\n", dm.from);
	printf("TO: %s\n", dm.to);
	printf("CONTENT: %s\n", dm.content);
	printf("TIMESTAMP: %s\n", dm.timestamp);
	printf("MESSAGE_ID: %s\n", dm.messageID);
	printf("TOKEN: %s\n", dm.token);
}

int findProfileIndex(Profile p[], int profileCount, const char *userID) {
	for (int i = 0; i < profileCount; i++) {
		if (strcmp(p[i].userID, userID) == 0) {
			return i;
		}
	}
	return -1; // not found
}

void printDMSimple(Profile profiles[], int profileCount, Dm dm) {
	int fromIdx = findProfileIndex(profiles, profileCount, dm.from);
	int toIdx = findProfileIndex(profiles, profileCount, dm.to);

	if (fromIdx == -1 || toIdx == -1) {
		printf("Unknown user(s) in DM.\n");
		return;
	}

	if (strlen(profiles[fromIdx].displayName) == 0) {
		printf("FROM: %s\n", profiles[fromIdx].userID);
	} else {
		printf("FROM: %s\n", profiles[fromIdx].displayName);
	}

	if (strlen(profiles[toIdx].displayName) == 0) {
		printf("TO: %s\n", profiles[toIdx].userID);
	} else {
		printf("TO: %s\n", profiles[toIdx].displayName);
	}

	printf("CONTENT: %s\n", dm.content);

	if (profiles[fromIdx].hasAvatar) {
		printf("AVATAR_TYPE: %s\n", profiles[fromIdx].avatarType);
		printf("AVATAR_ENCODING: %s\n", profiles[fromIdx].avatarEncoding);
		printf("AVATAR_DATA: %s\n", profiles[fromIdx].avatarData);
	} else if (profiles[toIdx].hasAvatar) {
		printf("AVATAR_TYPE: %s\n", profiles[toIdx].avatarType);
		printf("AVATAR_ENCODING: %s\n", profiles[toIdx].avatarEncoding);
		printf("AVATAR_DATA: %s\n", profiles[toIdx].avatarData);
	}
}