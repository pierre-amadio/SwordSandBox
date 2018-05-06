#include "simpleosisverseparser.h"
#include <QString>
#include <QDebug>
#include "versechunk.h"

SimpleOsisVerseParser::SimpleOsisVerseParser(QString verse)
{

    qDebug()<<"New verse";
    qDebug()<<verse;
    QList<QString> wordList;
    int maxLenght=verse.length();
    QString newWord("");


    for(int n=0;n<maxLenght;n++){

        if(n>1 && verse.mid(n-2,2)=="<w") {
            if(newWord.mid(0,newWord.length()-2)>0){
                wordList.append(newWord.mid(0,newWord.length()-2));
                newWord="<w";
            }
        }

        newWord.append(verse[n]);

        if (n>3){
            if(verse.mid(n-3,4)=="</w>" ) {
                wordList.append(newWord);
                newWord="";
            }
        }
    }

    if(newWord.length()>0){
        wordList.append(newWord);
    }


    foreach( QString curWord, wordList ) {
      qDebug()<<"curWord:"<<curWord;
       bool isXml=false;
       QString tmpWord=curWord;

       verseChunk tmpChunk;

       if(curWord.mid(0,2)=="<w") {
           qDebug()<<"yep tag";

            tmpChunk.setIsXmlTag(true);
            tmpChunk.rootValue="TO BE DONE";
            tmpChunk.morph="TO BE DEFINE";


       } else {
            tmpChunk.morph="NONE";
            tmpChunk.rootValue=curWord;


       }



       verseChunkList.append(tmpChunk);

    }

}

QList<verseChunk> SimpleOsisVerseParser::getVerselist(){
    return this->verseChunkList;


}
