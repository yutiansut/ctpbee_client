exports.install = function (Vue, options) {
  Vue.prototype.tips = function (tipOptions) {
    let tipType = tipOptions.type === true ? 'success' : 'error'
    let tipMsg = tipOptions.msg === 'token error' ? '登录信息已过期，请重新登录!' : tipOptions.msg
    if (tipType === 'success') {
      //是否需要弹窗提示（eg:请求成功时，并非都需要弹窗提示）
      if (tipOptions.isTips === true) {
        this.$message({
          showClose: true,
          message: tipMsg,
          type: tipType
        })
      }
      //成功时的回调函数
      tipOptions.success&&tipOptions.success()
    } else {
      this.$message({
        showClose: true,
        message: tipMsg,
        type: tipType
      })
      //重新登录
      if (tipMsg === '登录信息已过期，请重新登录!') {
        sessionStorage.removeItem('token')
        this.$router.push({
          path: '/login'
        })
      }
    }
  };
};
