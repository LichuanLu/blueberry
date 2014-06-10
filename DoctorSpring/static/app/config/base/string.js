define([], function() {
  // body...
  "use strict";
  var defaultToWhiteSpace = function(characters) {
    if (characters == null) {
      return '\\s';

    } else if (characters.source) {
      return characters.source;

    } else {
      return '[' + res.escapeRegExp(characters) + ']';

    }
  };

  var nativeTrim = String.prototype.trim;
  var nativeTrimRight = String.prototype.trimRight;
  var nativeTrimLeft = String.prototype.trimLeft;
  var res = {


    trim: function(str, characters) {
      if (str == null) {
        return '';
      }
      if (!characters && nativeTrim) {
        return nativeTrim.call(str);
      }
      characters = defaultToWhiteSpace(characters);
      return String(str).replace(new RegExp('\^' + characters + '+|' + characters + '+$', 'g'), '');
    },

    ltrim: function(str, characters) {
      if (str == null) {
        return '';
      }
      if (!characters && nativeTrimLeft) {
        return nativeTrimLeft.call(str);
      }
      characters = defaultToWhiteSpace(characters);
      return String(str).replace(new RegExp('^' + characters + '+'), '');
    },

    rtrim: function(str, characters) {
      if (str == null) {
        return '';
      }
      if (!characters && nativeTrimRight) {
        return nativeTrimRight.call(str);
      }
      characters = defaultToWhiteSpace(characters);
      return String(str).replace(new RegExp(characters + '+$'), '');
    },
    escapeRegExp: function(str) {
      if (str == null) {
        return '';
      }
      return String(str).replace(/([.*+?^=!:${}()|[\]\/\\])/g, '\\$1');
    }
  }

  return res

});