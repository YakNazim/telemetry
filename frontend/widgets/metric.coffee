class window.Metric extends Widget

    constructor: (id, @node) ->
        super(id)
        @datastring = @node.getAttribute "data-bind"

    update: (d) ->
        val = d.get(@datastring)
        if typeof val == 'number'
            val = val.toFixed(2)
        @node.innerHTML = val
