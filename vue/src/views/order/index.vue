<template>
  <div class="order" v-show="orderFlag">
    <transition enter-active-class="zoomIn" leave-active-class="zoomOut">
      <div class="journal animated faster" v-show="journal" v-drag ref="journal" id="journal">
        <p>
          <span>日志信息</span>
          <i class="el-icon-circle-close closeicon" @click="journal = false"></i>
        </p>
        <el-table :data="logData" stripe id="logTab">
          <el-table-column prop="created" label="时间" min-width="160px">
            <template scope="scope">
              <span style="color:red">{{ scope.row.created }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="levelname" label="等级" min-width="80px">
            <template scope="scope">
              <span style="color:#EF6FE9">{{ scope.row.levelname }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="owner" label="APP" min-width="100px">
            <template scope="scope">
              <span style="color:#000000">{{scope.row.owner}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="接口" min-width="100px">
            <template scope="scope">
              <span style="color:#30CCCC">{{scope.row.name}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="msg" label="信息" min-width="100px">
            <template scope="scope">
              <span v-if="scope.row.levelname==='INFO'" style="color:#67C23A">{{scope.row.msg}}</span>
              <span v-if="scope.row.levelname==='ERROR'" style="color:red">{{scope.row.msg}}</span>
              <span v-if="scope.row.levelname==='DEBUG'" style="color:#EF6FE9">{{scope.row.msg}}</span>
              <span v-if="scope.row.levelname==='WARNING'" style="color:#89C800">{{scope.row.msg}}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </transition>

    <el-button
      type="warning"
      icon="el-icon-star-off"
      circle
      class="journalIcon"
      @click="journal = !journal"
    ></el-button>

    <el-row :gutter="10">
      <el-col :span="18" :xs="24">
        <el-card class="box-card" id="kline">
          <div ref="klineBox" style="overflow:auto" id="klineBox">
            <Vue-Kline ref="kline" :klineParams="klineParams" :klineData="klineData"></Vue-Kline>
          </div>
        </el-card>
        <br />
        <el-card class="box-card">
          <el-tabs tab-position="top">
            <el-tab-pane label="持仓数据">
              <el-table :data="positionData" border style="width: 100%">
                <el-table-column prop="local_symbol" label="local_symbol" v-if="false"></el-table-column>
                <el-table-column prop="symbol" label="持仓合约"></el-table-column>
                <el-table-column prop="direction" label="持仓方向"></el-table-column>
                <el-table-column prop="exchange" label="交易所"></el-table-column>
                <el-table-column prop="volume" label="持仓手数"></el-table-column>
                <el-table-column prop="position_profit" label="浮动盈亏"></el-table-column>
                <el-table-column prop="price" label="持仓均价"></el-table-column>
                <el-table-column prop="yd_volume" label="昨日持仓手数"></el-table-column>
                <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button type="primary" size="medium" @click="positionClose(scope.row)">平仓</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="待成交数据">
              <el-table :data="activeOrderData" border style="width: 100%">
                <el-table-column prop="order_id" label="id" v-if="false"></el-table-column>
                <el-table-column prop="local_symbol" label="local_symbol" v-if="false"></el-table-column>
                <el-table-column prop="symbol" label="报单合约"></el-table-column>
                <el-table-column prop="direction" label="报单方向"></el-table-column>
                <el-table-column prop="exchange" label="交易所"></el-table-column>
                <el-table-column prop="volume" label="报单手数"></el-table-column>
                <el-table-column prop="price" label="报单价格"></el-table-column>
                <el-table-column prop="status" label="状态"></el-table-column>
                <el-table-column prop="time" label="报单时间"></el-table-column>
                <el-table-column prop="type" label="价格类型"></el-table-column>
                <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button type="primary" size="medium" @click="cancelOrder(scope.row)">撤单</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="发单数据">
              <el-table :data="orderData" border style="width: 100%">
                <el-table-column prop="symbol" label="报单合约"></el-table-column>
                <el-table-column prop="direction" label="报单方向"></el-table-column>
                <el-table-column prop="exchange" label="交易所"></el-table-column>
                <el-table-column prop="volume" label="报单手数"></el-table-column>
                <el-table-column prop="price" label="报单价格"></el-table-column>
                <el-table-column prop="status" label="状态"></el-table-column>
                <el-table-column prop="time" label="报单时间"></el-table-column>
                <el-table-column prop="type" label="价格类型"></el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="成交数据">
              <el-table :data="tradeData" border style="width: 100%">
                <el-table-column prop="symbol" label="成交合约"></el-table-column>
                <el-table-column prop="direction" label="成交方向"></el-table-column>
                <el-table-column prop="exchange" label="交易所"></el-table-column>
                <el-table-column prop="volume" label="报单手数"></el-table-column>
                <el-table-column prop="price" label="报单价格"></el-table-column>
                <el-table-column prop="offset" label="开平"></el-table-column>
                <el-table-column prop="time" label="成交时间"></el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
      <el-col :span="6" :xs="24">
        <el-card class="box-card" style="height:340px">
          <table class="tickTab">
            <tr v-for="(val,key,index) in tickTabData" :key="index">
              <td>{{key|chinese}}</td>
              <td>{{val}}</td>
            </tr>
          </table>
        </el-card>
        <br />
        <el-card class="box-card">
          <el-form label-position="right" label-width="40px" :model="orderForm">
            <el-form-item label="合约">
              <el-input v-model="orderForm.local_symbol" readonly></el-input>
            </el-form-item>
            <el-form-item label="类型">
              <el-select v-model="type" clearable placeholder="请选择">
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="价格">
              <el-input type="number" v-model.number="orderForm.price" placeholder="请输入价格"></el-input>
            </el-form-item>
            <el-form-item label="手数">
              <el-input-number v-model="orderForm.volume" :min="1" placeholder="请输入手数"></el-input-number>
            </el-form-item>
            <el-form-item label>
              <el-button type="success" @click="business(orderForm,'buy')">买多</el-button>
              <el-button type="primary" @click="business(orderForm,'sell')">卖空</el-button>
            </el-form-item>
          </el-form>
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
      orderUrl: 'order_solve',
      klineUrl: 'bar',
      positionUrl: 'close_position',
      journal: false,
      orderFlag: false,
      klineBoxWidth: '',
      orderForm: {
        local_symbol: '',
        price: '',
        volume: 1
      },
      options: [
        {
          value: 'limit',
          label: '限价'
        },
        {
          value: 'market',
          label: '市价'
        }
      ],
      type: 'limit',
      tickTabData: {},
      positionData: [],
      activeOrderData: [],
      orderData: [],
      tradeData: [],
      logData: [],
      tick_map: {
        ask_price_1: '买一价',
        ask_volume_1: '买一量',
        bid_price_1: '卖一价',
        bid_volume_1: '卖一量',
        last_price: '最新价格',
        local_symbol: '本地id',
        exchange: '交易所',
        open_interest: '持仓量',
        pre_close: '昨日收盘价',
        volume: '成交量',
        datetime: '时间'
      },
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
      }
    }
  },
  components: {
    VueKline
  },
  sockets: {
    //监听socket连接
    connect: function() {
      console.log('下单已连接')
    },
    //推送当前所选合约的行情数据
    tick: function(res) {
      // console.log(res)
      let data = res.data
      if (res.data.local_symbol !== this.orderForm.local_symbol) {
        return
      }
      for (var i in this.tick_map) {
        if (i == 'datetime') {
          this.tickTabData[i] = data[i].split('.')[0]
        } else {
          this.tickTabData[i] = data[i]
        }
      }
    },
    //推送持仓数据
    position: function(res) {
      this.positionData = res.data
    },
    //推送待成交数据
    active_order: function(res) {
      this.activeOrderData = res.data
    },
    //推送成交数据
    trade: function(res) {
      this.tradeData = res.data
    },
    //推送发单数据
    order: function(res) {
      this.orderData = res.data
    },
    //socket推送k线数据
    bar: function(res) {
      if (res.local_symbol === this.orderForm.local_symbol) {
        this.klineData.data.lines.push(res.data)
      }
    },
    //推送日志数据
    log: function(res) {
      if (this.logData.length >= 50) {
        this.logData = this.logData.slice(0, 49)
      }
      this.logData.unshift(res)
    }
  },
  filters: {
    chinese: val => {
      let tick_map = {
        ask_price_1: '买一价',
        ask_volume_1: '买一量',
        bid_price_1: '卖一价',
        bid_volume_1: '卖一量',
        last_price: '最新价格',
        local_symbol: '本地id',
        exchange: '交易所',
        open_interest: '持仓量',
        pre_close: '昨日收盘价',
        volume: '成交量',
        datetime: '时间'
      }
      return tick_map[val]
    }
  },
  methods: {
    //获取持仓，待成交，发单，成交数据
    getTabData() {
      this.$axios
        .get(this.orderUrl)
        .then(res => {
          let returnData = res.data
          if (returnData.success == true) {
            this.orderData = returnData.data.order_list
            this.positionData = returnData.data.position_list
            this.activeOrderData = returnData.data.active_order_list
            this.tradeData = returnData.data.trade_list
            let log = returnData.data.log_history
            this.logData =
              log.length >= 50
                ? log.slice(log.length - 50).reverse()
                : log.reverse()
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    //交易（买多。卖空）
    business(data, transactionType) {
      if (data.price === '') {
        return this.$message({
          showClose: true,
          message: '价格不能为空!',
          type: 'error'
        })
      }
      data['exchange'] = data.local_symbol.split('.')[1]
      data['offset'] = 'open'
      data['type'] = this.type
      data['direction'] = transactionType === 'buy' ? 'long' : 'short'
      this.$axios
        .post(this.orderUrl, this.$qs.stringify(data))
        .then(res => {
          let returnData = res.data
          this.tips({
            type: returnData.success,
            msg: returnData.msg,
            isTips: true
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
    //撤单
    cancelOrder(val) {
      console.log(val)

      this.$axios
        .delete(this.orderUrl, {
          params: {
            local_symbol: val.local_symbol,
            exchange: val.exchange,
            order_id: val.order_id
          }
        })
        .then(res => {
          let returnData = res.data
          this.tips({
            type: returnData.success,
            msg: returnData.msg,
            isTips: true
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
    //平仓
    positionClose(val) {
      // exchange local_symbol symbol volume
      let sendData = {
        exchange: val.exchange,
        local_symbol: val.local_symbol,
        symbol: val.symbol,
        volume: val.volume,
        direction: val.direction
      }
      this.$axios
        .post(this.positionUrl, this.$qs.stringify(sendData))
        .then(res => {
          let returnData = res.data
          console.log(returnData)
          this.tips({
            type: returnData.success,
            msg: returnData.msg,
            isTips: true
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
    //获取K线数据
    async getKlineData() {
      let { data: returnData } = await this.$axios.post(
        this.klineUrl,
        this.$qs.stringify({ local_symbol: this.orderForm.local_symbol })
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
      this.$refs.kline.setSymbol(
        this.orderForm.local_symbol,
        this.orderForm.local_symbol
      )
      //设置主题
      this.$refs.kline.setTheme('light')
    },
    //初始化日志
    initJournal() {
      //因日志盒子是隐藏的，无法获取其宽，故暂时先写个固定值
      let bw = 580
      let cw = document.body.clientWidth
      this.$refs.journal.style.left = (cw - bw) / 2 + 'px'
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
      elementResizeDetectorMaker().listenTo(
        document.getElementById('journal'),
        function(element) {
          var height = element.offsetHeight
          document.getElementById('logTab').style.height = height - 55 + 'px'
        }
      )
    }
  },
  mounted() {
    this.orderForm.local_symbol = sessionStorage.getItem('symbolName')
    if (!this.orderForm.local_symbol) {
      return this.$alert('请先订阅行情！', '友情提示', {
        confirmButtonText: '确定',
        callback: action => {
          this.$router.push({
            path: '/quotation/index'
          })
        }
      })
    }
    this.orderFlag = true
    this.getTabData()
    //请求k线数据
    this.getKlineData()
    // this.initKline()
    this.watchWidth()
    this.initJournal()
  }
}
</script>
<style lang="scss">
.order {
  padding: 20px;
  .el-select {
    width: 100%;
  }
  input[type='number']::-webkit-outer-spin-button,
  input[type='number']::-webkit-inner-spin-button {
    -webkit-appearance: none !important;
    margin: 0;
  }
  input[type='number'] {
    -moz-appearance: textfield;
  }
  .tickTab {
    width: 100%;
    border-collapse: collapse;
    tr td:nth-child(1) {
      color: #909399;
      font-weight: 500;
    }
    td {
      border: 1px solid #eee;
      line-height: 24px;
      padding-left: 10px;
      color: #606266;
      font-size: 12px;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }
  #kline {
    .el-card__body {
      padding: 0px;
    }
    .chart_container {
      border: 1px solid #eee;
    }
    #sizeIcon {
      display: none;
    }
  }
  .journal {
    width: 580px;
    // min-width: 500px;
    height: 400px;
    box-sizing: border-box;
    background-color: #eee;
    border: 1px solid #ccc;
    position: fixed;
    top: 10px;
    border-radius: 10px;
    z-index: 1001;
    padding: 10px;
    overflow: hidden;
    p {
      margin: 5px 0 10px;
    }
    span {
      margin-left: 10px;
    }
    .closeicon {
      float: right;
      margin-right: 10px;
      font-size: 20px;
      cursor: pointer;
    }
    .el-table {
      // width: 100%;
      overflow: auto;
      /* 滚动条 */
      &::-webkit-scrollbar-thumb:horizontal {
        /*水平滚动条的样式*/
        width: 4px;
        background-color: #ccc;
        border-radius: 10px;
      }
      &::-webkit-scrollbar-track-piece {
        background-color: #fff; /*滚动条的背景颜色*/
        border-radius: 0; /*滚动条的圆角宽度*/
      }
      &::-webkit-scrollbar {
        width: 10px; /*滚动条的宽度*/
        height: 8px; /*滚动条的高度*/
      }
      &::-webkit-scrollbar-thumb:vertical {
        /*垂直滚动条的样式*/
        height: 50px;
        background-color: #ccc;
        border-radius: 10px;
        outline: 2px solid #fff;
        outline-offset: -2px;
        border: 2px solid #fff;
      }
      &::-webkit-scrollbar-thumb:hover {
        /*滚动条的hover样式*/
        height: 50px;
        background-color: #9f9f9f;
        border-radius: 10px;
      }
      span {
        margin: 0;
      }
    }
  }
  .journalIcon {
    position: fixed;
    top: 60px;
    right: 5px;
    z-index: 1002;
  }
}
</style>
