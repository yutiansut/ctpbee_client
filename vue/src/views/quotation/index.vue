<template>
  <div class="quotation">
    <el-select v-model="value" filterable placeholder="请选择">
      <el-option v-for="(item , index) in options" :key="index" :value="item"></el-option>
    </el-select>
    <el-button type="success" @click="subscribe(value)" style="margin-left:20px;">订阅单个</el-button>
    <!-- <el-button type="primary" @click="handleEdit('ag1910')">订阅全部</el-button> -->
    <el-button type="primary" @click="getSymbol()">更新合约</el-button>
    <!-- <el-button type="primary" @click="handleEdit('ag1910')">下單</el-button> -->
    <h4>订阅列表</h4>
    <el-table :data="symbolArr" border style="width: 100%">
      <el-table-column prop="name" label="中文名"></el-table-column>
      <el-table-column prop="symbol" label="品种"></el-table-column>
      <el-table-column prop="last_price" label="行情"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button type="primary" @click="order(scope.row.symbol)">
            前往下单
            <i class="el-icon-upload el-icon--right"></i>
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      quotationUrl: this.URL + "/market",
      tableData: [],
      options: ["ag1901", "ad5244", "fdf5545"],
      value: "",
      symbol:"",
      symbolObj:{},
      symbolArr:[]
    };
  },
  sockets: {
    // 通信的name
    //这里是监听connect事件
    connect: function() {
      console.log("connect......");
    },
    contract: function(res) {
      // console.log(res)
      this.options=res
    },
    tick:function(res){
      this.symbolObj[res.data.symbol]=res.data
      // console.log(this.symbolObj)
      this.symbolArr=[]
      for(let i in this.symbolObj){
        this.symbolArr.push(this.symbolObj[i])
      }
    }
  },
  methods: {
    subscribe(symbol) {
      if(!symbol){
        this.tip("error","请先选择",this)
        return
      }
      let token = sessionStorage.getItem("token");
      this.$axios
        .post(this.quotationUrl, this.$qs.stringify({ symbol: symbol }), {
          headers: {
            Authorization: "JWT " + token
          }
        })
        .then(res => {
          let returnData=res.data
          if(returnData.success===true){
            this.tip("success",returnData.msg,this)
          }else{
            this.tip("error",returnData.msg,this)
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    order(symbol){
      console.log(symbol)
    },
    getSymbol() {
      let token = sessionStorage.getItem("token");
      this.$axios
        .put(this.quotationUrl, this.$qs.stringify({name:'test'}),{
          headers: {
            Authorization: "JWT " + token
          }
        })
        .then(res => {
          let returnData=res.data
          if(returnData.success===true){
            this.tip("success",returnData.msg,this)
          }else{
            this.tip("error",returnData.msg,this)
          }
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.getSymbol();
  }
};
</script>

<style lang='scss' scoped>
.quotation {
  padding: 20px;
  h4 {
    color: #666;
  }
}
</style>
