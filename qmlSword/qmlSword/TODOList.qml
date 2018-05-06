import QtQuick 2.0
import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import Todo 1.0

Frame {
    ListView {
        implicitWidth: 250
        implicitHeight: 250
        clip: true

        model: TODOModel {}

        delegate: RowLayout {
            width: parent.width

            CheckBox {
                checked:model.done
                onClicked: model.done = checked
            }
            TextField {
                text:model.description
                onEditingFinished: model.description = text
                Layout.fillWidth: true
            }
        }

    }
}
