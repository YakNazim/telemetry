
class window.Widget

    constructor: (@id) ->

    update: (d) ->


class window.Packets extends Widget

    constructor: (id) ->
        super(id)

    update: (d) ->
        place = document.getElementById(@id)
        place.innerHTML = '<span>Time Since Last FC Packet: </span>'
        place.innerHTML += d.get('d.servertime - d.RECV_fc.TimeLastPacketReceived')
        return


class window.Message extends Widget

    constructor: (id) ->
        super(id)
        @buffer = []

    update: (d) ->
        message = d.get('d.MESG')

        if message? and message not in @buffer
            @buffer.push message

        place = document.getElementById(@id)
        place.innerHTML = '<span>Messages: </span><br>'
        for msg in @buffer
            place.innerHTML += msg['Message']+'<br>'

        console.log d.get('d')

class window.Graph extends Widget

    constructor: (id) ->
        super(id)
        @div = document.getElementById(@id)
        @buffer = []

    update: (d) ->
        value = d.get('d.ADIS.Acc_X_mean')
        time = d.get('d.ADIS.timestamp')
        
        if value? and time?
            message =
                v: value
                t: time
            if @buffer.length < 1
                @buffer.push message
            if @buffer[@buffer.length - 1].t != time
                @buffer.push message

        @div.innerHTML = ''
        for n in @buffer
            @div.innerHTML += '<li>'+n.v+'|'+n.t+'</li>'
