QT -= gui

CONFIG += c++11 console
CONFIG -= app_bundle

# The following define makes your compiler emit warnings if you use
# any feature of Qt which as been marked deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
        main.cpp

unix:!macx: LIBS += -L$$PWD/../../../../../usr/local/sword/lib/ -lsword-1.8.1

INCLUDEPATH += $$PWD/../../../../../usr/local/sword/include
DEPENDPATH += $$PWD/../../../../../usr/local/sword/include

win32:CONFIG(release, debug|release): LIBS += -L$$PWD/../../../../../usr/local/sword/lib/release/ -lsword-1.8.1
else:win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/../../../../../usr/local/sword/lib/debug/ -lsword-1.8.1
else:unix: LIBS += -L$$PWD/../../../../../usr/local/sword/lib/ -lsword-1.8.1

INCLUDEPATH += $$PWD/../../../../../usr/local/sword/include/sword
DEPENDPATH += $$PWD/../../../../../usr/local/sword/include/sword
