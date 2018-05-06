#ifndef VERSECHUNK_H
#define VERSECHUNK_H
#include<QString>

class verseChunk
{
public:
    verseChunk();
    bool isXmlTag;
    QString rootValue;
    QString strong;
    QString morph;
    void setIsXmlTag(bool i);

};

#endif // VERSECHUNK_H
