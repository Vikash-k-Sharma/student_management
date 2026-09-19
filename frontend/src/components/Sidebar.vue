<script setup>
</script>

<template>
  <aside class="sidebar">
    <div class="brand">
      <i class="fa-solid fa-graduation-cap"></i>
    </div>

    <nav class="nav-links">
      <RouterLink to="/dashboard" class="nav-item">
        <i class="fa-solid fa-house icon"></i>
        <span>Dashboard</span>
      </RouterLink>

      <RouterLink to="/students" class="nav-item">
        <i class="fa-solid fa-user icon"></i>
        <span>Students</span>
      </RouterLink>

      <RouterLink to="/courses" class="nav-item">
        <i class="fa-solid fa-book icon"></i>
        <span>Courses</span>
      </RouterLink>

      <RouterLink to="/reports" class="nav-item">
        <i class="fa-solid fa-file-lines icon"></i>
        <span>Reports</span>
      </RouterLink>
    </nav>

    <RouterLink to="/logout" class="nav-item logout">
      <i class="fa-solid fa-right-from-bracket icon"></i>
      <span>Logout</span>
    </RouterLink>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 220px;
  min-width: 220px;
  height: 100vh;
  position: sticky;
  top: 0;
  background: #1e2a4a;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
}

.brand {
  text-align: center;
  font-size: 26px;
  margin-bottom: 20px;
  color: #4f8dfd;
}

.nav-links {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 0 0 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #cfd6e8;
  text-decoration: none;
  padding: 12px 16px;
  border-radius: 8px 0 0 8px;
  font-size: 15px;
}

.nav-item .icon {
  width: 18px;
  text-align: center;
  font-size: 16px;
}

.nav-item:hover {
  background: #2c3a63;
}

.nav-item.router-link-active {
  background: #3b6fe0;
  color: white;
  font-weight: bold;
}

.nav-item.logout {
  margin: 0 12px 8px 12px;
}
</style>