<template>
  <div class="quotation">
    <div class="in-coder-panel">
      <textarea ref="textarea"></textarea>
      <!-- <el-select class="code-mode-select" v-model="mode" @change="changeMode">
        <el-option v-for="mode in modes" :key="mode.value" :label="mode.label" :value="mode.value"></el-option>
      </el-select> -->
    </div>
    <el-button type="success" size="medium" @click="send(code)">RUN1</el-button>
    <el-button type="success" size="medium" @click="check_code(code)">RUN2</el-button>
    <el-drawer
      title="控制台"
      :visible.sync="drawer"
      :direction="direction"
      :before-close="handleClose"
      style="overflow:auto"
    >
      <span>
        <pre class="retrunMsg">{{returnData}}</pre>
      </span>
    </el-drawer>
  </div>
</template>

<script type="text/ecmascript-6">
// 引入全局实例
import _CodeMirror from "codemirror";

//代码折叠
import "codemirror/addon/fold/foldgutter.css";
import "codemirror/addon/fold/foldcode.js";
import "codemirror/addon/fold/foldgutter.js";
import "codemirror/addon/fold/brace-fold.js";
import "codemirror/addon/fold/comment-fold.js";
//括号匹配
import "codemirror/addon/edit/matchbrackets.js";
//自动补全
import "codemirror/addon/hint/show-hint.css";
import "codemirror/addon/hint/show-hint.js";
import "codemirror/addon/hint/anyword-hint.js";

import "codemirror/addon/lint/lint.css";
// 核心样式
import "codemirror/lib/codemirror.css";
import "codemirror/lib/codemirror.js";
// 引入主题后还需要在 options 中指定主题才会生效
// import "codemirror/theme/cobalt.css";
import "codemirror/theme/ambiance.css";
// import "codemirror/theme/Monokai.css";
import "codemirror/addon/hint/show-hint";
// import "codemirror/addon/hint/Python-hint";
import "codemirror/addon/selection/active-line";
import "codemirror/addon/edit/matchbrackets";
import "codemirror/addon/selection/active-line";
import "codemirror/addon/hint/show-hint.css";

import "codemirror/addon/lint/lint.js";

// 需要引入具体的语法高亮库才会有对应的语法高亮效果
// codemirror 官方其实支持通过 /addon/mode/loadmode.js 和 /mode/meta.js 来实现动态加载对应语法高亮库
// 但 vue 貌似没有无法在实例初始化后再动态加载对应 JS ，所以此处才把对应的 JS 提前引入
import "codemirror/mode/javascript/javascript.js";
import "codemirror/mode/css/css.js";
import "codemirror/mode/xml/xml.js";
import "codemirror/mode/clike/clike.js";
import "codemirror/mode/markdown/markdown.js";
import "codemirror/mode/python/python.js";
import "codemirror/mode/r/r.js";
import "codemirror/mode/shell/shell.js";
import "codemirror/mode/sql/sql.js";
import "codemirror/mode/swift/swift.js";
import "codemirror/mode/vue/vue.js";
// import "@/assets/js/checkCode.js";

// 尝试获取全局实例
const CodeMirror = window.CodeMirror || _CodeMirror;

