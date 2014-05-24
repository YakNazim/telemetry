class Metric extends Widget

    constructor: (id, @node) ->
        super(id)
        @buffer = []
        @datastring = @node.getAttribute "data-bind"
        @format = @node.getAttribute "data-format"
        @select = @node.getAttribute "data-select"
        @viztype = @node.getAttribute "data-viz"
        @range = @node.getAttribute "data-range"

        if @select?
            @select = JSON.parse @select

        if @range?
            @range = JSON.parse @range
        else
            @range = [10,-10]

        @number = @node.firstElementChild
        @chart = @node.children[1]

        if @chart?

            if @viztype == 'sparkline'
                if @number.className.indexOf('key') > 0
                    @spark = new Sparkline(@chart, true, @range)
                else
                    @spark = new Sparkline(@chart, false, @range)

            if @viztype == 'gauge'
                margin =
                    top: 0
                    right: 15
                    bottom: 17
                    left: 15
                @viz = new GaugeViz(@chart, margin, @range)

    update: (d) ->
        val = d.get(@datastring)
        if typeof val == 'number'
            if @spark?
                tbase = @datastring.split '.'
                time = d.get('d.' + tbase[1] + '.timestamp')
                now = d.get('d.servertime')
                if val? and time?
                    message =
                        v: val
                        t: time
                    if @buffer.length < 1
                        @buffer.push message
                    if @buffer[@buffer.length - 1].t != time
                        @buffer.push message

                @spark.update @buffer, now

            if @viz?
                @viz.update val

            if @format != 'special'
                val = sprintf @format, val
            else
                if @select?
                    for t in @select
                        if val == t[0]
                            val = t[1]
                
        else
            val = '<span class="nodata">' + val + '</span>'
        @number.innerHTML = val
