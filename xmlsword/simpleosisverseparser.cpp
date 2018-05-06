#include "simpleosisverseparser.h"
#include <QString>
#include <QDebug>
#include "versechunk.h"
#include <QXmlStreamReader>
#include <utilxml.h>

using namespace::sword;


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
            //qDebug()<<"yep tag";
            tmpChunk.setIsXmlTag(true);
            QString tmpRoot="none found";
            QString tmpStrong="none found";
            QString tmpMorph="none found";

            XMLTag xmlTag;

            QXmlStreamReader reader(curWord);

            while(!reader.atEnd() && !reader.hasError()) {
                if(reader.readNext() == QXmlStreamReader::StartElement && reader.name() == "w") {
                    tmpRoot=reader.readElementText();
                }
                if(reader.hasError()) {
                    qDebug()<<"error:"<<curWord<<"\n";
                    qDebug()<< "\n\nreader error: " << reader.errorString() << "\n";
                }
            }


            xmlTag.setText(curWord.toUtf8());

            StringList attributes = xmlTag.getAttributeNames();

            for (StringList::iterator it = attributes.begin(); it != attributes.end(); it++) {
                QString attributeName=it->c_str();

                if(attributeName=="lemma") {
                    qDebug()<<"it s a lemma"<<xmlTag.getAttribute("lemma", 1, ' ');
                    tmpStrong=xmlTag.getAttribute("lemma", 1, ' ');
                } else if (attributeName=="morph"){
                    qDebug()<<"it s a morph"<<xmlTag.getAttribute("morph", 0, ' ');
                    tmpMorph=xmlTag.getAttribute("morph", 0, ' ');
                } else {
                    qDebug()<<"unknown attributeName"<<attributeName;
                    }


            }


            tmpChunk.rootValue=tmpRoot;
            tmpChunk.strong=tmpStrong;
            tmpChunk.morph=tmpMorph;


       } else {
            tmpChunk.morph="NONE";
            tmpChunk.strong="NONE";
            tmpChunk.rootValue=curWord;
       }



       verseChunkList.append(tmpChunk);

    }

}

QList<verseChunk> SimpleOsisVerseParser::getVerselist(){
    return this->verseChunkList;


}
