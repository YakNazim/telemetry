class Sky extends Widget

    constructor: (id, @node) ->
        super(id)
        @datastring = @node.getAttribute "data-bind"
        @skychart = new Skychart(@node, true)

    update: (d) ->
        val = d.get(@datastring)
        if '-' not in val
            @skychart.update(val)

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

        @r = d3.scale.linear()
            .domain([0, Math.PI/2])
            .range([@horizon, 0])

        # horizon
        @svg.append("circle")
            .attr('class', 'horizon')
            .attr('cx', @width/2)
            .attr('cy', @height/2)
            .attr('r', @horizon)

        # zenith
        @svg.append("line")
            .attr('class', 'zenith')
            .attr('x1', @width/2 - 5)
            .attr('y1', @height/2)
            .attr('x2', @width/2 + 5)
            .attr('y2', @height/2)
        @svg.append("line")
            .attr('class', 'zenith')
            .attr('x1', @width/2)
            .attr('y1', @height/2 - 5)
            .attr('x2', @width/2)
            .attr('y2', @height/2 + 5)

        # grid
        for i in [1...3] by 1
            @mark = i * (@horizon / 3)

            @svg.append("circle")
                .attr('class', 'grid')
                .attr('cx', @width/2)
                .attr('cy', @height/2)
                .attr('r', @mark)

    update: (data)->
        rad = @r
        x = @width/2
        y = @height/2
        sats = @svg.selectAll('.sat').data(data)
            .enter()
              .append("g")
                .attr('class', 'sat')
                .attr("transform", (d) ->
                    dx = rad(d.alt)*Math.cos(d.az+(Math.PI/2)) + x
                    dy = rad(d.alt)*Math.sin(d.az+(Math.PI/2)) + y
                    return "translate("+dx+","+dy+")")

        sats.append('circle')
            .attr('r', 7)

        sats.append('text')
            .attr("text-anchor", "middle")
            .attr('y', 16)
            .attr('x', 1)
            .text((d) -> d.prn )
