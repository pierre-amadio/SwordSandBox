#ifndef WORDINFO_H
#define WORDINFO_H
#include <QString>

class wordInfo
{

public:
    wordInfo();

    QString getDisplayWord() const;
    void setDisplayWord(const QString cn);


    QString displayWord;
    bool hasInfo;
    QString rootWord;
    QString morphCode;
    QString morphDesciption;
    QString StrongId;
    QString StrongDescription;



};

#endif // WORDINFO_H
