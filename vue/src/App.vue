<template>
  <div id="app">
    <router-view v-if="isRouterAlive" />
  </div>
</template>

<script>
export default {
  name: "App",
  provide() {
    return {
      reload: this.reload
    };
  },
  data() {
    return {
      isRouterAlive: true,
      checkUrl: this.URL + "/check_key"
    };
  },
  methods: {
    reload() {
      this.isRouterAlive = false;
      this.$nextTick(function() {
        this.isRouterAlive = true;
      });
    }
  },
  created() {
    const token = sessionStorage.getItem("token");
    if (!token) {
      this.$router.push({ path: "/login" });
    }
  },
  methods: {
    check() {
      let mdStr = sessionStorage.getItem("key");
      let token = sessionStorage.getItem("token");
      console.log("begin:" + token);
      if (!token) {
        return;
      }
      this.$axios
        .post(this.checkUrl, this.$qs.stringify({ check_key: mdStr }), {
          headers: {
            Authorization: "JWT " + token
          }
        })
        .then(res => {
          let returnData = res.data;
          console.log("check:" + returnData.data);
          if (returnData.success === true) {
            sessionStorage.setItem("token", returnData.data);
          }
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  created() {
    // console.log(222)
    this.check();
  }
};
</script>
<style lang="scss">
</style>
