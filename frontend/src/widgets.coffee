
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
