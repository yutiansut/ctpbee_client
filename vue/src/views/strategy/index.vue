<template>
  <div class="strategy">
    <el-button size="medium" type="success" @click="goEditor()">编辑器</el-button>
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="name" label="策略名称"></el-table-column>
      <el-table-column prop="status" label="状态"></el-table-column>
      <el-table-column prop="operation" label="操作">
        <template slot-scope="scope">
          <el-button size="mini" type="success" v-if="scope.row.status!=='运行中'" @click="handleEdit(scope.$index, scope.row)">开启</el-button>
          <el-button size="mini" type="danger" v-else @click="handleDelete(scope.$index, scope.row)">关闭</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
export default {
  data() {
    return {
      strategyUrl: this.URL + "/write_strategy",
      tableData: []
    };
  },
  methods: {
    goEditor() {
      this.$router.push("/editor/index");
    },
    getStrategyData() {
      let token = sessionStorage.getItem("token");
      this.$axios
        .get(this.strategyUrl, {
          headers: {
            Authorization: "JWT " + token
          }
        })
        .then(res => {
          console.log(res);
          this.tableData = res.data.data;
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {
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
