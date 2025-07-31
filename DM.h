#ifndef DM_H
#define DM_H

#define MAXSTRING 256
#define MAX 20480
#define CONSTANT 50

typedef struct {
	char type[CONSTANT];
	char from[MAXSTRING];
	char to[MAXSTRING];
	char content[MAXSTRING];
	char timestamp[MAXSTRING];
	char messageID[MAXSTRING];
	char token[MAX];
} Dm;

Dm createDm(const char* from, const char* to, const char* content, const char* timestamp, const char* messageID, const char* token);
	
int findProfile(Profile p[], Dm dm);
void printVerboseDM(Dm dm);
void printSimpleDM(Dm dm);

#endif // DM_H
