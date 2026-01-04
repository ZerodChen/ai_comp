<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>Ticket Management Tool</h1>
          <nav>
            <router-link to="/">Tickets</router-link>
            <router-link to="/tags">Tags</router-link>
          </nav>
        </div>
      </el-header>
      <el-main>
        <RouterView />
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

nav {
  display: flex;
  gap: 20px;
}

nav a {
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

nav a.router-link-active {
  color: #409eff;
}

.el-header {
  border-bottom: 1px solid #dcdfe6;
  background-color: #fff;
}

.el-main {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding-top: 20px;
}
</style>
