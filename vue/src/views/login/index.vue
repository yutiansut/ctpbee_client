<template>
  <div class="box">
    <div class="login">
      <el-tabs type="border-card">
        <el-tab-pane label="普通登录">
          <el-form :model="commonLogin">
            <el-input type="text" v-model="commonLogin.userid" placeholder="用户名/USERNAME"></el-input>
            <el-input
              type="password"
              v-model="commonLogin.password"
              placeholder="账号密码/PASSWORD"
              show-password
            ></el-input>
            <el-input
              type="password"
              v-model="commonLogin.authorization"
              placeholder="授权码/AUTHORIZATION_CODE"
              @keyup.enter.native="handleLogin(detailedLogin,'common')"
            ></el-input>
            <el-select v-model="interface" clearable placeholder="请选择">
              <el-option
                v-for="item in interfaceOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
            <el-select v-model="simnowValue" clearable placeholder="请选择">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
            <el-form-item>
              <el-button
                type="primary"
                @keyup.enter="handleLogin(commonLogin,'common')"
                @click="handleLogin(commonLogin,'common')"
              >登录</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="详细登录" class="detailBox">
          <el-form :model="detailedLogin">
            <el-input type="text" v-model="detailedLogin.userid" placeholder="用户名/USERNAME"></el-input>
            <el-input
              type="password"
              v-model="detailedLogin.password"
              placeholder="账号密码/PASSWORD"
              show-password
            ></el-input>
            <el-input type="text" v-model="detailedLogin.brokerid" placeholder="期货公司编号/BROKERID"></el-input>
            <el-input type="text" v-model="detailedLogin.appid" placeholder="产品名称/APPID"></el-input>
            <el-input type="text" v-model="detailedLogin.auth_code" placeholder="认证码/AUTH_CODE"></el-input>
            <el-input type="text" v-model="detailedLogin.td_address" placeholder="交易前置/TD_ADDRESS"></el-input>
            <el-input type="text" v-model="detailedLogin.md_address" placeholder="行情前置/MD_ADDRESS"></el-input>
            <el-input
              type="password"
              v-model="detailedLogin.AuthorizationCode"
              placeholder="授权码/AUTHORIZATION_CODE"
              @keyup.enter.native="handleLogin(detailedLogin,'detail')"
            ></el-input>
            <el-select v-model="interface" clearable placeholder="请选择">
              <el-option
                v-for="item in interfaceOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
            <el-form-item>
              <el-button type="primary" @click="handleLogin(detailedLogin,'detail')">登录</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import { setTimeout } from "timers";
export default {
  name: "Login",
  data() {
    return {
      loginUrl: this.URL + "/login",
      checkUrl: this.URL + "/check_key",
      commonLogin: {
        userid: "089131",
        password: "350888",
        authorization: "00000000"
      },
      interfaceOptions: [
        {
          value: "ctp",
          label: "ctp"
        },
        {
          value: "ctp_se",
          label: "ctp_se"
        }
      ],
      interface: "ctp",
      options: [
        {
          value: "simnow24小时",
          label: "simnow24小时"
        },
        {
          value: "simnow移动",
          label: "simnow移动"
        }
      ],
      simnowValue: "simnow24小时",
      detailedLogin: {
        userid: "",
        password: "",
        detailedLogin: "",
        brokerid: "",
        appid: "",
        auth_code: "",
        td_address: "",
        md_address: ""
      },
      simple_login_info: {
        simnow_forever: {
          appid: "simnow_client_test",
          auth_code: "0000000000000000",
          td_address: "tcp://180.168.146.187:10130",
          md_address: "tcp://180.168.146.187:10131",
          brokerid: "9999"
        },
        simnow_inet: {
          appid: "simnow_client_test",
          auth_code: "0000000000000000",
          td_address: "tcp://218.202.237.33:10102",
          md_address: "tcp://218.202.237.33:10112",
          brokerid: "9999"
        }
      },
      loading: false
    };
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true
    }
  },
  methods: {
    handleLogin(data, type) {
      data["interface"] = this.interface;
      if (type === "common") {
        let simnowObj =
          this.simnowValue === "simnow24小时"
            ? this.simple_login_info["simnow_forever"]
            : this.simple_login_info["simnow_inet"];
        for (let i in simnowObj) {
          data[i] = simnowObj[i];
        }
      }
      this.$axios
        .post(this.loginUrl, this.$qs.stringify(data))
        .then(res => {
          console.log(res);
          let returnData = res.data;
          this.tip(returnData.success, returnData.msg, this);
          if (returnData.success === true) {
            let id = data.userid;
            let password = data.password;
            let str = id + "9615" + password;
            let mdStr = this.$md5(str);
            sessionStorage.setItem("key", mdStr);
            sessionStorage.setItem("token", returnData.data);
            setTimeout(() => {
              this.$router.push({ path: "/" });
            }, 1000);
          }
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {}
};
</script>

<style lang="scss" scoped>
$bg: #283443;
$light_gray: #fff;
$cursor: #fff;
$width: 400px;
.box {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #eee;
}
.login {
  width: $width;
  box-sizing: border-box;
}
</style>
<style lang="scss">
$width: 400px;
.login {
  .el-tabs__item {
    width: $width/2;
    text-align: center;
  }
  .el-input {
    margin-top: 20px;
  }
  .el-select {
    width: 100%;
  }
  .el-button {
    width: 100%;
    margin-top: 20px;
  }
  .detailBox {
    .el-input {
      margin-top: 12px;
    }
    .el-form-item {
      margin-bottom: 10px;
    }
  }
}
</style>
