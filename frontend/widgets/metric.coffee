class window.Metric extends Widget

    constructor: (id, @node) ->
        super(id)
        @datastring = @node.getAttribute "data-bind"

    update: (d) ->
        val = d.get(@datastring)
        if typeof val == 'number'
            val = sprintf("%5.1f", val)
        else
            val = '<span class="nodata">' + val + '</span>'
        @node.innerHTML = val
