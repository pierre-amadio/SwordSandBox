#ifndef WORDINFO_H
#define WORDINFO_H
#include <QString>
#include <QObject>

class wordInfo : public QObject
{
    Q_OBJECT


public:
    wordInfo(QObject *parent=0);

    QString getDisplayWord() const;
    void setDisplayWord(const QString cn);


    QString displayWord;
    bool hasInfo;
    QString rootWord;
    QString morphCode;
    QString morphDesciption;
    QString StrongId;
    QString StronDescription;

signals:


};

#endif // WORDINFO_H
