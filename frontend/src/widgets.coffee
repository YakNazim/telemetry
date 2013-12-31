
# A base Widget class
class Widget

    constructor: (@id) ->

    update: (d) ->

    editor: () ->
        h = '<div>&nbsp;</div>'
        h


class window.Graph extends Widget

    constructor: (id) ->
        super(id)
        @div = document.getElementById(@id)
        @chart = new CanvasChart(@id)
        @buffer = []

    update: (d) ->
        value = d.get('d.ADIS.Acc_X_mean')
        time = d.get('d.ADIS.timestamp')
        now = d.get('d.servertime')
        
        if value? and time?
            message =
                v: value
                t: time
            if @buffer.length < 1
                @buffer.push message
            if @buffer[@buffer.length - 1].t != time
                @buffer.push message

        @chart.update @buffer, now
        #@div.innerHTML = ''
        #for n in @buffer
        #    @div.innerHTML += '<li>'+n.v+'|'+n.t+'</li>'
