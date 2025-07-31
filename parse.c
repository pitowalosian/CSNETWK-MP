#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "parse.h"

char* getFieldValue(const char* buffer, const char* key) {
	char* value = NULL;
	char* keyStart = strstr(buffer, key);
	
	if (keyStart) {
		keyStart += strlen(key) + 1;
		char *keyEnd = strchr(keyStart, '\n');
		
		if (keyEnd) {
			size_t len = keyEnd - keyStart;
			value = (char*)malloc(len + 1);
			strncpy(value, keyStart, len);
			value[len] = '\0';
		}
	}
	
	return value;
}

Profile parseProfile(const char* buffer) {
	
	const char* userID = getFieldValue(buffer, "USER_ID");
	const char* displayName = getFieldValue(buffer, "DISPLAY_NAME");
	const char* status = getFieldValue(buffer, "STATUS");
	const char* avatarType = getFieldValue(buffer, "AVATAR_TYPE");
	const char* avatarEncoding = getFieldValue(buffer, "AVATAR_ENCODING");
	const char* avatarData = getFieldValue(buffer, "AVATAR_DATA");
	
	Profile p = createProfile(userID, displayName, status, avatarType, avatarEncoding, avatarData);
		
	return p;
}

Dm parseDm(const char* buffer) {
	
	const char* from = getFieldValue(buffer, "FROM");
	const char* to = getFieldValue(buffer, "TO");
	const char* content = getFieldValue(buffer, "CONTENT");
	const char* timestamp = getFieldValue(buffer, "TIMESTAMP");
	const char* messageID = getFieldValue(buffer, "MESSAGE_ID");
	const char* token = getFieldValue(buffer, "TOKEN");
	
	Dm dm = createDm(from, to, content, timestamp, messageID, token);
	
	return dm;
}