#ifndef VERSECHUNK_H
#define VERSECHUNK_H
#include<QString>

class verseChunk
{
public:
    verseChunk(bool i,QString w);
    bool isXmlTag;
    QString word;
    void setIsXmlTag(bool i);

};

#endif // VERSECHUNK_H
