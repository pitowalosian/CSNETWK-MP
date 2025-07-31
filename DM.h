#ifndef DM_H
#define DM_H

#define MAX_STRING_SIZE 256
#define MAX_PROFILES 10

#include "profile.h"

typedef struct {
	char type[50];
	char from[MAX_STRING_SIZE];
	char to[MAX_STRING_SIZE];
	char content[MAX_STRING_SIZE];
	char timestamp[MAX_STRING_SIZE];
	char messageID[MAX_STRING_SIZE];
	char token[MAX_STRING_SIZE];
} Dm;

Dm createDm(const char *from, const char *to, const char *content,
	const char *timestamp, const char *messageID, const char *token);
void printDMVerbose(Dm dm);
int findProfileIndex(Profile p[], int profileCount, const char *userID);
void printDMSimple(Profile profiles[], int profileCount, Dm dm);

#endif // DM_H