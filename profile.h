#ifndef PROFILE_H
#define PROFILE_H

#define MAXSTRING 256
#define CONSTANT 50
#define MAX 2048

typedef struct {
	char type[CONSTANT];
	char userID[MAXSTRING];
	char displayName[CONSTANT];
	char status[MAXSTRING];
	char avatarType[CONSTANT];
	char avatarEncoding[CONSTANT];
	char avatarData[MAX];
	int hasAvatar;
} Profile;

Profile createProfile(const char* userID, const char* displayName, const char* status,
		const char* avatarType, const char* avatarEncoding, const char* avatarData);
		
void printVerboseProfile(Profile p);
void printSimpleProfile(Profile p);

#endif // PROFILE_H
