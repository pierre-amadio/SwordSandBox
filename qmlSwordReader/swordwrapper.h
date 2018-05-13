#ifndef SWORDWRAPPER_H
#define SWORDWRAPPER_H

#include <QObject>

class swordWrapper : public QObject
{
    Q_OBJECT
public:
    explicit swordWrapper(QObject *parent = nullptr);

signals:

public slots:
};

#endif // SWORDWRAPPER_H