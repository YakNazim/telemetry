class Metric extends Widget

    constructor: (id, @node) ->
        super(id)
        @buffer = []
        @datastring = @node.getAttribute "data-bind"
        @format = @node.getAttribute "data-format"
        @select = @node.getAttribute "data-select"
        if @select?
            @select = JSON.parse @select
        @number = @node.firstElementChild
        @chart = @node.children[1]
        if @chart?
            if @number.className.indexOf('key') > 0
                @spark = new Sparkline(@chart, true)
            else
                @spark = new Sparkline(@chart, false)

    update: (d) ->
        val = d.get(@datastring)
        if typeof val == 'number'
            if @spark?
                time = d.get('d.ADIS.timestamp')
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