export default {
  name: "in-coder",
  props: {
    // 外部传入的内容，用于实现双向绑定
    value: String,
    // 外部传入的语法类型
    language: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      checkUrl: this.URL + "/check_code",
      sendUrl: this.URL + "/run_code",
      returnData: "",
      drawer: false,
      direction: "btt",
      // 内部真实的内容
      code: `class Foo:
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

`,
      // 默认的语法类型
      mode: "Python",
      // 编辑器实例
      coder: null,
      // 默认配置
      options: {
        // 缩进格式
        tabSize: 4,
        //换行缩进
        indentUnit: 4,
        //1
        indentWithTabs: true,
        // 主题，对应主题库 JS 需要提前引入
        theme: "ambiance",
        // 显示行号
        lineNumbers: true,
        line: true,
        //括号匹配
        matchBrackets: true,
        // spellcheck:true,
        lineWrapping: true,
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        // gutters: ["CodeMirror-lint-markers"],
        // 智能提示
        extraKeys: { "Ctrl-Space": "autocomplete" },

        lintWith: {
          getAnnotations: CodeMirror.remoteValidator,
          async: true,
          check_cb: this.check_syntax
        }
      },
      // 支持切换的语法高亮类型，对应 JS 已经提前引入
      // 使用的是 MIME-TYPE ，不过作为前缀的 text/ 在后面指定时写死了
      modes: [
        {
          value: "x-python",
          label: "Python"
        }
        // {
        //   value: "css",
        //   label: "CSS"
        // },
        // {
        //   value: "javascript",
        //   label: "Javascript"
        // },
        // {
        //   value: "html",
        //   label: "XML/HTML"
        // },
        // {
        //   value: "x-java",
        //   label: "Java"
        // },
        // {
        //   value: "x-objectivec",
        //   label: "Objective-C"
        // },

        // {
        //   value: "x-rsrc",
        //   label: "R"
        // },
        // {
        //   value: "x-sh",
        //   label: "Shell"
        // },
        // {
        //   value: "x-sql",
        //   label: "SQL"
        // },
        // {
        //   value: "x-swift",
        //   label: "Swift"
        // },
        // {
        //   value: "x-vue",
        //   label: "Vue"
        // },
        // {
        //   value: "markdown",
        //   label: "Markdown"
        // }
      ]
    };
  },
  mounted() {
    // 初始化
    this._initialize();
    this.changeMode("x-python");
  },
  methods: {
    // 初始化
    _initialize() {
      // 初始化编辑器实例，传入需要被实例化的文本域对象和默认配置
      this.coder = CodeMirror.fromTextArea(this.$refs.textarea, this.options);
      // 编辑器赋值
      this.coder.setValue(this.value || this.code);

      // this.coder.extraKeys={Ctrl: 'autocomplete'};//自定义快捷键
      // this.coder.hintOptions= {//自定义提示选项
      //   tables: {
      //     users: ['name', 'score', 'birthDate']
      //   }
      // }
      // this.coder.on("cursorActivity", () =>{
      //   this.coder.showHint();
      // });
      // 支持双向绑定
      this.coder.on("change", coder => {
        this.code = coder.getValue();
        if (this.$emit) {
          this.$emit("input", this.code);
        }
      });

      // 尝试从父容器获取语法类型
      if (this.language) {
        // 获取具体的语法类型对象
        let modeObj = this._getLanguage(this.language);

        // 判断父容器传入的语法是否被支持
        if (modeObj) {
          this.mode = modeObj.label;
        }
      }
    },
    // 获取当前语法类型
    _getLanguage(language) {
      // 在支持的语法类型列表中寻找传入的语法类型
      return this.modes.find(mode => {
        // 所有的值都忽略大小写，方便比较
        let currentLanguage = language.toLowerCase();
        let currentLabel = mode.label.toLowerCase();
        let currentValue = mode.value.toLowerCase();

        // 由于真实值可能不规范，例如 java 的真实值是 x-java ，所以讲 value 和 label 同时和传入语法进行比较
        return (
          currentLabel === currentLanguage || currentValue === currentLanguage
        );
      });
    },
    // 更改模式
    changeMode(val) {
      // 修改编辑器的语法配置
      this.coder.setOption("mode", `text/${val}`);

      // 获取修改后的语法
      let label = this._getLanguage(val).label.toLowerCase();

      // 允许父容器通过以下函数监听当前的语法值
      this.$emit("language-change", label);
    },
    check_syntax(code, result_cb) {
      console.log(code);
      //Example error for guideline
      var error_list = [
        {
          line_no: null,
          column_no_start: null,
          column_no_stop: null,
          fragment: null,
          message: null,
          severity: null
        }
      ];

      //Push and replace errors
      function check(data) {
        //Clear array.
        error_list = [
          {
            line_no: null,
            column_no_start: null,
            column_no_stop: null,
            fragment: null,
            message: null,
            severity: null
          }
        ]; //Check if pylint output is empty.
        if (data == null) {
          result_cb(error_list);
        } else {
          var data_length = 0;
          if (data != null) {
            data_length = Object.keys(data).length;
          }
          for (var x = 0; x < data_length; x += 1) {
            if (data[x] == null) {
              continue;
            }
            number = data[x].line;
            code = data[x].code;
            codeinfo = data[x].error_info;
            severity = code[0];
            moreinfo = data[x].message;
            message = data[x].error;

            //Set severity to necessary parameters
            if (severity == "E" || severity == "e") {
              severity = "error";
              severity_color = "red";
            } else if (severity == "W" || severity == "w") {
              severity = "warning";
              severity_color = "yellow";
            }
            //Push to error list
            error_list.push({
              line_no: number,
              column_no_start: null,
              column_no_stop: null,
              fragment: null,
              message: message,
              severity: severity
            });
          }
          result_cb(error_list);
        }
      }

      //AJAX call to pylint
      // $.post(
      //   "/check_code",
      //   {
      //     text: code
      //   },
      //   function(data) {
      //     current_text = data;
      //     check(current_text);
      //     return false;
      //   },
      //   "json"
      // );

      this.$axios
        .post(this.url, this.$qs.stringify({ text: code }))
        .then(data => {
          current_text = data;
          check(current_text);
          return false;
        })
        .catch(err => {
          console.log(err);
        });
    },
    check_code(code) {
      let token = sessionStorage.getItem("token");
      this.$axios
        .post(this.checkUrl, this.$qs.stringify({ text: code }), {
          headers: {
            Authorization: "JWT " + token
          }
        })
        .then(res => {
          console.log(res);
        })
        .catch(err => {
          console.log(err);
        });
    },
    send(code) {
      console.log(code);
      let token = sessionStorage.getItem("token");
      this.$axios
        .post(this.sendUrl, this.$qs.stringify({ text: code }), {
          headers: {
            Authorization: "JWT " + token
          }
        })
        .then(res => {
          console.log(res);
          this.returnData = res.data.data;
          this.drawer = true;
        })
        .catch(err => {
          console.log(err);
        });
    },
    handleClose(done) {
      done();
    }
  }
};
</script>

