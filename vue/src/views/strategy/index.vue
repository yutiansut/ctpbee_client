<template>
  <div class="app-container">
    <textarea id="txt">
    class Foo:
        def __init__(self):
            self.cn = "大锅大嫂过年好～"
            self.en = 'Happy New Year to Big Brother and Big Sister-in-law~'

        def makeSense(self):
            print(self.cn)
            print(self.en)

    x = Foo()
    x.makeSense()

    #test error and warn
    def foo(bar, baz):
        pass
    foo(42)
    </textarea>
    <br />
    <button type="button" id="run" class="btn btn-success">Run</button>
    <br />

    <div class="alert alert-warning alert-dismissible" role="alert" id="info">
      <button type="button" class="close" id="close" style="opacity: 1;color:#fff">
        <span>&times;</span>
      </button>
      <div class="container">
        <b>Result:</b>
        <pre id="info-content"></pre>
      </div>
    </div>
  </div>
</template>

<script>
//codemirror.js
import "@/assets/codemirror/codemirror.js";//1

import "@/assets/js/pylint_js/cm-validator-remote.js";//2
//addon
import "@/assets/codemirror/addon/search.js";//3
import "@/assets/codemirror/addon/searchcursor.js";//4
import "@/assets/codemirror/addon/dialog.css";
import "@/assets/codemirror/addon/dialog.js";
//lib
import "@/assets/codemirror/lib/python.js";
import "@/assets/codemirror/lib/lint.js";

import "@/assets/codemirror/hint/show-hint.js";

import "@/assets/codemirror/hint/anyword-hint.js";

import "@/assets/codemirror/lib/matchbrackets.js";

import "@/assets/codemirror/lib/codemirror.css";
import "@/assets/codemirror/lib/lint.css";


//hint

import "@/assets/codemirror/hint/show-hint.css";

//js
import "@/assets/js/pylint_js/require.min.js";
import "@/assets/js/pylint_js/javascript.js";



export default {
  data() {
    return {};
  },
  created() {},
  methods: {}
};
</script>
