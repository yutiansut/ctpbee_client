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
    connect: function(){
      console.log('connect......')
    },
    account: function(res){
      console.log(res)
      let returnData=res.data
      if(returnData.success===false){
        this.$message({
          showClose: true,
          message: returnData.msg,
          type: 'error'
        });
      }else{
        this.tableData=returnData
      }
    }
  }

};
</script>

<style lang="scss" scoped>
.account{
  padding:20px;
  h4{
    color: #666;
    font-weight: normal;
  }
}
</style>
