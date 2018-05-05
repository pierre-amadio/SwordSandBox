#ifndef SIMPLEOSISVERSEPARSER_H
#define SIMPLEOSISVERSEPARSER_H
#include<QString>
#include<QList>

class SimpleOsisVerseParser
{
public:
    SimpleOsisVerseParser(QString OsisVerse);
    QList<QString> getVerselist();

private:
    QString OsisVerse;
    QList<QString> VerseList;
};

#endif // SIMPLEOSISVERSEPARSER_H
