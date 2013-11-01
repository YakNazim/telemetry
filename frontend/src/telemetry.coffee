# Main PSAS Controller.

# inject context into a function that is othewise called globally
proxy = (fn, context) ->
    p = -> fn.apply(context)
    return p


# A PSAS Backend connection class
class Connection

    @server = 'ws://'+ location.host + '/ws'

    # instance variables
    websocket = null
    retries = 0

    constructor: (@data) ->
        @openWebSocket()

    # This is our connection event
    onopen: (evt) ->
        document.getElementById("status").innerHTML = "Connected"
        return

    # Disconnect event
    onclose: (evt) ->
        return

    # Message event
    onmessage: (evt) ->
        @data.update(evt.data)
        return

    retry: ->
        document.getElementById("status").innerHTML = "Retrying.." + @retries
        setTimeout proxy(@openWebSocket, @), 1000

    openWebSocket: ->
        @retries++
        console.log 'RETRY'

        # Cancel if already open
        if @websocket? and @websocket is WebSocket.OPEN
            console.log 'ALREADY OPEN'
            return

        @websocket = new WebSocket @constructor.server

        @websocket.onopen = (evt) =>
            @retries = 0
            @onopen(evt)
            return

        @websocket.onclose = (evt) =>
            @retry()
            @onclose(evt)
            return

        @websocket.onerror = (evt) =>
            console.log 'ERROR', evt
            return

        @websocket.onmessage = (evt) =>
            console.log 'MESSAGE'
            @onmessage(evt)
            return

        return


class CurrentData

    # Data state
    d = null

    # update state with current data
    update: (chunk) ->
        d = JSON.parse chunk
        return

    # Clean state
    clean: ->
        d = null
        return

    # Eval expression and return data, or null if broken
    get: (expression) ->
        r = null
        try r = eval(expression)
        return r


# Run
data = new CurrentData()
conn = new Connection(data)

setTimeout  (-> console.log data.get('d.ADIS.VCC + 1')), 3000
