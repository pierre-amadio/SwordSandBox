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

int main(int argc, char *argv[])
{
    SWMgr library(new MarkupFilterMgr(FMT_HTML));
    library.setGlobalOption("Morpheme Segmentation","On");
    library.setGlobalOption("Lemmas","On");
    library.setGlobalOption("Morphological Tags","On");
    library.setGlobalOption("Strong's Numbers","On");

    //library.setGlobalOption("OSISStrongs","On");


    SWModule * target;
    qStdOut() << "Lets try that out !\n";
    //target = library.getModule("OSHB");
    //target = library.getModule("ESV2011");
    //target = library.getModule("LXX");
    target = library.getModule("MorphGNT");

    if (!target) {
            fprintf(stderr, "Could not find module [%s].  Available modules:\n", argv[1]);
            ModMap::iterator it;
            for (it = library.Modules.begin(); it != library.Modules.end(); it++) {
                fprintf(stderr, "[%s]\t - %s\n", (*it).second->Name(), (*it).second->Description());
            }
            exit(-1);
        }

    //target->setKey("PS 1:1");

    target->setKey("Jhon 1:1");
    target->renderText();    // force an entry lookup first to resolve key to something pretty for printing below.

    std::cout << target->getKeyText() << "\n";
    std::cout << target->renderText();
    std::cout << "\n";
    std::cout << std::endl;
    return 0;

}



