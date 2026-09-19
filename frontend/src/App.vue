<script setup>
import Sidebar from './components/Sidebar.vue'
import Nav from './components/Nav.vue'
import { ref } from 'vue'

const searchQuery = ref('')
</script>

<template>
  <div class="layout">
    <Sidebar />

    <div class="main">
      <Nav v-model:searchQuery="searchQuery" />
      <div class="content">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  overflow-x: hidden;
  font-family: 'Segoe UI', Arial, sans-serif;
  background: #f4f6fb;
}

.layout {
  display: flex;
  height: 100vh;
  width: 100%;
}

.main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
}

.content {
  padding: 0px 24px 24px 24px;
}
</style>