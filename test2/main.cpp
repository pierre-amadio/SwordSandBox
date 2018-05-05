#include <QCoreApplication>
#include <QTextStream>

#include <swmgr.h>
#include <swmodule.h>
#include <markupfiltmgr.h>
using namespace::sword;

QTextStream& qStdOut()
{
    static QTextStream ts( stdout );
    return ts;
}


int showVerse(const char * bookName, const char * keyName){
    SWMgr library(new MarkupFilterMgr(FMT_PLAIN));
    SWModule * target;
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

    //target->setKey("Jhon 1:1");
    target->renderText();    // force an entry lookup first to resolve key to something pretty for printing below.

    //std::cout << target->getKeyText() << "\n";
    std::cout << target->renderText();
    std::cout << "\n";
    std::cout << std::endl;

    return 0;
}

int main(int argc, char *argv[])
{

    QString searchQuery;
    QString targetModule;
    int searchType;
    SWMgr manager;
    SWModule *target;
    ListKey listkey;
    ModMap::iterator it;


    // FROM swmodule.h
            /*
             *                      >=0 - regex; (for backward compat, if > 0 then used as additional REGEX FLAGS)
             *                      -1  - phrase
             *                      -2  - multiword
             *                      -3  - entryAttrib (eg. Word//Lemma./G1234/)      (Lemma with dot means check components (Lemma.[1-9]) also)
             *                      -4  - Lucene
             *                      -5  - multilemma window; set 'flags' param to window size (NOT DONE)
             */

    searchType=-4;
    //searchQuery="dog";
    //searchQuery="strong:G846";
    //searchQuery='lemma="strong:H0835"';
    searchQuery="strong:H0835";
    //searchQuery='morph:"N-NSF"';

    targetModule="OSHB";
    //targetModule="LXX";
    //targetModule="MorphGNT";
    //targetModule="FreSegond";
    //targetModule="ESV2011";

    //manager.setGlobalOption("Greek Accents", "Off");
    //manager.setGlobalOption("Strong's Numbers", "Off");
    //manager.setGlobalOption("Hebrew Vowel Points", "Off");
    //manager.filterText("Greek Accents", searchTerm);


    it = manager.Modules.find(targetModule.toStdString().c_str());
    if (it == manager.Modules.end()) {
        qStdOut() << "No such module: " << targetModule <<"\n";
    }

    target = (*it).second;
    listkey = target->search(searchQuery.toStdString().c_str(), searchType);


    while (!listkey.popError()) {
            std::cout << (const char *)listkey <<"\n";
            //if (listkey.getElement()->userData) std::cout << " : " << (__u64)listkey.getElement()->userData << "%";
            showVerse(targetModule.toStdString().c_str(),(const char *) listkey);
            std::cout << std::endl;
            listkey++;
    }


    //showVerse(targetModule.toStdString().c_str(),"Mat 1:1");



    return 0;

}
