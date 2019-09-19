<template>
  <div class="quotation">
    <div class="in-coder-panel" ref="editor" :style="{height:editorHeight}">
      <textarea ref="textarea"></textarea>
    </div>
    <el-button type="success" size="medium" @click="run(code)">运行</el-button>
    <el-button type="primary" size="medium" @click="updateOrAdd(code)">更新或添加</el-button>
    <el-drawer
      title="控制台"
      :visible.sync="drawer"
      :direction="direction"
      :before-close="handleClose"
    >
      <span>
        <pre class="retrunMsg">{{returnData}}</pre>
      </span>
    </el-drawer>
  </div>
</template>

<script type="text/ecmascript-6">
// 引入全局实例
import _CodeMirror from 'codemirror'
// 尝试获取全局实例
const CodeMirror = window.CodeMirror || _CodeMirror
// 核心样式
import 'codemirror/lib/codemirror.css'
import 'codemirror/lib/codemirror.js'
//代码折叠
import 'codemirror/addon/fold/foldgutter.css'
import 'codemirror/addon/fold/foldcode.js'
import 'codemirror/addon/fold/foldgutter.js'
import 'codemirror/addon/fold/brace-fold.js'
import 'codemirror/addon/fold/comment-fold.js'
import 'codemirror/addon/fold/indent-fold.js'
//括号匹配
import 'codemirror/addon/edit/matchbrackets.js'
import 'codemirror/addon/edit/closebrackets.js'
//自动补全
import 'codemirror/addon/hint/show-hint.css'
import 'codemirror/addon/hint/show-hint.js'
import 'codemirror/addon/hint/anyword-hint.js'

import 'codemirror/addon/lint/lint.css'
import 'codemirror/addon/lint/lint.js'

// 引入主题后还需要在 options 中指定主题才会生效
// import "codemirror/theme/cobalt.css";
import 'codemirror/theme/ambiance.css'
// import "codemirror/theme/Monokai.css";
// import "codemirror/addon/hint/Python-hint";
import 'codemirror/addon/selection/active-line'

import 'codemirror/addon/comment/comment.js'
import 'codemirror/keymap/sublime.js'
// import "@/assets/js/pylint_js/javascript.js";
// import "@/assets/js/pylint_js/cm-validator-remote.js";
// 需要引入具体的语法高亮库才会有对应的语法高亮效果
// codemirror 官方其实支持通过 /addon/mode/loadmode.js 和 /mode/meta.js 来实现动态加载对应语法高亮库
// 但 vue 貌似没有无法在实例初始化后再动态加载对应 JS ，所以此处才把对应的 JS 提前引入
import 'codemirror/mode/javascript/javascript.js'
import 'codemirror/mode/css/css.js'
import 'codemirror/mode/xml/xml.js'
import 'codemirror/mode/clike/clike.js'
import 'codemirror/mode/markdown/markdown.js'
import 'codemirror/mode/python/python.js'
import 'codemirror/mode/r/r.js'
import 'codemirror/mode/shell/shell.js'
import 'codemirror/mode/sql/sql.js'
import 'codemirror/mode/swift/swift.js'
import 'codemirror/mode/vue/vue.js'

