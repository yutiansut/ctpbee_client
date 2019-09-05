<template>
  <div class="strategy">
    <el-button type="primary" @click="goEditor()">添加策略</el-button>
    <el-table :data="tableData" border style="width: 100%;margin-top:10px;">
      <el-table-column prop="name" label="策略名称"></el-table-column>
      <el-table-column prop="status" label="状态"></el-table-column>
      <el-table-column prop="operation" label="操作">
        <template slot-scope="scope">
          <el-button size="mini" type="info" @click="edit(scope.row.name)" :disabled="scope.row.name==='default_settings'">编辑</el-button>
          <el-button size="mini" type="success" v-if="scope.row.status!=='运行中'" @click="deal(scope.row.name,'开启')" :disabled="scope.row.name==='default_settings'">开启</el-button>
          <el-button size="mini" type="warning" v-else @click="deal(scope.row.name,'关闭')" :disabled="scope.row.name==='default_settings'">关闭</el-button>
          <el-button size="mini" type="danger" @click="deleteStrategy(scope.row.name)" :disabled="scope.row.name==='default_settings'">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
export default {
  inject:['reload'],
  data() {
    return {
      updateUrl: this.URL + "/code",
      strategyUrl: this.URL + "/strategy",
      tableData: [],
      token:''
    };
  },
  methods: {
    getStrategyData() {
      this.$axios
        .get(this.strategyUrl, {
          headers: {
            Authorization: "JWT " + this.token
          }
        })
        .then(res => {
          this.tableData = res.data.data;
        })
        .catch(err => {
          console.log(err);
        });
    },
    deal(name,operation){
      this.$axios
        .put(this.strategyUrl,this.$qs.stringify({name:name,operation:operation}),{
          headers: {
            Authorization: "JWT " + this.token
          }
        })
        .then(res => {
          let returnData=res.data
          this.tip(returnData.success,returnData.msg,this,true)
        })
        .catch(err => {
          console.log(err);
        });
    },
    edit(name){
      this.$router.push({
        path:"/editor/index",
        query:{
          name:name
        }
      })
    },
    deleteStrategy(name){
      this.$confirm("此操作将永久删除该策略, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          this.$axios
            .delete(this.strategyUrl, {
              params:{
                name: name
              },
              headers: {
                Authorization: "JWT " + this.token
              }
            })
            .then(res => {
              let returnData=res.data
              this.tip(returnData.success,returnData.msg,this,true)
            })
            .catch(err => {
              console.log(err);
            });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    },
    goEditor(){
      this.$router.push({
        path:"/editor/index",
      })
    }
  },
  mounted() {
    this.token = sessionStorage.getItem("token");
    this.getStrategyData();
  }
};
</script>
<style lang='scss' scoped>
.strategy {
  padding: 20px;
  width: 100%;
  height: 100%;
}
</style>
