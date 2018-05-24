#ifndef WORDINFO_H
#define WORDINFO_H
#include <QString>
#include <QObject>

class wordInfo : public QObject
{
    Q_OBJECT

    Q_PROPERTY(QString displayW READ getDisplayWord WRITE setDisplayWord NOTIFY notifyDisplayWord  )

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
    QString StrongDescription;

signals:
    void notifyDisplayWord();


};

#endif // WORDINFO_H
