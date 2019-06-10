#include <iostream>
#include <swmgr.h>
#include <swmodule.h>
#include <markupfiltmgr.h>

using namespace std;
using namespace::sword;

int showVerse(const char * bookName, const char * keyName){
    SWMgr library(new MarkupFilterMgr(FMT_PLAIN));

    library.setGlobalOption("Morpheme Segmentation","On");
    library.setGlobalOption("Lemmas","Off");
    library.setGlobalOption("Morphological Tags","Off");
    library.setGlobalOption("Strong's Numbers","Off");

    //library.setGlobalOption("OSISStrongs","On");

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


int main()
{
    const char * searchQuery;
    const char * targetModule;
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


    //for indexed, search lemma:G1234
    //searchType=-3;
    //searchQuery="H8064";

    //This works to search for strong number.
    //searchType=-3;
    //searchQuery="Word//Lemma./H2916/";

    //And this wokrs for clucene search as well.
    //searchType=-4;
    //searchQuery="lemma:G2531";
    
    //do not forget to "mkfastmod OSHB"
    //searchType=-4;
    //searchQuery="lemma:H0835";
    //searchQuery="strong:H0835";

    targetModule="KJV";

    searchType=-4;
    //searchQuery="strong:H08064";


    //Work:

/*
    targetModule="OSHB";
    searchType=-1;
    searchQuery="בקשׁ";
    manager.setGlobalOption("Hebrew Vowel Points", "Off");
*/

/*
    //do not forget to "mkfastmod OSHB"
    targetModule="OSHB";
    searchType=-4;
    searchQuery="בקשׁ";
    manager.setGlobalOption("Hebrew Vowel Points", "Off");
*/

/*
    targetModule="KJV";
    searchType=-1;
    searchQuery="heaven";
*/

/*
    /Do not forget to "mkfastmod KJV" first
    targetModule="KJV";
    searchType=-4;
    searchQuery="heaven";
*/

    //targetModule="LXX";
    //targetModule="MorphGNT";
    //targetModule="FreSegond";
    //targetModule="ESV2011";

    //manager.setGlobalOption("Greek Accents", "Off");
    //manager.setGlobalOption("Strong's Numbers", "Off");
    //manager.setGlobalOption("Hebrew Vowel Points", "Off");
    //manager.filterText("Greek Accents", searchTerm);


    it = manager.Modules.find(targetModule);
    if (it == manager.Modules.end()) {
         cout << "No such module: " << targetModule <<"\n";
    }

    target = (*it).second;
    listkey = target->search(searchQuery, searchType);


    while (!listkey.popError()) {
            std::cout << (const char *)listkey <<"\n";
            //if (listkey.getElement()->userData) std::cout << " : " << (__u64)listkey.getElement()->userData << "%";
            showVerse(targetModule,(const char *) listkey);
            std::cout << std::endl;
            listkey++;
    }


    //showVerse(targetModule.toStdString().c_str(),"Mat 1:1");



    //cout << "Hello World!" << endl;
    return 0;
}
