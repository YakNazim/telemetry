# Controls for adding and editing layouts

types = ['text', 'chart']

tiles = []

class Tile

    # instance variables
    type = 'text'
    title = 'Title'
    sizex = 1
    sizey = 1
    coords = [1,1]

    constructor: (@id) ->

    html: () ->
        h  = '<li class="tile">'
        h += '<input type="text" value="Title">'
        h += '<span>Widget Type:</span>'
        h += '<select class="form-control">'
        h += '  <option>Text Values</option>'
        h += '</select>'
        h += '<ul class="lines">'
        h += '  <li><input type="text" value="Name">:<input type="text" value="data"> [<input type="text" value="units">]</li>'
        h += '  <li><button>Add line</button></li>'
        h += '</ul>'
        h += '</li>'
        h


window.addTile = () ->
    t = new Tile('asdf')
    tiles.push t
    t
