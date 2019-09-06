<template>
  <div class="order">
    <el-row :gutter="20">
      <el-col :span="16" :xs="24">
        <el-card class="box-card">
          <el-tabs tab-position="top">
            <el-tab-pane label="持仓数据">
              <el-table :data="tableData" border style="width: 100%">
                <el-table-column prop="date" label="日期" width="180"></el-table-column>
                <el-table-column prop="name" label="姓名" width="180"></el-table-column>
                <el-table-column prop="address" label="地址"></el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="待成交数据">配置管理</el-tab-pane>
            <el-tab-pane label="发单数据">角色管理</el-tab-pane>
            <el-tab-pane label="成交数据">定时任务补偿</el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
      <el-col :span="8" :xs="24">
        <el-card class="box-card">
          <el-form label-position="right" label-width="50px" :model="orderForm">
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
              <el-input v-model="orderForm.price" placeholder="请输入价格"></el-input>
            </el-form-item>
            <el-form-item label="手数">
              <el-input v-model="orderForm.num" placeholder="请输入手数"></el-input>
            </el-form-item>
            <el-form-item label>
              <el-button type="success">买多</el-button>
              <el-button type="primary">卖空</el-button>
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
      orderForm: {
        price: "",
        num: ""
      },
      options: [
        {
          value: "限价",
          label: "限价"
        },
        {
          value: "市假",
          label: "市假"
        }
      ],
      type: "",
      tableData: [
        {
          date: "2016-05-02",
          name: "LWSB",
          address: "上海市普陀区金沙江路 1518 弄"
        },
        {
          date: "2016-05-04",
          name: "LWSB",
          address: "上海市普陀区金沙江路 1517 弄"
        },
        {
          date: "2016-05-01",
          name: "LWSB",
          address: "上海市普陀区金沙江路 1519 弄"
        }
      ]
    };
  },
  created() {},
  methods: {}
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
