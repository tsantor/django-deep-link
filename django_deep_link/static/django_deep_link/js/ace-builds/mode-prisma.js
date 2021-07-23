ace.define("ace/mode/prisma_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"],function(e,t,n){"use strict";var r=e("../lib/oop"),i=e("./text_highlight_rules").TextHighlightRules,s=function(){this.$rules={start:[{include:"#triple_comment"},{include:"#double_comment"},{include:"#model_block_definition"},{include:"#config_block_definition"},{include:"#enum_block_definition"},{include:"#type_definition"}],"#model_block_definition":[{token:["source.prisma.embedded.source","storage.type.model.prisma","source.prisma.embedded.source","entity.name.type.model.prisma","source.prisma.embedded.source","punctuation.definition.tag.prisma"],regex:/^(\s*)(model|type)(\s+)([A-Za-z][\w]*)(\s+)({)/,push:[{token:"punctuation.definition.tag.prisma",regex:/\s*\}/,next:"pop"},{include:"#triple_comment"},{include:"#double_comment"},{include:"#field_definition"},{defaultToken:"source.prisma.embedded.source"}]}],"#enum_block_definition":[{token:["source.prisma.embedded.source","storage.type.enum.prisma","source.prisma.embedded.source","entity.name.type.enum.prisma","source.prisma.embedded.source","punctuation.definition.tag.prisma"],regex:/^(\s*)(enum)(\s+)([A-Za-z][\w]*)(\s+)({)/,push:[{token:"punctuation.definition.tag.prisma",regex:/\s*\}/,next:"pop"},{include:"#triple_comment"},{include:"#double_comment"},{include:"#enum_value_definition"},{defaultToken:"source.prisma.embedded.source"}]}],"#config_block_definition":[{token:["source.prisma.embedded.source","storage.type.config.prisma","source.prisma.embedded.source","entity.name.type.config.prisma","source.prisma.embedded.source","punctuation.definition.tag.prisma"],regex:/^(\s*)(generator|datasource)(\s+)([A-Za-z][\w]*)(\s+)({)/,push:[{token:"source.prisma.embedded.source",regex:/\s*\}/,next:"pop"},{include:"#triple_comment"},{include:"#double_comment"},{include:"#assignment"},{defaultToken:"source.prisma.embedded.source"}]}],"#assignment":[{token:["text","variable.other.assignment.prisma","text","keyword.operator.terraform","text"],regex:/^(\s*)(\w+)(\s*)(=)(\s*)/,push:[{token:"text",regex:/$/,next:"pop"},{include:"#value"},{include:"#double_comment_inline"}]}],"#field_definition":[{token:["text","variable.other.assignment.prisma","invalid.illegal.colon.prisma","text","support.type.primitive.prisma","keyword.operator.list_type.prisma","keyword.operator.optional_type.prisma","invalid.illegal.required_type.prisma"],regex:/^(\s*)(\w+)((?:\s*:)?)(\s+)(\w+)((?:\[\])?)((?:\?)?)((?:\!)?)/},{include:"#attribute_with_arguments"},{include:"#attribute"}],"#type_definition":[{token:["text","storage.type.type.prisma","text","entity.name.type.type.prisma","text","support.type.primitive.prisma"],regex:/^(\s*)(type)(\s+)(\w+)(\s*=\s*)(\w+)/},{include:"#attribute_with_arguments"},{include:"#attribute"}],"#enum_value_definition":[{token:["text","variable.other.assignment.prisma","text"],regex:/^(\s*)(\w+)(\s*$)/},{include:"#attribute_with_arguments"},{include:"#attribute"}],"#attribute_with_arguments":[{token:["entity.name.function.attribute.prisma","punctuation.definition.tag.prisma"],regex:/(@@?[\w\.]+)(\()/,push:[{token:"punctuation.definition.tag.prisma",regex:/\)/,next:"pop"},{include:"#named_argument"},{include:"#value"},{defaultToken:"source.prisma.attribute.with_arguments"}]}],"#attribute":[{token:"entity.name.function.attribute.prisma",regex:/@@?[\w\.]+/}],"#array":[{token:"source.prisma.array",regex:/\[/,push:[{token:"source.prisma.array",regex:/\]/,next:"pop"},{include:"#value"},{defaultToken:"source.prisma.array"}]}],"#value":[{include:"#array"},{include:"#functional"},{include:"#literal"}],"#functional":[{token:["support.function.functional.prisma","punctuation.definition.tag.prisma"],regex:/(\w+)(\()/,push:[{token:"punctuation.definition.tag.prisma",regex:/\)/,next:"pop"},{include:"#value"},{defaultToken:"source.prisma.functional"}]}],"#literal":[{include:"#boolean"},{include:"#number"},{include:"#double_quoted_string"},{include:"#identifier"}],"#identifier":[{token:"support.constant.constant.prisma",regex:/\b(?:\w)+\b/}],"#map_key":[{token:["variable.parameter.key.prisma","text","punctuation.definition.separator.key-value.prisma","text"],regex:/(\w+)(\s*)(:)(\s*)/}],"#named_argument":[{include:"#map_key"},{include:"#value"}],"#triple_comment":[{token:"comment.prisma",regex:/\/\/\//,push:[{token:"comment.prisma",regex:/$/,next:"pop"},{defaultToken:"comment.prisma"}]}],"#double_comment":[{token:"comment.prisma",regex:/\/\//,push:[{token:"comment.prisma",regex:/$/,next:"pop"},{defaultToken:"comment.prisma"}]}],"#double_comment_inline":[{token:"comment.prisma",regex:/\/\/[^$]*/}],"#boolean":[{token:"constant.language.boolean.prisma",regex:/\b(?:true|false)\b/}],"#number":[{token:"constant.numeric.prisma",regex:/(?:0(?:x|X)[0-9a-fA-F]*|(?:\+|-)?\b(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:(?:e|E)(?:\+|-)?[0-9]+)?)(?:[LlFfUuDdg]|UL|ul)?\b/}],"#double_quoted_string":[{token:"string.quoted.double.start.prisma",regex:/"/,push:[{token:"string.quoted.double.end.prisma",regex:/"/,next:"pop"},{include:"#string_interpolation"},{token:"string.quoted.double.prisma",regex:/[\w\-\/\._\\%@:\?=]+/},{defaultToken:"unnamed"}]}],"#string_interpolation":[{token:"keyword.control.interpolation.start.prisma",regex:/\$\{/,push:[{token:"keyword.control.interpolation.end.prisma",regex:/\s*\}/,next:"pop"},{include:"#value"},{defaultToken:"source.tag.embedded.source.prisma"}]}]},this.normalizeRules()};s.metaData={name:"Prisma",scopeName:"source.prisma"},r.inherits(s,i),t.PrismaHighlightRules=s}),ace.define("ace/mode/folding/cstyle",["require","exports","module","ace/lib/oop","ace/range","ace/mode/folding/fold_mode"],function(e,t,n){"use strict";var r=e("../../lib/oop"),i=e("../../range").Range,s=e("./fold_mode").FoldMode,o=t.FoldMode=function(e){e&&(this.foldingStartMarker=new RegExp(this.foldingStartMarker.source.replace(/\|[^|]*?$/,"|"+e.start)),this.foldingStopMarker=new RegExp(this.foldingStopMarker.source.replace(/\|[^|]*?$/,"|"+e.end)))};r.inherits(o,s),function(){this.foldingStartMarker=/([\{\[\(])[^\}\]\)]*$|^\s*(\/\*)/,this.foldingStopMarker=/^[^\[\{\(]*([\}\]\)])|^[\s\*]*(\*\/)/,this.singleLineBlockCommentRe=/^\s*(\/\*).*\*\/\s*$/,this.tripleStarBlockCommentRe=/^\s*(\/\*\*\*).*\*\/\s*$/,this.startRegionRe=/^\s*(\/\*|\/\/)#?region\b/,this._getFoldWidgetBase=this.getFoldWidget,this.getFoldWidget=function(e,t,n){var r=e.getLine(n);if(this.singleLineBlockCommentRe.test(r)&&!this.startRegionRe.test(r)&&!this.tripleStarBlockCommentRe.test(r))return"";var i=this._getFoldWidgetBase(e,t,n);return!i&&this.startRegionRe.test(r)?"start":i},this.getFoldWidgetRange=function(e,t,n,r){var i=e.getLine(n);if(this.startRegionRe.test(i))return this.getCommentRegionBlock(e,i,n);var s=i.match(this.foldingStartMarker);if(s){var o=s.index;if(s[1])return this.openingBracketBlock(e,s[1],n,o);var u=e.getCommentFoldRange(n,o+s[0].length,1);return u&&!u.isMultiLine()&&(r?u=this.getSectionRange(e,n):t!="all"&&(u=null)),u}if(t==="markbegin")return;var s=i.match(this.foldingStopMarker);if(s){var o=s.index+s[0].length;return s[1]?this.closingBracketBlock(e,s[1],n,o):e.getCommentFoldRange(n,o,-1)}},this.getSectionRange=function(e,t){var n=e.getLine(t),r=n.search(/\S/),s=t,o=n.length;t+=1;var u=t,a=e.getLength();while(++t<a){n=e.getLine(t);var f=n.search(/\S/);if(f===-1)continue;if(r>f)break;var l=this.getFoldWidgetRange(e,"all",t);if(l){if(l.start.row<=s)break;if(l.isMultiLine())t=l.end.row;else if(r==f)break}u=t}return new i(s,o,u,e.getLine(u).length)},this.getCommentRegionBlock=function(e,t,n){var r=t.search(/\s*$/),s=e.getLength(),o=n,u=/^\s*(?:\/\*|\/\/|--)#?(end)?region\b/,a=1;while(++n<s){t=e.getLine(n);var f=u.exec(t);if(!f)continue;f[1]?a--:a++;if(!a)break}var l=n;if(l>o)return new i(o,r,l,t.length)}}.call(o.prototype)}),ace.define("ace/mode/prisma",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/prisma_highlight_rules","ace/mode/folding/cstyle"],function(e,t,n){"use strict";var r=e("../lib/oop"),i=e("./text").Mode,s=e("./prisma_highlight_rules").PrismaHighlightRules,o=e("./folding/cstyle").FoldMode,u=function(){this.HighlightRules=s,this.foldingRules=new o};r.inherits(u,i),function(){this.lineCommentStart="//",this.$id="ace/mode/prisma"}.call(u.prototype),t.Mode=u});                (function() {
                    ace.require(["ace/mode/prisma"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
