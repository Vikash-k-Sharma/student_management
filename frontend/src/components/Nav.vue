<script setup>
defineProps({
    searchQuery: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['update:searchQuery'])

const onInput = (e) => {
    emit('update:searchQuery', e.target.value)
}
</script>

<template>
    <header class="topbar">
        <h1>
            <i class="fa-solid fa-graduation-cap"></i>
            Student Management System
        </h1>
        <div class="topbar-right">
            <div class="search-box">
                <i class="fa-solid fa-magnifying-glass"></i>
                <input :value="searchQuery" @input="onInput" type="text" placeholder="Search students..." />
            </div>
            <div class="admin-badge">
                <i class="fa-solid fa-circle-user"></i>
                <span>Admin</span>
                <i class="fa-solid fa-chevron-down"></i>
            </div>
        </div>
    </header>
</template>

<style scoped>
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    flex-wrap: wrap;
    gap: 12px;
    background-color: rgb(205, 207, 209);
    padding: 15px;
}

.topbar h1 {
    font-size: 22px;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 10px;
    color: #1e2a4a;
}

.topbar-right {
    display: flex;
    align-items: center;
    gap: 16px;
}

.search-box {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border: 1px solid #ddd;
    border-radius: 20px;
    background: white;
    min-width: 220px;
}

.search-box i {
    color: #999;
}

.search-box input {
    border: none;
    outline: none;
    font-size: 14px;
    flex: 1;
}

.admin-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    background: white;
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid #ddd;
    white-space: nowrap;
    cursor: pointer;
}

.admin-badge i:first-child {
    font-size: 20px;
    color: #666;
}

.admin-badge i:last-child {
    font-size: 12px;
    color: #999;
}
</style>