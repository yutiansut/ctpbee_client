// Created by Ethan Chiu 2016
// Updated August 4, 2018

$(document).ready(function () {
    //Pulls info from AJAX call and sends it off to codemirror's update linting
    //Has callback result_cb
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/check_disconnect');
    var click_count = 0;

    function check_syntax(code, result_cb) {
        //Example error for guideline
        var error_list = [{
            line_no: null,
            column_no_start: null,
            column_no_stop: null,
            fragment: null,
            message: null,
            severity: null
        }];

        //Push and replace errors
        function check(data) {
            //Clear array.
            error_list = [{
                line_no: null,
                column_no_start: null,
                column_no_stop: null,
                fragment: null,
                message: null,
                severity: null
            }];//Check if pylint output is empty.
            if (data == null) {
                result_cb(error_list);
            }
        }

        //AJAX call to pylint
        $.post('/check_code', {
            text: code
        }, function (data) {
            current_text = data;
            check(current_text);
            return false;
        }, 'json');
    }

    var editor = CodeMirror.fromTextArea(document.getElementById("txt"), {
        mode: {
            name: "python",
            version: 3,
            singleLineStringErrors: false
        },
        //代码折叠
        lineWrapping: true,
        foldGutter: true,
        gutters: ["CodeMirror-lint-markers", "CodeMirror-foldgutter"],

        lineNumbers: true,
        indentUnit: 4,
        //括号匹配
        matchBrackets: true,
        lint: true,
        styleActiveLine: true,
        //智能提示
        extraKeys: {"Ctrl": "autocomplete"},
        lintWith: {
            "getAnnotations": CodeMirror.remoteValidator,
            "async": true,
            "check_cb": check_syntax
        },
    });
    //Actually Run in Python
    $("#run").click(function () {
        $.post('/run_code', {
            text: editor.getValue()
        }, function (data) {
            print_result(data);
            return false;
        }, 'json');

        function print_result(data) {
            document.getElementById('output').innerHTML = '';
            $("#output").append("<pre>" + data + "</pre>");
        }
    });
});
