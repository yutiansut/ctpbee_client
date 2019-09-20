<template>
  <div class="config">
    <el-card class="box-card">
      <table>
        <tr>
          <th>key</th>
          <th>value</th>
        </tr>
        <tr>
          <td>CLOSE_PATTERN</td>
          <td>
            <el-select v-model="tableData.CLOSE_PATTERN" clearable placeholder="请选择">
              <el-option
                v-for="item in closePatternOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </td>
        </tr>
        <tr>
          <td>INSTRUMENT_INDEPEND</td>
          <td>
            <el-switch
              v-model="tableData.INSTRUMENT_INDEPEND"
              active-color="#13ce66"
              inactive-color="#ff4949"
            ></el-switch>
          </td>
        </tr>
        <tr>
          <td>REFRESH_INTERVAL</td>
          <td>
            <el-input placeholder="请输入内容" v-model="tableData.REFRESH_INTERVAL"></el-input>
          </td>
        </tr>
        <tr>
          <td>SHARED_FUNC</td>
          <td>
            <el-switch
              v-model="tableData.SHARED_FUNC"
              active-color="#13ce66"
              inactive-color="#ff4949"
            ></el-switch>
          </td>
        </tr>
        <tr>
          <td>SLIPPAGE_SHORT</td>
          <td>
            <el-input placeholder="请输入内容" v-model="tableData.SLIPPAGE_SHORT"></el-input>
          </td>
        </tr>
        <tr>
          <td>SLIPPAGE_BUY</td>
          <td>
            <el-input placeholder="请输入内容" v-model="tableData.SLIPPAGE_BUY"></el-input>
          </td>
        </tr>
        <tr>
          <td>SLIPPAGE_COVER</td>
          <td>
            <el-input placeholder="请输入内容" v-model="tableData.SLIPPAGE_COVER"></el-input>
          </td>
        </tr>
        <tr>
          <td>SLIPPAGE_SELL</td>
          <td>
            <el-input placeholder="请输入内容" v-model="tableData.SLIPPAGE_SELL"></el-input>
          </td>
        </tr>
      </table>
      <el-button type="success" style="margin-top:10px;" @click="updateConfig(tableData)">确认更改</el-button>
    </el-card>
  </div>
</template>

<script>
export default {
  inject: ['reload'],
  data() {
    return {
      configUrl: 'config',
      tableData: {},
      closePatternOptions: [
        {
          value: 'today',
          label: 'today'
        },
        {
          value: 'yesterday',
          label: 'yesterday'
        }
      ]
    }
  },
  mounted() {
    this.getData()
  },
  methods: {
    getData() {
      this.$axios
        .get(this.configUrl)
        .then(res => {
          let returnData = res.data
          this.tips({
            type: returnData.success,
            msg: returnData.msg,
            isTips:false,
            success: () => {
              this.tableData = returnData.data
            }
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
    updateConfig(data) {
      this.$axios
        .put(this.configUrl, this.$qs.stringify(data))
        .then(res => {
          let returnData = res.data
          this.tips({
            type: returnData.success,
            msg: returnData.msg,
            isTips:true,
            success: () => {
              this.getData()
            }
          })
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>
<style lang="scss" scoped>
.config {
  padding: 20px;
}
.config {
  padding: 20px;
  table {
    width: 100%;
    border-collapse: collapse;
    tr {
      width: 100%;
    }
    tr th:nth-child(1) {
      color: #909399;
      width: 30%;
    }
    th,
    td {
      border: 1px solid #eee;
      line-height: 50px;
      padding-left: 10px;
      color: #606266;
      font-size: 16px;
      text-align: left;
    }
  }
}
</style>
<style>
.config .el-input__inner {
  width: 50%;
}
.config .el-select {
  width: 50%;
}
.config .el-select .el-input__inner {
  width: 100%;
}
</style>
