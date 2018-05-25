#ifndef SIMPLEOSISVERSEPARSER_H
#define SIMPLEOSISVERSEPARSER_H
#include<QString>
#include<QList>
#include "versechunk.h"

class simpleOsisVerseParser
{
public:
    simpleOsisVerseParser(QString osisVerse);
    QList<verseChunk> getVerselist();

private:
    //QString osisVerse;
    QList<verseChunk> verseChunkList;
};

#endif // SIMPLEOSISVERSEPARSER_H











