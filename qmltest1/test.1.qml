import QtQuick 2.5

Rectangle {
  id: root
  width: 800; height: 440
  color: "#000000"
  onHeightChanged: console.log('height:', height)

 Text {
   id: verseWindow
   width: root.width
   height: 10
   color: "#FFFFCC"
   font {
    //family: "Ezra SIL"
    family: "Linux Libertine O"
    pixelSize: 40
   }
   //focus: true
   //color: focus?"red":"black"
   text:"οὐδέν ἐστιν ἔξωθεν τοῦ ἀνθρώπου εἰσπορευόμενον εἰς αὐτὸν ὃ δύναται κοινῶσαι αὐτόν· ἀλλὰ τὰ ἐκ τοῦ ἀνθρώπου ἐκπορευόμενά ἐστιν τὰ κοινοῦντα τὸν ἄνθρωπον." 
 }


 ListView {
    anchors.fill: parent; 
    model: Qt.fontFamilies()

    delegate: Item {
        height: 40; 
        width: ListView.view.width
        Text {
            anchors.centerIn: parent
            text: modelData; 
            color: "white"
        }
    }
}



}
