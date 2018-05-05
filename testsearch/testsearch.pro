TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
        main.cpp

win32:CONFIG(release, debug|release): LIBS += -L$$PWD/../../../../../usr/local/sword/lib/release/ -lsword-1.8.1
else:win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/../../../../../usr/local/sword/lib/debug/ -lsword-1.8.1
else:unix: LIBS += -L$$PWD/../../../../../usr/local/sword/lib/ -lsword-1.8.1

INCLUDEPATH += $$PWD/../../../../../usr/local/sword/include/sword
DEPENDPATH += $$PWD/../../../../../usr/local/sword/include/sword
