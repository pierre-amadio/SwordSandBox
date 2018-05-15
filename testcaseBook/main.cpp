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

    const char *keyName="Genesis 1:1";
    //const char *keyName="Mark 1:1";


    target = library.getModule(moduleName);
    target->setKey(keyName);
    char e=target->Error();
    if(e) {
        printf("Error: %c \n", target->Error());
        std::cout<< "Error:"<<target->Error()<<"\n";
    } else {
        std::cout << target->getKeyText() << "\n";
        std::cout << target->renderText();
    }
    std::cout << "\n";
    std::cout << std::endl;

    return 0;
}
