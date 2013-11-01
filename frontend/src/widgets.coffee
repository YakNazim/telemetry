
class window.Widget

    constructor: (@id) ->

    update: (d) ->

class window.Message extends Widget

    update: (d) ->
        console.log d.get('d')
