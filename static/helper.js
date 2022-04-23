function EnterExec(jq, callback){ //press enter to execute
  $(jq).keypress(function(e){
    if(e.which == 13){
      callback();
    }
  });
}

function linkify(inputText) { // replace link with <a> tag
  // from https://stackoverflow.com/a/49634926/15493213
  var replacedText, replacePattern1, replacePattern2, replacePattern3;
  //URLs starting with http://, https://, or ftp://
  replacePattern1 = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
  replacedText = inputText.replace(replacePattern1, '<a href="$1" target="_blank">$1</a>');
  return replacedText;
}

function htmlifly(inputText){ //replace html tag
  replacedText = inputText.replaceAll('\n', '<br>');
  replacedText = linkify(replacedText);
  return replacedText
}