<template>
  <div class="account">
    <h4>基本账户信息</h4>
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="key" label="key"></el-table-column>
      <el-table-column prop="value" label="Value"></el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: []
    };
  },
  sockets:{
    // 通信的name
    //这里是监听connect事件
    connect: function(){
      console.log('connect......')
    },
    account: function(res){
      console.log(res)
      let returnData=res.data
      this.tableData=returnData
    }
  }

};
</script>

<style lang="scss" scoped>
.account{
  padding:20px;
  h4{
    color: #666;
  }
}
</style>
