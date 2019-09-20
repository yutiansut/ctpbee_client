<template>
  <div class="test">
    <el-row :gutter="10">
      <el-col :span="12">
        <el-card class="box-card kline_card">
          <div ref="klineBox" id="klineBox">
            <Vue-Kline ref="kline" :klineParams="klineParams" :klineData="klineData"></Vue-Kline>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="box-card formBox">
          <div class="backTestParameter">
            <p>回测参数</p>
            <el-form label-position="right">
              <el-form-item>
                <el-date-picker v-model="startTime" type="date" placeholder="开始时间" style="width:100%"></el-date-picker>
              </el-form-item>
              <el-form-item>
                <el-date-picker v-model="endTime" type="date" placeholder="结束时间" style="width:100%"></el-date-picker>
              </el-form-item>
              <el-form-item>
                <el-input></el-input>
              </el-form-item>
              <el-form-item>
                <el-input></el-input>
              </el-form-item>
              <el-button type="primary" style="backgroundColor:#c56cf0;border:1px solid #c56cf0;">确认</el-button>
            </el-form>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="box-card formBox">
          <div class="backTestParameter">
            <p>策略参数</p>
            <el-form label-position="right">
              <el-form-item>
                <el-input></el-input>
              </el-form-item>
              <el-form-item>
                <el-input></el-input>
              </el-form-item>
              <el-form-item>
                <el-input></el-input>
              </el-form-item>
              <el-button type="info" style="backgroundColor:#55efc4;border:1px solid #55efc4;">确认</el-button>
            </el-form>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="box-card">
          <table class="status">
            <tr v-for="(value,key,index) in status" :key="index">
              <td>{{key}}</td>
              <td>{{value}}</td>
            </tr>
          </table>
        </el-card>
        <br />
        <el-card class="box-card">
          <div class="btn">
            <el-select v-model="symbolValue" filterable placeholder="请选择合约" style="width:100%">
              <el-option v-for="(item , index) in symbolOptions" :key="index" :value="item"></el-option>
            </el-select>
            <br />
            <br />
            <el-button type="warning">载入数据</el-button>
          </div>
        </el-card>
        <br />
        <el-card class="box-card">
          <div class="btn">
            <el-select v-model="retreatValue" filterable placeholder="请选择策略 " style="width:100%">
              <el-option
                v-for="item in retreatOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
            <br />
            <br />
            <el-button type="info" style="backgroundColor:#ff7675">载入策略</el-button>
          </div>
        </el-card>
        <br />
        <el-card class="box-card">
          <div class="btn">
            <el-button type="primary">启动</el-button>
            <br />
            <br />
            <el-button type="warning" style="backgroundColor:#d63031;border:1px solid #d63031;">停止</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <br />
    <el-row :gutter="10">
      <el-col :span="12">
        <el-card class="box-card">
          <div class="orderMsg">
            <p>下单信息</p>
            <el-table :data="orderData" border style="width: 100%">
              <el-table-column prop="date" label="日期" width="180"></el-table-column>
              <el-table-column prop="name" label="姓名" width="180"></el-table-column>
              <el-table-column prop="address" label="地址"></el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card">
          <div class="retreatResult">
            <p>回测结果</p>
            <el-table :data="testData" border style="width: 100%">
              <el-table-column prop="date" label="日期" width="180"></el-table-column>
              <el-table-column prop="name" label="姓名" width="180"></el-table-column>
              <el-table-column prop="address" label="地址"></el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import VueKline from 'vue-kline'
