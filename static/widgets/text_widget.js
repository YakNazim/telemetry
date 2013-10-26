function TextWidget(config) {

    Widget.call(this, config);

    function pad(n, width, z) {
        z = z || '0';   // Defualt padding char
        n = n + '';
        return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
    }


    var text = '<h2>' + config.id + '</h2>';
    text    += '<table><tbody>';
    this.config.controls.forEach( function (control) {
       text += '<tr><td class="label">' + control.label + ':' + '</td><td> </td><td> </td></tr>';
    });
    text    += '</tbody></table>';
    this.div.innerHTML = text;

    this.onControlChanged = function (control) {
        var text = '<h2>' + config.id + '</h2>';
        text    += '<table><tbody>';
        this.config.controls.forEach( function (control) {
           text += '<tr><td class="label">';
           text += control.label;
           text += ':</td><td><value style="color:';
           text += control.color + '">';
           text += pad(control.value, 10, '&nbsp;');
           text += ' </value></td><td class="units">';
           if (control.units)
                text += '[' + control.units + ']';
          text += '</span></td></tr>';
        });
        text    += '</tbody></table>';
        this.setText(text);
    };

    this.setText = function (text) {
        this.div.innerHTML = text;
    };
}

TextWidget.prototype = Object.create(Widget.prototype, {constructor: {value: TextWidget, enumerable: false, writable: true, configurable: true}});
