import QtQuick 2.5

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
