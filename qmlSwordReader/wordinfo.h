#ifndef WORDINFO_H
#define WORDINFO_H
#include <QString>
#include <QObject>

class wordInfo : public QObject
{
    Q_OBJECT



public:
    wordInfo(QObject *parent=0);

signals:

private:
    QString displayWord;
    bool hasInfo;
    QString rootWord;
    QString morphCode;
    QString morphDesciption;
    QString StrongId;
    QString StronDescription;
};

#endif // WORDINFO_H
