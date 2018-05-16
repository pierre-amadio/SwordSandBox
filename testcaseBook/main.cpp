#include <iostream>
#include <swmgr.h>
#include <swmodule.h>
#include <markupfiltmgr.h>
#include <versekey.h>
using namespace::sword;

using namespace std;

int main()
{
    cout << "Hello World!" << endl;


    SWMgr library(new MarkupFilterMgr(FMT_PLAIN));
    SWModule * target;

    //const char *moduleName="KJV";
    //const char *moduleName="OSHB";
    const char *moduleName="MorphGNT";
    //const char *moduleName="Nestle1904";

    //const char *keyName="Genesis 1:1";
    const char *keyName="Mark 1:1";


    target = library.getModule(moduleName);

    VerseKey *vk = (target) ? (VerseKey *)target->getKey() : new VerseKey();

        for ((*vk) = TOP; !vk->popError(); vk->setBook(vk->getBook()+1)) {
            if (!target || target->hasEntry(vk)) {
                cout << vk->getBookName() << "\n";
            }
        }



    std::cout << std::endl;

    return 0;
}
