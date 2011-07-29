$(document).ready(function($)
{
  $('#id_content').wysiwyg({
    resizeOptions: {},
    controls: {
      strikeThrough : { visible : true },
      underline     : { visible : true },
      
      justifyLeft   : { visible : true },
      justifyCenter : { visible : true },
      justifyRight  : { visible : true },
      justifyFull   : { visible : true },
      
      indent  : { visible : true },
      outdent : { visible : true },
      
      subscript   : { visible : true },
      superscript : { visible : true },
      
      undo : { visible : true },
      redo : { visible : true },
      
      insertOrderedList    : { visible : true },
      insertUnorderedList  : { visible : true },
      insertHorizontalRule : { visible : true },

      
      cut   : { visible : true },
      copy  : { visible : true },
      paste : { visible : true },
      html  : { visible: true },
      exam_html: { exec: function() { this.insertHtml('<abbr title="exam">Jam</abbr>') }, visible: true  }
    },
    /*
    events: {
      click : function(e)
      {
        if ($('#click-inform:checked').length > 0)
        {
          e.preventDefault();
          alert('You have clicked jWysiwyg content!');
        }
      }
    }
     */
  });
});
