
class window.Widget

    constructor: (@id) ->

    update: (d) ->

class window.Packets extends Widget

    constructor: (id) ->
        super(id)

    update: (d) ->
        document.getElementById(@id).innerHTML = d.get('d.servertime - d.RECV_fc.TimeLastPacketReceived')


class window.Message extends Widget

    update: (d) ->
        console.log d.get('d')
