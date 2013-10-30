# Main PSAS Controller.

# inject context into a function that is othewise called globally
proxy = (fn, context) ->
    p = -> fn.apply(context)
    return p


# A PSAS Backend connection class
class Connection

    @server = 'ws://'+ location.host + '/ws'

    # This is our connection event
    @onopen: (evt) ->
        console.log 'CONNECTED'
        document.getElementById("status").innerHTML = "Connected"
        return

    # Disconnect event
    @onclose: (evt) ->
        console.log 'DISCONNECT'
        #document.getElementById("status").innerHTML = "Not Connected"
        return


    # instance variables
    websocket = null
    retries = 0

    constructor: ->
        @openWebSocket()

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
            @constructor.onopen(evt)
            return

        @websocket.onclose = (evt) =>
            @retry()
            @constructor.onclose(evt)
            return

        @websocket.onerror = (evt) =>
            console.log 'ERROR', evt
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

data = new CurrentData()

conn = new Connection()

#conn.retryWebSocket()

#console.log data.get('Math.sqrt((d.adis.acc*d.adis.acc) + (d.adis.gry*d.adis.gry))')
