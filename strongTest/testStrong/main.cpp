#include <iostream>
#include <swmgr.h>
#include <swmodule.h>
#include <markupfiltmgr.h>
using namespace::sword;
using namespace std;




int main()
{

    SWMgr library(new MarkupFilterMgr(FMT_HTML));
    SWModule * target;
    target = library.getModule("StrongsHebrew");

    if (!target) {
        fprintf(stderr, "Could not find module.  Available modules:\n");
        ModMap::iterator it;
        for (it = library.Modules.begin(); it != library.Modules.end(); it++) {
            fprintf(stderr, "[%s]\t - %s\n", (*it).second->Name(), (*it).second->Description());
        }
        exit(-1);
    }
    target->setKey("05975");
    target->renderText();    // force an entry lookup first to resolve key to something pretty for printing below.

    std::cout << target->getKeyText() << "\n";
    std::cout << target->renderText();
    std::cout << "\n";
    std::cout << std::endl;
    return 0;
}
