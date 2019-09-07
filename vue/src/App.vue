<template>
  <div id="app">
    <router-view v-if="isRouterAlive" />
  </div>
</template>

<script>
export default {
  name: "App",
   provide() { // 注册一个方法
    return {
      reload: this.reload
    }
  },
  data() {
    return {
      isRouterAlive: true
    }
  },
  methods: {
    reload() {
      this.isRouterAlive = false
      this.$nextTick(function() {
        this.isRouterAlive = true
      })
    }
  },
  mounted() {
    const token = sessionStorage.getItem("token");
    if (!token) {
      this.$router.push({ path: "/login" });
    }
  },
  methods: {
    // check() {
    //   let mdStr = sessionStorage.getItem("key");
    //   let token = sessionStorage.getItem("token");
    //   console.log("begin:" + token);
    //   if (!token) {
    //     return;
    //   }
    //   this.$axios
    //     .post(this.checkUrl, this.$qs.stringify({ check_key: mdStr }), {
    //       headers: {
    //         Authorization: "JWT " + token
    //       }
    //     })
    //     .then(res => {
    //       let returnData = res.data;
    //       console.log("check:" + returnData.data);
    //       if (returnData.success === true) {
    //         sessionStorage.setItem("token", returnData.data);
    //       }
    //     })
    //     .catch(err => {
    //       console.log(err);
    //     });
    // }
  }
};
</script>
<style lang="scss">
</style>
