class Sky extends Widget

    constructor: (id, @node) ->
        super(id)
        @datastring = @node.getAttribute "data-bind"
        @skychart = new Skychart(@node, true)

    update: (d) ->
        val = d.get(@datastring)
        console.log(val)

class Skychart

    constructor: (node) ->
        @margin =
            top: 10
            right: 10
            bottom: 10
            left: 10

        w = node.clientWidth
        h = node.clientHeight

        @width = w - @margin.left - @margin.right
        @height = h - @margin.top - @margin.bottom

        @svg = d3.select(node).append('svg')
            .attr('class', 'chart')
            .attr('width', @width + @margin.left + @margin.right)
            .attr('height', @height + @margin.top + @margin.bottom)
            .append("g")
                .attr("transform", "translate(" + @margin.left + "," + @margin.top + ")")


        @horizon = if @width <= @height then @width/2 else  @height /2
        @svg.append("circle")
            .attr('class', 'horizon')
            .attr('cx', @width/2)
            .attr('cy', @height/2)
            .attr('r', @horizon)


