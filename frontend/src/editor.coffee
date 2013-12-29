# Controls for adding and editing layouts

jquery = $

types = ['text', 'chart']

tiles = []

class Tile

    # instance variables
    type = 'text'
    title = 'Title'
    sizex = 2
    sizey = 1
    coords = [1,1]

    constructor: (@id) ->

    sizex: sizex
    sizey: sizey

    html: () ->
        h  = '<li id="#' + @id + '" class="tile">'
        h += ' <div class="col-sm-5"><input type="text" class="form-control input-sm" placeholder="' + title + '"></div>'
        h += ' <div class="col-sm-2">Type:</div>'
        h += ' <div class="col-sm-5">'
        h += '  <select class="form-control">'
        h += '   <option>Text Values</option>'
        h += '  </select>'
        h += '</div>'
        h += '</li>'
        h

window.addLine = (button) ->
    console.log jquery(button)

window.addTile = () ->
    t = new Tile('asdf')
    tiles.push t
    t
