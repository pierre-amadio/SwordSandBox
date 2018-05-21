import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4

Window {
    id: root
    objectName: "rootWindow"
    visible:true
    width: 800; height: 440
    //color: "#00EE00"
    //opacity: .9
    onHeightChanged: {
        console.log(" ")
        //console.log("curModuleName",curModuleName)
        //console.log("currBookName",curBookName)
        //console.log("curChapter",curChapter)
        //console.log("curVerse", curVerse)
        //cleanBookList()
        var start=verseWindow.selectionStart
        var end=verseWindow.selectionEnd
        var curTxt=verseWindow.getText(start,end)
        console.log("begin at",start)
        console.log(verseWindow.selectedText)
        console.log("end at",end)
        console.log("\n",curTxt)
        verseWindow.font.underline=false
    }

    //onHeightChanged: console.log("max chapter",maxChapter)
    title:qsTr("Sword Reader")

    property string curModuleName: "none yet"
    property string curModuleLang: "none yet"
    property string curBookName: "none yet"
    property int curChapter: 155
    property int maxChapter: 156
    property int curVerse: 157
    property int maxVerse: 158

    property variant chapterListModel: []
    property variant verseListModel: []

    property string mainTextModel:"pika coin coin"


    function cleanBookList(){
        console.log("Cleaning book list")
        //curBookModel=new Array (0)
        //curBookModel="none yet"
        //bookListView.model=new Array(0)
        var s=bookListView.model.lenght
        var m=bookListView.model
        //console.log(m[70])
        //for(var i=0;i<70;i++) {
        //    if (m[i]!==undefined){
        //        console.log(m[i])
        //    }
        //}
        while(m[0]!==undefined){
            console.log(m[0])
            m.pull(0)
        }

        //console.log(bookListView.model.count)
        //newModuleSelected(curModuleName)

    }

    function fillChapterList(nbr){
        //console.log("let's fill stuff:",nbr)
        chapterListModel=[]
        var tmpArray = new Array (0)
        for (var i = 1; i <= nbr; i++){
            tmpArray.push(i)
        }
        chapterListModel=tmpArray
        chapterView.currentIndex=0
        newChapterSelected(chapterListModel[chapterView.currentIndex])
    }

    function fillVerseList(nbr){
        //console.log("let's fill VerseList:",nbr)
        verseListModel=[]
        var tmpArray = new Array (0)
        for (var i = 1; i <= nbr; i++){
            tmpArray.push(i)
        }
        verseListModel=tmpArray
        singleVerseView.currentIndex=0
        newVerseSelected(verseListModel[singleVerseView.currentIndex])

    }


    signal newModuleSelected(string msg)
    onCurModuleNameChanged: {
        console.log("New module selected",curModuleName)
        //console.log(curBookModel)
        //curBookModel=new Array (0)
        //bookListView.model=curBookModel

        //curBookModel=tmpArray
        //bookListView.model=tmpArray
        //console.log("tmp array",tmpArray)
        //console.log("curbookModel is now ",curBookModel)

        //chapterListModel=[]

        newModuleSelected(curModuleName)
    }

    signal newBookSelected(string msg)
    onCurBookNameChanged: {
        console.log("New book selected",curBookName)
        newBookSelected(curBookName)
    }

    signal newChapterSelected(int chapter)
    onCurChapterChanged: {
        //console.log("New chapter selected",curChapter)
        newChapterSelected(curChapter)
    }


    onMaxChapterChanged: {
        console.log("mach chapter changed",maxChapter)
        fillChapterList(maxChapter)
    }

    signal newVerseSelected(int verse)
    onCurVerseChanged: {
        //console.log("New verse selected",curVerse)
        newVerseSelected(curVerse)
    }

    onMaxVerseChanged: {
        console.log("max verse changed",maxVerse)
        fillVerseList(maxVerse)
    }


    Row {
        objectName: "selectVerseRow"
        id: selectVerseRow
        width:parent.width
        spacing: 0

        MyListSelect {
            id: selectModuleView
            objectName: "selectModuleView"
            width: parent.width/4
            ListView{
                id:moduleListView
                objectName: "moduleListView"
                anchors.fill:parent
                model:curModuleModel
                snapMode:ListView.SnapToItem
                highlightRangeMode:ListView.StrictlyEnforceRange
                onCurrentItemChanged:{
                    root.curModuleName=curModuleModel[currentIndex].name
                    root.curModuleLang=curModuleModel[currentIndex].lang
                }
                delegate:
                    Text{
                    id:moduleNameText
                    font.pixelSize: 16
                    height:selectVerseRow.height/1
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    width: parent.width
                    text: modelData.name
                }

            }
        }



        MyListSelect {
            id: selectBookView
            objectName: "selectBookView"
            width:parent.width/4
            ListView{
                id:bookListView
                objectName: "bookListView"
                anchors.fill:parent
                model:curBookModel
                snapMode:ListView.SnapToItem
                highlightRangeMode:ListView.StrictlyEnforceRange
                onCurrentItemChanged:{
                    root.curBookName=curBookModel[currentIndex]
                }
                delegate:
                    Text{
                    id:bookNameDelegate
                    objectName: "bookNameDelegate"
                    font.pixelSize: 16
                    height:selectVerseRow.height/1
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    width: parent.width
                    text: modelData
                }

            }
        }

        MyListSelect {
            id:selectChapterView
            width:parent.width/4



            ListView{
                id:chapterView
                anchors.fill:parent
                model: chapterListModel
                snapMode:ListView.SnapToItem
                highlightRangeMode:ListView.StrictlyEnforceRange
                onCurrentItemChanged:{
                    root.curChapter=chapterListModel[currentIndex]
                }
                delegate:
                    Text{
                    id:chapterId
                    font.pixelSize: 16
                    height:selectVerseRow.height/1
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    width: parent.width
                    text: modelData
                }

            }

        }
        MyListSelect {
            id:selectVerseView
            width:parent.width/4


            ListView{
                id:singleVerseView
                anchors.fill:parent
                model: verseListModel
                snapMode:ListView.SnapToItem
                highlightRangeMode:ListView.StrictlyEnforceRange
                onCurrentItemChanged:{
                    root.curVerse=verseListModel[currentIndex]
                }
                delegate:
                    Text{
                    id:verseId
                    font.pixelSize: 16
                    height:selectVerseRow.height/1
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    width: parent.width
                    text: modelData
                }

            }



        }


    }




    Rectangle {
        id: verseView
        objectName: "verseView"
        width:parent.width
        anchors.bottom: parent.bottom
        anchors.top:selectVerseRow.bottom
        //color: "#22DDFF"

        focus: true
        TextArea{
            id: verseWindow
            textFormat: Text.RichText

            style: TextAreaStyle {
                backgroundColor: "green"
                selectedTextColor: "blue"
                selectionColor: "yellow"
            }


            anchors.fill:parent
            readOnly: true
            //height: 10
            //color: "#101010"
            font {
                //family: "Ezra SIL"
                family: "Linux Libertine O"
                pixelSize: 40
                //underline: false
            }
            wrapMode: Text.WordWrap
            text:mainTextModel

            onLinkActivated:{
                console.log("cliketi:"+link)
            }

            onLinkHovered: {
                console.log("what to do with:"+link)
            }



        }

    }
}


