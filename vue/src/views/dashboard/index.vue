<template>
  <div class="dashboard">
    <!-- <a href="http://community.ctpbee.com">社区</a> -->
    <!-- <a>文档</a> -->
    <el-calendar v-model="value"></el-calendar>
  </div>
</template>

<script>
import { Socket } from 'dgram';
import { setInterval } from 'timers';
export default {
  name: "Dashboard",
  data() {
    return {
      value: new Date()
    };
  },
  methods:{
    heart(){
      console.log(666)
      let token =sessionStorage.getItem('token')
      this.$socket.emit('heartbeat', token)
    }
  },
  mounted () {
    var timer=setInterval(()=>{
      clearInterval(timer)
      this.heart()
    },3000)
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
