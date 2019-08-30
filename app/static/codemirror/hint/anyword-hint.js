// CodeMirror, copyright (c) by Marijn Haverbeke and others
// Distributed under an MIT license: https://codemirror.net/LICENSE
var kw = [' ', 'async', 'await', 'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue',
    'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if',
    'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
    'try', 'while', 'with', 'yield', 'abs', 'divmod', 'input', 'open', 'all', 'enumerate',
    'int', 'ord', 'any', 'eval', 'isinstance', 'pow', 'basestring', 'execfile', 'issubclass',
    'print', 'bin', 'file', 'iter', 'property', 'bool', 'filter', 'len', 'range', 'bytearray',
    'float', 'list', 'raw_input', 'callable', 'format', 'locals', 'reduce', 'chr', 'frozenset',
    'long', 'reload', 'classmethod', 'getattr', 'map', 'repr', 'cmp', 'globals', 'max', 'reversed',
    'compile', 'hasattr', 'memoryview', 'round', 'complex', 'hash', 'min', 'set', 'delattr', 'help',
    'next', 'setattr', 'dict', 'hex', 'object', 'slice', 'dir', 'id', 'oct', 'sorted',
    '@property', '@classmethod', '@staticmethod']

var pp = kw.join(" ");
(function (mod) {
    if (typeof exports == "object" && typeof module == "object") // CommonJS
        mod(require("../codemirror"));
    else if (typeof define == "function" && define.amd) // AMD
        define(["../codemirror"], mod);
    else // Plain browser env
        mod(CodeMirror);
})(function (CodeMirror) {
    "use strict";


    var WORD = /[\w$]+/, RANGE = 500;

    CodeMirror.registerHelper("hint", "anyword", function (editor, options) {
        var word = options && options.word || WORD;
        var range = options && options.range || RANGE;
        var cur = editor.getCursor(), curLine = editor.getLine(cur.line);
        var end = cur.ch, start = end;
        while (start && word.test(curLine.charAt(start - 1))) --start;
        var curWord = start != end && curLine.slice(start, end);
        var list = options && options.list || [], seen = {};
        var re = new RegExp(word.source, "g");
        for (var dir = -1; dir <= 1; dir += 2) {
            var line = cur.line,
                endLine = Math.min(Math.max(line + dir * range, editor.firstLine()), editor.lastLine()) + dir;

            for (; line != endLine; line += dir) {

                var text = editor.getLine(line), m;
                text += pp;
                while (m = re.exec(text)) {
                    if (line == cur.line && m[0] === curWord) continue;
                    if ((!curWord || m[0].lastIndexOf(curWord, 0) == 0) && !Object.prototype.hasOwnProperty.call(seen, m[0])) {
                        seen[m[0]] = true;
                        list.push(m[0]);
                    }
                }
            }
        }

        return {list: list, from: CodeMirror.Pos(cur.line, start), to: CodeMirror.Pos(cur.line, end)};
    });
});
