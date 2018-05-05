#include "simpleosisverseparser.h"
#include <QString>
#include <QDebug>

SimpleOsisVerseParser::SimpleOsisVerseParser(QString verse)
{

    int maxLenght=verse.length();
    QString newWord("");
    bool inTagFlag=false;

    for(int n=0;n<maxLenght;n++){
        //qDebug() << n ;
        //qDebug() << verse[n];

        if(n>1 && verse.mid(n-2,2)=="<w") {
            qDebug()<<"New TAG";
            inTagFlag=true;
            qDebug()<<"neWord="<<newWord;

            if(newWord.mid(0,newWord.length()-2)>0){
                qDebug()<<"withoutTag"<<newWord.mid(0,newWord.length()-2);
                VerseList.append(newWord.mid(0,newWord.length()-2));
                newWord="<w";
            }

        }


        newWord.append(verse[n]);
        qDebug()<<"newWord"<<newWord;
        if (n>3){
            int startIndex=n;

           // qDebug() << "newword" << newWord;

            if(verse.mid(n-3,4)=="</w>" ) {
               qDebug()<< "Fin de TAG" << newWord << "YEOP";
               inTagFlag=false;
                VerseList.append(newWord);
                newWord="";
            }
            //if(verse[n] == 'p') {qDebug() << "YOP\n";}

        }

    }
}

QList<QString> SimpleOsisVerseParser::getVerselist(){
    return this->VerseList;

}
