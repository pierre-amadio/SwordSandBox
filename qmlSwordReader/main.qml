import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 1.4


Window {
    id: root
    visible:true
    width: 800; height: 440
    //color: "#00EE00"
    //opacity: .9
    //onHeightChanged: console.log(curModuleName, curModuleLang)
    onHeightChanged: console.log("max chapter",maxChapter)
    title:qsTr("Sword Reader")

    property string curModuleName: "none yet"
    property string curModuleLang: "none yet"
    property string curBookName: "none yet"
    property int curChapter: 155
    property int maxChapter: 156
    property int curVerse: 157
    property int maxVerse: 158

    //property ListModel curModuleModel:({})
    //property ListModel curBookModel:({})

    property variant chapterListModel: []
    property variant verseListModel: []

    function fillChapterList(nbr){
        //console.log("let's fill stuff:",nbr)
        chapterListModel=[]
        var tmpArray = new Array (0)
        for (var i = 1; i <= nbr; i++){
            tmpArray.push(i)
        }
        chapterListModel=tmpArray
    }

    function fillVerseList(nbr){
        //console.log("let's fill stuff:",nbr)
        verseListModel=[]
        var tmpArray = new Array (0)
        for (var i = 1; i <= nbr; i++){
            tmpArray.push(i)
        }
        verseListModel=tmpArray
    }


    signal newModuleSelected(string msg)
    onCurModuleNameChanged: {
        console.log("New module selected",curModuleName)
        newModuleSelected(curModuleName)
    }

    signal newBookSelected(string msg)
    onCurBookNameChanged: {
        console.log("New book selected",curBookName)
        newBookSelected(curBookName)
    }

    signal newChapterSelected(int chapter)
    onCurChapterChanged: {
        console.log("New chapter selected",curChapter)
        newChapterSelected(curChapter)
    }


    onMaxChapterChanged: {
        console.log("mach chapter changed",maxChapter)
        fillChapterList(maxChapter)
    }

    signal newVerseSelected(int verse)
    onCurVerseChanged: {
        console.log("New verse selected",curVerse)
        newVerseSelected(curVerse)
    }

    onMaxVerseChanged: {
        console.log("max verse changed",maxVerse)
        fillVerseList(maxVerse)
    }



    Row {
        id: selectVerseRow
        width:parent.width
        spacing: 0

        MyListSelect {
            id: selectModuleView
            width: parent.width/4
            ListView{
                id:moduleListView
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
            width:parent.width/4
            ListView{
                id:bookListView
                anchors.fill:parent
                model:curBookModel
                snapMode:ListView.SnapToItem
                highlightRangeMode:ListView.StrictlyEnforceRange
                onCurrentItemChanged:{
                    root.curBookName=curBookModel[currentIndex]
                }
                delegate:
                    Text{
                    id:bookNameText
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
        width:parent.width
        anchors.bottom: parent.bottom
        anchors.top:selectVerseRow.bottom
        //color: "#22DDFF"

        focus: true

        Text {
            id: verseWindow
            anchors.fill:parent
            //height: 10
            //color: "#101010"
            font {
                //family: "Ezra SIL"
                family: "Linux Libertine O"
                pixelSize: 40
            }
            wrapMode: Text.WordWrap
            //elide: Text.ElideMiddle
            //style: Text.Sunken
            //styleColor: '#FF4444'
            //focus: true
            //color: focus?"red":"black"
            text:"οὐδέν ἐστιν ἔξωθεν τοῦ ἀνθρώπου εἰσπορευόμενον εἰς αὐτὸν ὃ δύναται κοινῶσαι αὐτόν· ἀλλὰ τὰ ἐκ τοῦ ἀνθρώπου ἐκπορευόμενά ἐστιν τὰ κοινοῦντα τὸν ἄνθρωπον."
        }


    }
}