<style lang="scss">
.el-drawer__open .el-drawer.btt {
  overflow: auto;
  height: 50% !important;
  background-color: #333;
  color:#fff;
  pre{
    font-family: "微软雅黑";
    line-height: 25px;
    padding: 0 10px;
  }
  .el-drawer__header{
    margin-bottom: 10px;
  }
}
.quotation {
  padding: 10px 20px;
}
.in-coder-panel {
  height: 500px;
  flex-grow: 1;
  display: flex;
  position: relative;
  margin-bottom: 10px;
  .CodeMirror-sizer {
    font-size: 16px;
    font-weight: bold;
  }
  .CodeMirror pre.CodeMirror-line,
  .CodeMirror pre.CodeMirror-line-like {
    line-height: 28px;
  }
  .cm-s-ambiance .CodeMirror-linenumber {
    line-height: 28px;
    color: #ccc;
  }
  .CodeMirror {
    width: 100%;
    height: 100%;
    flex-grow: 1;
    z-index: 1;
    .CodeMirror-code {
      line-height: 19px;
    }
  }

  .code-mode-select {
    position: absolute;
    z-index: 2;
    right: 10px;
    top: 10px;
    max-width: 130px;
  }
}
</style>
<style>
/* .el-drawer__open .el-drawer.btt {
  overflow: auto;
  height: 50% !important;
} */
</style>
