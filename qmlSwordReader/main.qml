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

    Rectangle {
        id: selectStuffView
        anchors.top: parent.top
        //color: "#000000"
        width:parent.width
        height:50

        MyListSelect {
            id: selectModuleView
            anchors.left: parent.left
            //color: "#22FF22"
            width: parent.width/3
            height: parent.height


            ListView{
                id:moduleListView
                width:parent.width
                height:parent.height
                model:testModel
                clip:true
                //spacing:10
                //snapMode:ListView.SnapToItem
                //highlightRangeMode:ListView.NoHighlightRange
                highlightRangeMode:ListView.StrictlyEnforceRange
                //highlightRangeMode:ListView.ApplyRange
                //highlightFollowCurrentItem:true
                onCurrentItemChanged:{
                    //console.log('new item:',testModel[currentIndex].name)
                    //console.log('new item:',testModel[currentIndex].type)
                    //console.log('new item:',testModel[currentIndex].lang)
                    root.curModuleName=testModel[currentIndex].name
                    root.curModuleLang=testModel[currentIndex].lang
                }
                delegate:

                    Rectangle{
                    color: ListView.isCurrentItem ? "white" : "gey"
                    //opacity:.9
                    //radius: 5

                    height:selectModuleView.height/1
                    //width:parent.width
                    Text{
                        id:moduleNameText
                        font.pixelSize: 16
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        verticalAlignment: Text.AlignVCenter
                        //text: testModel.moduleListModel.name
                        text: modelData.name
                    }
                }

            }



        }

        Rectangle {
            id: selectVerseKeyView
            anchors.left: selectModuleView.right
            //color: "#F00FFF"
            width:parent.width-selectModuleView.width
            height: parent.height

            Row {
                id: selectVerseRow
                anchors.centerIn: parent
                spacing: 20

                MyListSelect {
                    id: selectBookView

                }
                MyListSelect {
                    id:selectChapterView
                    width:100
                }
                MyListSelect {
                    id:selectVerseView

                }


            }
        }

    }

    Rectangle {
        id: verseView
        width:parent.width
        height:parent.height-selectStuffView.height
        anchors.top:selectStuffView.bottom
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
