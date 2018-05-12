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


    Row {
        id: selectVerseRow
        width:parent.width
        //height: 50
        //anchors.centerIn: parent
        spacing: 10

        MyListSelect {
            id: selectModuleView
            //anchors.left: parent.left
            //color: "#22FF22"
            width: parent.width/4
            //height: parent.height


            ListView{
                id:moduleListView
                anchors.fill:parent
                model:testModel
                snapMode:ListView.SnapToItem
                highlightRangeMode:ListView.StrictlyEnforceRange
                onCurrentItemChanged:{
                    console.log('new item:',testModel[currentIndex].name)
                    //console.log('new item:',testModel[currentIndex].type)
                    //console.log('new item:',testModel[currentIndex].lang)
                    root.curModuleName=testModel[currentIndex].name
                    root.curModuleLang=testModel[currentIndex].lang
                }
                delegate:
                    Text{
                    id:moduleNameText
                    font.pixelSize: 16
                    height:selectVerseRow.height/1
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    width: parent.width
                    //anchors.centerIn:parent

                    //text: testModel.moduleListModel.name
                    text: modelData.name
                }

            }
        }



        MyListSelect {
            id: selectBookView
            width:parent.width/4
            Text {
                anchors.centerIn:parent
                text:"a"
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
