#ifndef PARSE_H
#define PARSE_H

#include "profile.h"
//#include "post.h"
#include "DM.h"

// Function declarations for parsing messages
char* getFieldValue(const char *buffer, const char *key);
Profile parseProfile(const char *buffer);
//Post parsePost(const char *buffer);
Dm parseDm(const char *buffer);

#endif // PARSE_H