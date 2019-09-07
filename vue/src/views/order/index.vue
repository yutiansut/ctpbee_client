<template>
  <div class="order">
    <el-row :gutter="20">
      <el-col :span="16" :xs="24">
        <el-card class="box-card">
          <el-tabs tab-position="top">
            <el-tab-pane label="持仓数据">
              <el-table :data="positionData" border style="width: 100%">
                <el-table-column prop="symbol" label="持仓合约"></el-table-column>
                <el-table-column prop="direction" label="持仓方向"></el-table-column>
                <el-table-column prop="exchange" label="交易所"></el-table-column>
                <el-table-column prop="volume" label="持仓手数"></el-table-column>
                <el-table-column prop="position_profit" label="浮动盈亏"></el-table-column>
                <el-table-column prop="price" label="持仓均价"></el-table-column>
                <el-table-column prop="yd_volume" label="昨日持仓手数"></el-table-column>
                <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button type="primary" size="medium" @click="order(scope.row.symbol)">平仓</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="待成交数据">
              <el-table :data="activeOrderData" border style="width: 100%">
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
                    <el-button type="primary" size="medium" @click="order(scope.row.symbol)">平仓</el-button>
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
      <el-col :span="8" :xs="24">
        <el-card class="box-card">
          <el-form label-position="right" label-width="50px" :model="orderForm">
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
              <el-input
                v-model.number="orderForm.price"
                placeholder="请输入价格"
                oninput = "value=value.replace(/[^\d|\.]+/g,'')"
              ></el-input>
            </el-form-item>
            <el-form-item label="手数">
              <el-input-number v-model="volume" :min="1" placeholder="请输入手数"></el-input-number>
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
export default {
  data() {
    return {
      orderUrl: this.URL + "/order_solve",
      token: "",
      orderForm: {
        local_symbol: "",
        price: ""
      },
      volume: 1,
      options: [
        {
          value: "limit",
          label: "限价"
        },
        {
          value: "market",
          label: "市价"
        }
      ],
      type: "limit",
      positionData: [],
      activeOrderData: [],
      orderData: [],
      tradeData: []
    };
  },
  watch: {
    volume(newVolume, oldVolume) {
      if (newVolume < 1) {
        this.orderForm.volume = 1;
      }
    }
  },
  methods: {
    handleClick() {
      console.log(666)
      this.orderForm.price = this.orderForm.price.replace(/[^\w]/g, "");
    },
    getTabData() {
      this.$axios
        .get(this.orderUrl, {
          headers: {
            Authorization: "JWT " + this.token
          }
        })
        .then(res => {
          let returnData = res.data;
          if (returnData.success == true) {
            this.orderData = returnData.data.order_list;
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    orderTip() {
      let symbolName = sessionStorage.getItem("symbolName");
      if (!symbolName) {
        this.$alert("请先订阅行情！", "友情提示", {
          confirmButtonText: "确定",
          callback: action => {
            this.$router.push({
              path: "/quotation/index"
            });
          }
        });
      }
    },
    business(data, transactionType) {
      if (data.price === "") {
        return this.$message({
          showClose: true,
          message: "价格不能为空!",
          type: "error"
        });
      }
      data["exchange"] = data.local_symbol.split(".")[1];
      data["offset"] = "open";
      data["type"] = this.type;
      data["direction"] = transactionType === "buy" ? "long" : "short";
      this.$axios
        .post(this.orderUrl, this.$qs.stringify(data), {
          headers: {
            Authorization: "JWT " + this.token
          }
        })
        .then(res => {
          let returnData = res.data;
          this.tip(returnData.success, returnData.msg, this);
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.orderTip();
    if (this.$route.query.symbol) {
      this.orderForm.local_symbol = this.$route.query.symbol;
    } else {
      this.orderForm.local_symbol = sessionStorage.getItem("symbolName");
    }

    this.token = sessionStorage.getItem("token");
    this.getTabData();
  }
};
</script>
<style lang="scss">
.order {
  padding: 20px;
  .el-select {
    width: 100%;
  }
}
</style>
