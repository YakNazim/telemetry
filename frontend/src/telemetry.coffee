# Main PSAS Controller.

# inject context into a function that is othewise called globally
proxy = (fn, context) ->
    p = -> fn.apply(context)
    return p


# PSAS Backend connection class
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

        WebSocket = window.WebSocket || window.MozWebSocket
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
            #console.log 'MESSAGE'
            @onmessage(evt)
            return

        return

# Contains and handles current data
class CurrentData

    # Data state
    d = {}

    constructor: (@widgets) ->

    # update state with current data
    update: (chunk) ->
        newd = JSON.parse chunk
        for type of newd
            d[type] = newd[type]
        for wid in @widgets
            wid.update(@)
        return

    # Clean state
    clean: ->
        d = {}
        return

    # Eval expression and return data, or null if broken
    get: (expression) ->
        try
            ret = eval(expression)
        catch error
            # Turn on for debug:
            #console.log error
            ret = '-----'
        if not ret?
            ret = '-----'
        ret

# Run
window.start = () ->
    #g = new Graph('graphh')

    views = []

    # Get all data binds for metric types
    data_binds = $('.metric *[data-bind]')
    for node in data_binds
        n = new Metric('metric', node)
        views.push n

    # Get all data binds for sky types
    data_binds = $('.sky *[data-bind]')
    for node in data_binds
        n = new Sky('sky', node)
        views.push n


    data = new CurrentData(views)
    conn = new Connection(data)
