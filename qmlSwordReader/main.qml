import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 1.4


Window {
    id: root
    visible:true
    width: 800; height: 440
    //color: "#00EE00"
    //opacity: .9
    onHeightChanged: console.log(curModuleName, curModuleLang)
    title:qsTr("Sword Reader")

    property string curModuleName: "none"
    property string curModuleLang: "none"

    property string curBookName: "none"

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

    Row {
        id: selectVerseRow
        width:parent.width
        spacing: 10

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
                    root.curBookName=curBookModel[currentIndex].text
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
            Text {text:"b"}
            width:parent.width/4
        }
        MyListSelect {
            id:selectVerseView
            width:parent.width/4
            Text {text:"c"}
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
