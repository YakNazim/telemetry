class window.WidgetText extends window.Widget

    constructor: (id) ->
        super(id)

    editor: () ->
        h =  '<ul>'
        h += '<li>'
        h += ' <form class="form-inline" role="form">'
        h += '  <div class="form-group">'
        h += '   <input type="text" class="form-control" id="linetitle" placeholder="Field Title">'
        h += '  </div>'
        h += '  <div class="form-group">'
        h += '   <input type="text" class="form-control" id="lineinput" placeholder="Datafield">'
        h += '  </div>'
        h += '  <button type="submit" onclick="return false;" class="btn btn-primary">Add Row</button>'
        h += ' </form>'
        h += '</li>'
        h += '</ul>'
        h