import elementResizeDetectorMaker from 'element-resize-detector'
export default {
  data() {
    return {
      klineUrl: 'bar',
      quotationUrl: 'market',
      //k线配置
      klineParams: {
        width: 800,
        height: 550,
        theme: 'light',
        language: 'zh-cn',
        ranges: ['1w', '1d', '1h', '30m', '15m', '5m', '1m', 'line'],
        symbol: 'BTC',
        symbolName: 'BTC/USD',
        intervalTime: 1000,
        depthWidth: 50
      },
      //k线数据
      klineData: {
        success: true,
        data: {
          lines: []
        }
      },
      orderData: [
        {
          date: '2016-05-02',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        },
        {
          date: '2016-05-04',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1517 弄'
        },
        {
          date: '2016-05-01',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1519 弄'
        },
        {
          date: '2016-05-03',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1516 弄'
        }
      ],
      testData:[
        {
          date: '2016-05-02',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        },
        {
          date: '2016-05-04',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1517 弄'
        },
        {
          date: '2016-05-01',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1519 弄'
        },
        {
          date: '2016-05-03',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1516 弄'
        }
      ],
      status: {
        数据状态: '就绪',
        回测状态: '就绪'
      },
      symbolOptions: [],
      symbolValue: '',
      retreatOptions: [
        {
          value: '选项1',
          label: '黄金糕'
        },
        {
          value: '选项2',
          label: '双皮奶'
        },
        {
          value: '选项3',
          label: '蚵仔煎'
        },
        {
          value: '选项4',
          label: '龙须面'
        },
        {
          value: '选项5',
          label: '北京烤鸭'
        }
      ],
      retreatValue:'',
      //开始时间
      startTime:'',
      //结束时间
      endTime:''
    }
  },
  components: {
    VueKline
  },
  sockets: {
    //监听socket连接
    connect: function() {
      console.log('回测已连接')
    },
    contract: function(res) {
      // console.log(res)
      this.symbolOptions = res
    },
    //socket推送k线数据
    bar: function(res) {
      // if (res.local_symbol === this.orderForm.local_symbol) {
      //   this.klineData.data.lines.push(res.data)
      // }
    }
  },
  methods: {
    //获取K线数据
    async getKlineData() {
      let { data: returnData } = await this.$axios.post(
        this.klineUrl,
        this.$qs.stringify({ local_symbol: sessionStorage.getItem('symbolName')})
      )
      this.tips({
        type: returnData.success,
        msg: returnData.msg,
        isTips: false,
        success: () => {
          this.klineData.data.lines = returnData.data
          //初始化k线
          this.initKline()
        }
      })
    },
    //初始化K线
    initKline() {
      this.klineBoxWidth = this.$refs.klineBox.offsetWidth
      //更新数据
      this.$refs.kline.kline.data.lines = this.klineData.data.lines
      //设置k线容器宽度
      this.$refs.kline.resize(this.klineBoxWidth, 550)
      //设置k线symbol
      // this.$refs.kline.setSymbol(
      //   this.orderForm.local_symbol,
      //   this.orderForm.local_symbol
      // )
      //设置主题
      this.$refs.kline.setTheme('light')
    },
    //监听K线盒子大小，以达到自适应的效果
    watchWidth() {
      var that = this
      elementResizeDetectorMaker().listenTo(
        document.getElementById('klineBox'),
        function(element) {
          var width = element.offsetWidth
          try {
            that.$refs.kline.resize(width, 550)
          } catch (err) {
            // console.log(err)
          }
        }
      )
    },
    getSymbol() {
      this.$axios
        .put(this.quotationUrl, this.$qs.stringify({ name: 'test' }))
        .then(res => {
          let returnData = res.data
          this.tips({
            type: returnData.success,
            msg: returnData.msg,
            isTips: false
          })
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  mounted() {
    this.getSymbol()
    //请求k线数据
    this.getKlineData()

    this.watchWidth()
  }
}
</script>
<style lang='scss'>
.test {
  padding: 20px;
  #sizeIcon{
    display: none;
  }
  .kline_card {
    .el-card__body {
      padding: 0 !important;
      .chart_container {
        border: 1px solid #ccc;
      }
    }
  }
  .formBox {
    height: 550px;
  }
  .el-card__body {
    padding: 10px;
    .backTestParameter {
      p {
        color: #666;
        text-align: center;
      }
      button {
        width: 100%;
      }
    }
    .btn {
      padding: 5px;
      button {
        width: 100%;
      }
    }
    .retreatResult {
      p {
        color: #666;
        text-align: center;
      }
    }
    .orderMsg {
      p {
        color: #666;
        text-align: center;
      }
    }
    .status {
      width: 100%;
      border-collapse: collapse;
      td {
        width: 50%;
        border: 1px solid #ccc;
        line-height: 24px;
        padding-left: 10px;
        color: #606266;
        font-size: 12px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }
    }
  }
}
</style>
