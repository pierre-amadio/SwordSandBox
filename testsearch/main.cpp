
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



    //Morph search.
    targetModule="OSHB";
    searchType=-3;
    //<w morph="oshm:HVqp3ms" n="1.1" savlm="strong:H02421">חַי</w>
    searchQuery="Word//Morph./HVqp3ms/";


/*
    //Why does this not work ?
    targetModule="MorphGNT";
    searchType=-3;
    //<w morph="robinson:V-AAP-GPM" savlm="lemma.Strong:εξερχομαι strong:G1831">εξελθοντων</w>
    searchQuery="Word//Morph./V-AAP-GPM/";  
*/


    //Working example


/*
*	KJV search
*/

    /*
    //<w lemma="strong:G5547 lemma.TR:χριστον" src="9">Christ</w>
    targetModule="KJV";
    searchType=-3;
    searchQuery="Word//Lemma./G5547/";
    */

/*
    targetModule="KJV";
    searchType=-1;
    searchQuery="heaven";
*/

/*
    //Do not forget to "mkfastmod KJV" first
    targetModule="KJV";
    searchType=-4;
    searchQuery="lemma:G2531";
*/  

/*
    //Do not forget to "mkfastmod KJV" first
    targetModule="KJV";
    searchType=-4;
    searchQuery="heaven";
*/

/*
*	OSHB search
*/

/*
    //Strongs search without clucene index.
    targetModule="OSHB";
    searchType=-3;
    searchQuery="Word//Lemma./H0835/";
*/


/*
    //Morph search.
    targetModule="OSHB";
    searchType=-3;
    searchQuery="Word//Morph./HVqp3ms/";
*/

/*
    //Search with hebrew accent. Does not work with -4, clucene search.
    targetModule="OSHB";
    searchType=-1;
    searchQuery="תְּבַקְשֶׁנָּה";
    manager.setGlobalOption("Hebrew Vowel Points", "On");
*/

/*
    //Search without hebrew accent. Works with -1 and -4 search type.
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


/*  //Strongs search with clucene index.
    //Do not forget to "mkfastmod OSHB" first
    targetModule="OSHB";
    searchType=-4;
    searchQuery="lemma:H08064";
*/


/*
*	MorphGNT search
*/


/*
    targetModule="MorphGNT";
    searchType=-3;
    searchQuery="Word//Lemma./G5547/";  

*/

/*
*	LXX search
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
