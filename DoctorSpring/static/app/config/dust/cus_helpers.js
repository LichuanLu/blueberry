dust.helpers['pager'] = function(chunk, context, bodies, params) {

  var first,last;
  //tapping these to get the actual value (since we passed vsaraibles) and casting as a number with '+'
  first = +dust.helpers.tap(params.first, chunk, context);
  last = +dust.helpers.tap(params.last, chunk, context);

  //this one is all ready since we just passed a string
  //url = params.url;

  //build our html - do whatever you need here - this is an example
  // var html = '<ul>';
  var html = '';
  for(var i = first; i <= last; i++) {
    //I used a replace and placeholder - prob other methods you can use
    if( i == first){
          html += ('<li class="active"><a href="#">' + i +'</a></li>');

    }else{
          html += ('<li><a href="#">' + i +'</a></li>');

    }

    // if(url){
    //   html += '<a href="' + url.replace('%page%', i) + '">' + i '</a>';

    // }else{
    //   html += '<a href="#">' + i '</a>';

    // }
  }
  // html += '</ul>';

  //write this back to the template
  chunk.write(html);

  //return it
  return chunk;

};