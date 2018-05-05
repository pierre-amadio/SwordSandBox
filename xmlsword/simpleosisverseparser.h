#ifndef SIMPLEOSISVERSEPARSER_H
#define SIMPLEOSISVERSEPARSER_H
#include<QString>
#include<QList>
#include "versechunk.h"

class SimpleOsisVerseParser
{
public:
    SimpleOsisVerseParser(QString OsisVerse);
    QList<verseChunk> getVerselist();

private:
    QString OsisVerse;
    QList<verseChunk> verseChunkList;
};

#endif // SIMPLEOSISVERSEPARSER_H
