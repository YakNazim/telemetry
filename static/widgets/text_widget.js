function TextWidget(config) {
    Widget.call(this, config);

    //$('.container').append("<script type=\"text/javascript\">document.getElementById('widget " + this.config.id + "').style.width=\"" + this.config.width + "px\";</script>");
    //$('.container').append("<script type=\"text/javascript\">document.getElementById('widget " + this.config.id + "').style.height=\"" + this.config.height + "px\";</script>");

    var text = '<h2>' + config.id + '</h2>';
    text    += '<table><tbody>';
    this.config.controls.forEach(function(control) {
       text += '<tr><td class="label">' + control.label + ':' + '</td><td> </td><td> </td></tr>';
    });
    text    += '</tbody></table>';
    this.div.innerHTML = text;
    
    this.onControlChanged = function(control) {
        var text = '<h2>' + config.id + '</h2>';
        text    += '<table><tbody>';
        this.config.controls.forEach(function(control) {
           text += '<tr><td class="label">' + control.label + ':</td><td><value style="color:' + control.color + '">' + control.value + ' </value></td><td class="units">[' + control.units + ']</span></td></tr>';
        });
        text    += '</tbody></table>';
        this.setText(text);
    };

    this.setText = function(text) {
        this.div.innerHTML = text;
    };
}

TextWidget.prototype = Object.create(Widget.prototype, {constructor: {value: TextWidget, enumerable: false, writable: true, configurable: true}});
