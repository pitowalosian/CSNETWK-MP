#include <stdio.h>
#include <string.h>

#include "profile.h"

Profile createProfile(const char* userID, const char* displayName, const char* status,
		const char* avatarType, const char* avatarEncoding, const char* avatarData) {
	Profile p;
	strcpy(p.type, "PROFILE");
	strncpy(p.userID, userID, MAX - 1);
	p.userID[MAX - 1] = '\0';
	strncpy(p.displayName, displayName, MAX - 1);
	p.displayName[MAX - 1] = '\0';
	strncpy(p.status, status, MAX - 1);
	p.status[MAX - 1] = '\0';
	
	if (avatarType && avatarEncoding && avatarData) {
		strncpy(p.avatarType, avatarType, MAX - 1);
		p.avatarType[MAX - 1] = '\0';
		strncpy(p.avatarEncoding, avatarEncoding, MAX - 1);
		p.avatarEncoding[MAX - 1] = '\0';
		strncpy(p.avatarData, avatarData, MAX - 1);
		p.avatarData[MAX - 1] = '\0';
		p.hasAvatar = 1;
	} else {
		p.hasAvatar = 0;
	}
	
	return p;
}

void printVerboseProfile(Profile p) {
    printf("TYPE: %s\n", p.type);
    printf("USER_ID: %s\n", p.userID);
    printf("DISPLAY_NAME: %s\n", p.displayName);
    printf("STATUS: %s\n", p.status);
    
    if (p.hasAvatar) {
        printf("AVATAR_TYPE: %s\n", p.avatarType);
        printf("AVATAR_ENCODING: %s\n", p.avatarEncoding);
        printf("AVATAR_DATA: %s\n", p.avatarData);
    }
}

void printSimpleProfile(Profile p) {
    printf("DISPLAY_NAME: %s\n", p.displayName);
    printf("STATUS: %s\n", p.status);

    if (p.hasAvatar) {
        printf("(Avatar is present but not displayed)\n");
    }
}
