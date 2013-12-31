class window.Metric extends Widget

    constructor: (id, @node) ->
        super(id)
        @datastring = @node.getAttribute "data-bind"

    update: (d) ->
        @node.innerHTML = d.get(@datastring)
