<template>
  <div class="navbar">
    <hamburger
      :is-active="sidebar.opened"
      class="hamburger-container"
      @toggleClick="toggleSideBar"
    />

    <breadcrumb class="breadcrumb-container" />

    <div class="right-menu">
      <el-dropdown class="avatar-container" trigger="click">
        <div class="avatar-wrapper">
          ·
          <!-- <img :src="avatar+'?imageView2/1/w/80/h/80'" class="user-avatar"> -->
          <img src="@/assets/img/Admin.png" alt srcset width="20px" style="vertical-align:middle" />
          <span>admin</span>
          <!-- <i class="el-icon-caret-bottom" /> -->
        </div>
        <el-dropdown-menu slot="dropdown" class="user-dropdown">
          <router-link to="/dashboard/index">
            <el-dropdown-item>首页</el-dropdown-item>
          </router-link>
          <el-dropdown-item>
            <span style="display:block;" @click="dialogVisible = true">修改授权码</span>
          </el-dropdown-item>
          <el-dropdown-item>
            <span style="display:block;" @click="serveConfirm = true">服务器退出</span>
          </el-dropdown-item>
          <el-dropdown-item>
            <span style="display:block;" @click="logout">本地退出</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
    <el-dialog
      title="修改授权码"
      :visible.sync="dialogVisible"
      width="30%"
      @click="dialogVisible = false"
    >
      <el-form label-position="right" label-width="60px" :model="modifyCode">
        <el-form-item label="密码">
          <el-input type="password" v-model="modifyCode.password"></el-input>
        </el-form-item>
        <el-form-item label="授权码">
          <el-input type="password" v-model="modifyCode.authorization"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="modify(modifyCode)">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="服务器退出确认"
      :visible.sync="serveConfirm"
      width="30%"
      @click="serveConfirm = false"
    >
      <el-form label-position="right" label-width="60px" :model="serveLayoutForm">
        <el-form-item label="授权码">
          <el-input type="password" v-model="serveLayoutForm.authorization"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="serveConfirm = false">取 消</el-button>
        <el-button type="primary" @click="servelogout(serveLayoutForm)">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import Breadcrumb from "@/components/Breadcrumb";
import Hamburger from "@/components/Hamburger";
import { setTimeout } from "timers";

export default {
  data() {
    return {
      modifyUrl: "auth_code",
      serveUrl: "logout",
      dialogVisible: false,
      serveConfirm: false,
      token: "",
      modifyCode: {
        password: "",
        authorization: ""
      },
      serveLayoutForm: {
        authorization: ""
      }
    };
  },
  components: {
    Breadcrumb,
    Hamburger
  },
  computed: {
    ...mapGetters(["sidebar", "avatar"])
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch("app/toggleSideBar");
    },
    logout() {
      sessionStorage.removeItem("token");
      this.$router.push({ path: "/login" });
    },
    modify(data) {
      this.$axios
        .put(this.modifyUrl,data)
        .then(res => {
          let returnData = res.data;
           this.tips({
            type: returnData.success,
            msg: returnData.msg,
            isTips:true,
            success: () => {
              this.dialogVisible = false;
            }
          })

        })
        .catch(err => {
          console.log(err);
        });
    },
    servelogout(data) {
      this.$axios
        .post(this.serveUrl, data)
        .then(res => {
          let returnData = res.data;
          this.tips({
            type: returnData.success,
            msg: returnData.msg,
            isTips:true,
            success: () => {
               this.logout();
            }
          })
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.token = sessionStorage.getItem("token");
  }
};
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background 0.3s;
    -webkit-tap-highlight-color: transparent;

    &:hover {
      background: rgba(0, 0, 0, 0.025);
    }
  }

  .breadcrumb-container {
    float: left;
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background 0.3s;

        &:hover {
          background: rgba(0, 0, 0, 0.025);
        }
      }
    }

    .avatar-container {
      margin-right: 30px;
      cursor: pointer;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
}
</style>
<style lang="scss">
.el-dialog__body {
  padding-bottom: 10px;
}
</style>
