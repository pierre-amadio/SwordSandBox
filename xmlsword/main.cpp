//http://wiki.crosswire.rg/Tutorials:SWORD_102
//https://stackoverflow.com/questions/3092387/parse-a-xml-file-in-qt
//https://stackoverflow.com/questions/25450791/qt-and-qtregexp-for-parsing-html-tags
#include <iostream>
#include <swmgr.h>
#include <swmodule.h>
#include <markupfiltmgr.h>
#include <utilxml.h>
#include <QXmlStreamReader>
#include <QtDebug>
#include <QString>
#include <QRegExp>
#include <simpleosisverseparser.h>
using namespace std;
using namespace::sword;



int main()
{

    const char *bookName;
    const char *keyName;
    const char *xmlString ;
    SWModule * target;
    SWMgr library(new MarkupFilterMgr(FMT_OSIS));
    XMLTag x;
    QString qStr;
    qDebug()<<"start";

    /*
     *<w lemma=\"lemma.Strong:καί strong:G2532\" morph=\"robinson:CONJ\">⸀καὶ</w>
     * */
    //QRegExp rx("<\\s*(\\w+)\\s*");
    QRegExp rx("<(w.*?)>");

    library.setGlobalOption("Morpheme Segmentation","On");
    library.setGlobalOption("Lemmas","On");
    library.setGlobalOption("Morphological Tags","On");
    library.setGlobalOption("Strong's Numbers","On");
    library.setGlobalOption("OSISStrongs","On");

    bookName="MorphGNT";
    keyName="Mark 2:5";
    target = library.getModule(bookName);

    if (!target) {
        fprintf(stderr, "Could not find module [%s].  Available modules:\n", bookName);
        ModMap::iterator it;
        for (it = library.Modules.begin(); it != library.Modules.end(); it++) {
            fprintf(stderr, "[%s]\t - %s\n", (*it).second->Name(), (*it).second->Description());
        }
        exit(-1);
    }

    target->setKey(keyName);

    target->renderText();
    std::cout <<"Key" << target->getKeyText() << "\n";
    //std::cout << target->renderText();
    std::cout <<"\n";

    //xmlString=(const char *) target->renderText().c_str();
    //xmlString=(const char *) target->renderText();
    //qStr= QString::fromUtf8(target->renderText(0, -1, true));

    //xmlString=target->renderText(0, -1, true).c_str();
    //std::cout << "plop \n"<< qStr.toStdString() <<"\n";

    qStr= QString::fromUtf8(target->renderText(0, -1, true));
    //std::cout << "" << qStr.toStdString();

    //qDebug()<<qStr;

    SimpleOsisVerseParser simpleParser(qStr);
    //qDebug() << simpleParser.getVerselist();
    QList<verseChunk> list=simpleParser.getVerselist();

    /*
    int pos = 0;


    while ((pos = rx.indexIn(qStr, pos)) != -1) {


        list << rx.cap(1);
        qDebug() << "\n\nCOIN" <<rx.cap(1)<<"\n\n";
        pos += rx.matchedLength();
        qDebug()<<pos<<"\n";
    }
*/





    foreach( verseChunk s, list ) {
        qDebug()<<"word ='"<< s.fullWord<<"'";
        qDebug()<<"root="<<s.rootValue;
        qDebug()<<"tag="<<s.isXmlTag;
        qDebug()<<"morph" << s.morph;
        qDebug()<<"strong"<<s.strong;
        qDebug()<<"#############";
    }
        cout << "Hello World!" << endl;
        return 0;

}
