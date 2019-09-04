<template>
  <div class="dashboard">
    <!-- <a href="http://community.ctpbee.com">社区</a> -->
    <!-- <a>文档</a> -->
    <el-calendar v-model="value"></el-calendar>
  </div>
</template>

<script>
import { Socket } from 'dgram';
import { setInterval, clearInterval } from 'timers';
export default {
  name: "Dashboard",
  data() {
    return {
      value: new Date()
    };
  },
  created(){
    const token=sessionStorage.getItem('token')
    if(!token){
      this.$router.push({path:'/login'})
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
<style lang="scss">
.dashboard {
  .el-calendar__body {
    padding: 0 20px;
  }
  .el-calendar-table .el-calendar-day {
    height: 78px;
    text-align: center;
    line-height: 75px;
  }
  .el-calendar-table td.is-selected {
    background-color: #eee;
  }
}
</style>
