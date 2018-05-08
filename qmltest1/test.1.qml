import QtQuick 2.5
import QtQuick.Controls 1.4

Rectangle {
    id: root
    width: 800; height: 440
    color: "#000000"
    onHeightChanged: console.log('height:', height)

    Rectangle {
        id: selectStuffView
        anchors.top: parent.top
        color: "#FFFF00"
        width:parent.width

        Rectangle {
            id: selectModuleView
            anchors.left: parent.left
            color: "#22FF22"
            width: parent.width/3
            height: parent.height

            ListModel {
                id: testModel
                ListElement { name: "Banana"; color: "Yellow" }
                ListElement { name: "Apple"; color: "Green" }
                ListElement { name: "Coconut"; color: "Brown" }
                ListElement { name: "scoobydoo"; color: "Red" }
                ListElement { name: "pear"; color: "Yellow" }
                ListElement { name: "Raspberry"; color: "Green" }
                ListElement { name: "hazelnuts"; color: "Brown" }
                ListElement { name: "strawberry"; color: "Red" }
                ListElement { name: "figs"; color: "Yellow" }
                ListElement { name: "other stuff"; color: "Green" }
                ListElement { name: "milk"; color: "Brown" }
                ListElement { name: "kebab"; color: "Red" }

            }

            /*
     ComboBox{
         model: testModel
     }
*/

            ListView{
                id:moduleListView
                width:parent.width
                height:parent.height
                model:testModel
                clip:true
                spacing:3
                snapMode:ListView.SnapToItem
                //highlightRangeMode:ListView.NoHighlightRange
                highlightRangeMode:ListView.StrictlyEnforceRange
                //highlightRangeMode:ListView.ApplyRange
                //highlightFollowCurrentItem:true
                onCurrentItemChanged:{
                    console.log('new item:',testModel.get(moduleListView.currentIndex).name )
                }
                delegate:

                    Rectangle{
                    //color:"blue"
                    color: ListView.isCurrentItem ? "yellow" : "red"

                    height:selectModuleView.height/2
                    width:parent.width
                    Text{
                        id:moduleNameText
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        verticalAlignment: Text.AlignVCenter
                        text: name
                        color: color
                    }
                }

            }



        }

        Rectangle {
            id: selectVerseKeyView
            anchors.left: selectModuleView.right
            color: "#FFFFFF"
            width:parent.width-selectModuleView.width
            height: parent.height

            Row {
                id: selectVerseRow
                anchors.centerIn: parent
                spacing: 20

                Rectangle {
                    id: selectBookView
                    width: 48
                    height: 48
                    color: "#ea7025"
                    border.color: Qt.lighter(color)

                }
                Rectangle {
                    id:selectChapterView
                    width: 48
                    height: 48
                    color: "#ea7025"
                    border.color: Qt.lighter(color)

                }
                Rectangle {
                    id:selectVerseView
                    width: 48
                    height: 48
                    color: "#ea7025"
                    border.color: Qt.lighter(color)

                }
            }


        }




        height:100
    }

    Rectangle {
        id: verseView
        width:parent.width
        height:parent.height-selectStuffView.height
        anchors.top:selectStuffView.bottom
        color: "#22DDFF"

        focus: true

        Text {
            id: verseWindow
            anchors.fill:parent
            //height: 10
            color: "#101010"
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