export default {
  name: 'in-coder',
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
      updateUrl: 'code',
      sendUrl: 'run_code',
      editorHeight: '',
      returnData: '',
      drawer: false,
      direction: 'btt',
      // 内部真实的内容
      code: `from datetime import datetime

from ctpbee import CtpbeeApi
from ctpbee.constant import LogData, AccountData, PositionData


class StrategyClass(CtpbeeApi):
    def __init__(self, name, app=None):
        super().__init__(name, app)

    def on_trade(self, trade):
        pass

    def on_realtime(self):
        pass

    def on_contract(self, contract):
        pass

    def on_order(self, order):
        pass

    def on_position(self, position: PositionData) -> None:
        pass

    def on_account(self, account: AccountData) -> None:
        """ """
        # print(self.converter.account_df)

    def on_init(self, init):
        pass

    def on_tick(self, tick):
        """tick process function"""

    def on_bar(self, bar):
        """bar process function"""

ext = StrategyClass('strategy_name')


`,
      // 默认的语法类型
      mode: 'Python',
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
        theme: 'ambiance',
        // 显示行号
        lineNumbers: true,
        line: true,
        //快捷键风格
        keyMap: 'sublime',
        // 智能缩进
        smartIndent: true,
        // 使用制表符进行智能缩进
        indentWithTabs: true,
        // spellcheck:true,
        lineWrapping: true,
        // 启用行槽中的代码折叠
        foldGutter: true,
        // 自动聚焦
        autofocus: true,
        // 匹配结束符号，比如"]、}"
        matchBrackets: true,
        // 自动闭合符号
        autoCloseBrackets: true,
        // 显示选中行的样式
        styleActiveLine: true,
        //语法检测开启
        lint: true,
        // 在行槽中添加行号显示器、折叠器、语法检测器
        gutters: [
          'CodeMirror-linenumbers',
          'CodeMirror-foldgutter',
          'CodeMirror-lint-markers'
        ],
        // 智能提示
        extraKeys: { Ctrl: 'autocomplete' }
      },
      // 支持切换的语法高亮类型，对应 JS 已经提前引入
      // 使用的是 MIME-TYPE ，不过作为前缀的 text/ 在后面指定时写死了
      modes: [
        {
          value: 'x-python',
          label: 'Python'
        }
      ]
    }
  },
  mounted() {
    // 初始化
    this._initialize()
    this.changeMode('x-python')
    this.strategyName = this.$route.query.name
    this.getCode(this.strategyName)
    this.setEditorHeight()
  },
  methods: {
    // 初始化
    _initialize() {
      // 初始化编辑器实例，传入需要被实例化的文本域对象和默认配置
      this.coder = CodeMirror.fromTextArea(this.$refs.textarea, this.options)
      // 编辑器赋值
      this.coder.setValue(this.value || this.code)
      // 支持双向绑定
      this.coder.on('change', coder => {
        this.code = coder.getValue()
        if (this.$emit) {
          this.$emit('input', this.code)
        }
      })

      // 尝试从父容器获取语法类型
      if (this.language) {
        // 获取具体的语法类型对象
        let modeObj = this._getLanguage(this.language)

        // 判断父容器传入的语法是否被支持
        if (modeObj) {
          this.mode = modeObj.label
        }
      }
    },
    // 获取当前语法类型
    _getLanguage(language) {
      // 在支持的语法类型列表中寻找传入的语法类型
      return this.modes.find(mode => {
        // 所有的值都忽略大小写，方便比较
        let currentLanguage = language.toLowerCase()
        let currentLabel = mode.label.toLowerCase()
        let currentValue = mode.value.toLowerCase()

        // 由于真实值可能不规范，例如 java 的真实值是 x-java ，所以讲 value 和 label 同时和传入语法进行比较
        return (
          currentLabel === currentLanguage || currentValue === currentLanguage
        )
      })
    },
    // 更改模式
    changeMode(val) {
      // 修改编辑器的语法配置
      this.coder.setOption('mode', `text/${val}`)

      // 获取修改后的语法
      let label = this._getLanguage(val).label.toLowerCase()

      // 允许父容器通过以下函数监听当前的语法值
      this.$emit('language-change', label)
    },
    updateOrAdd(code) {
      this.$axios
        .post(this.updateUrl, this.$qs.stringify({ text: code }))
        .then(res => {
          let returnData = res.data
          this.tip(returnData.success, returnData.msg, this)
        })
        .catch(err => {
          console.log(err)
        })
    },
    run(code) {
      this.$axios
        .post(this.sendUrl, this.$qs.stringify({ text: code }))
        .then(res => {
          this.returnData = res.data.data
          this.drawer = true
        })
        .catch(err => {
          console.log(err)
        })
    },
    getCode(name) {
      this.$axios
        .get(this.updateUrl, {
          params: {
            name: name
          }
        })
        .then(res => {
          let returnData = res.data
          if (returnData.msg === 'name is none') {
            return
          } else {
            this.code = returnData.data[name]
            this.coder.setValue(this.code)
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    handleClose(done) {
      done()
    },
    setEditorHeight() {
      let h = window.innerHeight
      this.editorHeight = h - 120 + 'px'
    }
  }
}
</script>

<style lang="scss">
.in-coder-panel .CodeMirror pre.CodeMirror-line {
  font-family: '微软雅黑';
}
.el-drawer__open .el-drawer.btt {
  overflow: auto;
  height: 50% !important;
  background-color: #333;
  color: #fff;
  pre {
    font-family: '微软雅黑';
    line-height: 25px;
    padding: 0 10px;
  }
  .el-drawer__header {
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
    font-weight: 500;
  }
  .CodeMirror pre.CodeMirror-line,
  .CodeMirror pre.CodeMirror-line-like {
    line-height: 28px;
  }
  .cm-s-ambiance .CodeMirror-linenumber {
    line-height: 28px;
    color: #ccc;
    font-weight: bold;
    font-family: '微软雅黑';
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
  .cm-s-ambiance .CodeMirror-guttermarker-subtle {
    color: #ccc;
    margin-top: 6px;
    font-size: 18px;
  }
}
</style>
<style>
/* .el-drawer__open .el-drawer.btt {
  overflow: auto;
  height: 50% !important;
} */
</style>
