import QtQuick 1.1
import "colorPickerComponents"
import "colorPickerComponents/ColorFunctions.js" as ColorFunctions

//set of tools to choose the color (square + slider color + slider alpha + color inputs)
Item{
    id: colorPicker

    property color colorValue: ColorFunctions.hsba(colorSlider.value, colorSelector.saturation, colorSelector.brightness, alphaSlider.value)
    property color alphaColorText: ColorFunctions.fullColorString(colorPicker.colorValue, alphaSlider.value)
    property color colorSelectorValue: ColorFunctions.hsba(colorSlider.value, 1, 1, 1)


    implicitWidth: 267
    implicitHeight: 140
    //color: "transparent"

    //property variant paramObject: model.object

    Column {
        Text {
            id: titleColorPicker
            color: "white"
            //text: paramObject.text
        }

        Row{
            spacing: 5

            ColorSelector{
                id: colorSelector
                height: colorPicker.height
                width: height
                currentColor: colorSelectorValue
            }
            ColorSlider{
                id: colorSlider
                height: colorPicker.height
                //cursorColorPositionSlider: (colorInputs.cursorColorPositionInputs)/765 * colorPicker.height
            }
            ColorInputs{
                id: colorInputs
                height: colorPicker.height
                currentColor: colorPicker.colorValue
                // if we try to implement that as a property of colorPicker, we have no more capital letters...
                alphaColorText: ColorFunctions.fullColorString(colorPicker.colorValue, alphaSlider.value)
                redValue: ColorFunctions.getChannelStr(colorPicker.colorValue, 0)
                greenValue: ColorFunctions.getChannelStr(colorPicker.colorValue, 1)
                blueValue: ColorFunctions.getChannelStr(colorPicker.colorValue, 2)
                hValue: colorSlider.value.toFixed(2)
                sValue: colorSelector.saturation.toFixed(2)
                bValue: colorSelector.brightness.toFixed(2)
                alphaValue: Math.ceil(alphaSlider.value*255)
            }
        }
    }
}