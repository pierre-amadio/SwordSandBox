TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

LIBS += -lsword
#INCLUDEPATH += /usr/include/sword
#Using some version of sword installed in /usr/local
#Be sure to set LD_LIBRARY_PATH=/usr/local/sword/lib before running the executable
INCLUDEPATH += /usr/local/sword/include/sword
LIBS += -L/usr/local/sword/lib -lsword
CONFIG += c++11


SOURCES += \
        main.cpp

