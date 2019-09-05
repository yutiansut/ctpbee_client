<template>
  <div id="app">
    <router-view  v-if='isRouterAlive'/>
  </div>
</template>

<script>
export default {
  name: "App",
  provide(){
    return {
      reload:this.reload
    }
  },
  data(){
    return {
      isRouterAlive:true
    }
  },
  methods:{
    reload(){
      this.isRouterAlive=false
      this.$nextTick(function(){
        this.isRouterAlive=true
      })
    }
  },
  created(){
    const token=sessionStorage.getItem('token')
    if(!token){
      this.$router.push({path:'/login'})
    }
  }
};
</script>
<style lang="scss">

</style>
