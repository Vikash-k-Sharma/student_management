<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api.js'

const students = ref([])
const loading = ref(true)
const error = ref(null)

const searchQuery = ref('')
const courseFilter = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = 5

const showForm = ref(false)
const editingId = ref(null)
const deletingId = ref(null)

const getEmptyForm = () => ({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    course: '',
    status: 'Active',
    address: ''
})
const form = ref(getEmptyForm())
const submitting = ref(false)
const formError = ref(null)

const fetchStudents = async () => {
    loading.value = true
    error.value = null
    try {
        const response = await api.get('/students')
        students.value = response.data
    } catch (err) {
        error.value = 'Students fetch karne mein error aaya: ' + err.message
    } finally {
        loading.value = false
    }
}

const studentCode = (id) => 'ST' + String(id).padStart(3, '0')

const courseOptions = computed(() => [...new Set(students.value.map(s => s.course))])

const filteredStudents = computed(() => {
    let list = students.value
    if (searchQuery.value.trim()) {
        const q = searchQuery.value.toLowerCase()
        list = list.filter(s =>
            s.name.toLowerCase().includes(q) ||
            s.email.toLowerCase().includes(q) ||
            studentCode(s.id).toLowerCase().includes(q)
        )
    }
    if (courseFilter.value) list = list.filter(s => s.course === courseFilter.value)
    if (statusFilter.value) list = list.filter(s => s.status === statusFilter.value)
    return list
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredStudents.value.length / pageSize)))
const paginatedStudents = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    return filteredStudents.value.slice(start, start + pageSize)
})
const rangeStart = computed(() => filteredStudents.value.length === 0 ? 0 : (currentPage.value - 1) * pageSize + 1)
const rangeEnd = computed(() => Math.min(currentPage.value * pageSize, filteredStudents.value.length))

const goToPage = (page) => {
    if (page < 1 || page > totalPages.value) return
    currentPage.value = page
}
const onFilterChange = () => { currentPage.value = 1 }
const resetFilters = () => {
    searchQuery.value = ''
    courseFilter.value = ''
    statusFilter.value = ''
    currentPage.value = 1
}

const openAddForm = () => {
    editingId.value = null
    form.value = getEmptyForm()
    formError.value = null
    showForm.value = true
}

const openEditForm = (student) => {
    const parts = student.name.split(' ')
    editingId.value = student.id
    form.value = {
        firstName: parts[0] || '',
        lastName: parts.slice(1).join(' ') || '',
        email: student.email,
        phone: student.phone || '',
        course: student.course,
        status: student.status,
        address: student.address || ''
    }
    formError.value = null
    showForm.value = true
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
}

const closeForm = () => {
    showForm.value = false
    form.value = getEmptyForm()
    formError.value = null
}

const viewStudent = (student) => {
    alert(
        `Student ID: ${studentCode(student.id)}\n` +
        `Name: ${student.name}\n` +
        `Email: ${student.email}\n` +
        `Age: ${student.age}\n` +
        `Course: ${student.course}\n` +
        `Phone: ${student.phone || '-'}\n` +
        `Address: ${student.address || '-'}\n` +
        `Status: ${student.status}`
    )
}

const submitForm = async () => {
    submitting.value = true
    formError.value = null

    const payload = {
        name: `${form.value.firstName} ${form.value.lastName}`.trim(),
        email: form.value.email,
        age: editingId.value
            ? students.value.find(s => s.id === editingId.value)?.age
            : 18,
        course: form.value.course,
        phone: form.value.phone,
        address: form.value.address,
        status: form.value.status
    }

    try {
        if (editingId.value) {
            await api.put(`/students/${editingId.value}`, payload)
        } else {
            await api.post('/students', payload)
        }
        closeForm()
        fetchStudents()
    } catch (err) {
        formError.value = err.response?.data?.detail || ('Kuch galat ho gaya: ' + err.message)
    } finally {
        submitting.value = false
    }
}

const deleteStudent = async (student) => {
    if (!window.confirm(`Kya aap "${student.name}" ko delete karna chahte hain?`)) return
    deletingId.value = student.id
    try {
        await api.delete(`/students/${student.id}`)
        fetchStudents()
        if (editingId.value === student.id) closeForm()
    } catch (err) {
        alert('Delete karne mein error aaya: ' + err.message)
    } finally {
        deletingId.value = null
    }
}

onMounted(fetchStudents)
</script>

<template>
    <div class="container-fluid">
        <div class="d-flex justify-content-between align-items-start mb-3">
            <div>
                <h2 class="mb-0">Students</h2>
                <p class="text-muted mb-0">Manage all student records</p>
            </div>
            <button class="btn btn-primary" @click="openAddForm">+ Add Student</button>
        </div>

        <div class="row g-2 mb-3">
            <div class="col-md-4">
                <input v-model="searchQuery" @input="onFilterChange" type="text" class="form-control"
                    placeholder="Search by name, email or ID..." />
            </div>
            <div class="col-md-3">
                <select v-model="courseFilter" @change="onFilterChange" class="form-select">
                    <option value="">All Courses</option>
                    <option v-for="c in courseOptions" :key="c" :value="c">{{ c }}</option>
                </select>
            </div>
            <div class="col-md-3">
                <select v-model="statusFilter" @change="onFilterChange" class="form-select">
                    <option value="">All Status</option>
                    <option value="Active">Active</option>
                    <option value="Inactive">Inactive</option>
                </select>
            </div>
            <div class="col-md-2">
                <button class="btn btn-outline-secondary w-100" @click="resetFilters">Reset</button>
            </div>
        </div>

        <div v-if="loading">Loading students...</div>
        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-else class="card mb-3">
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>#</th>
                                <th>Student ID</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Course</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(student, index) in paginatedStudents" :key="student.id">
                                <td>{{ (currentPage - 1) * pageSize + index + 1 }}</td>
                                <td>{{ studentCode(student.id) }}</td>
                                <td>{{ student.name }}</td>
                                <td>{{ student.email }}</td>
                                <td>{{ student.course }}</td>
                                <td>
                                    <span class="badge"
                                        :class="student.status === 'Active' ? 'text-bg-success' : 'text-bg-secondary'">{{
                                            student.status }}</span>
                                </td>
                                <td>
                                    <div class="btn-group btn-group-sm">
                                        <button class="btn btn-outline-primary"
                                            @click="viewStudent(student)">View</button>
                                        <button class="btn btn-outline-warning"
                                            @click="openEditForm(student)">Edit</button>
                                        <button class="btn btn-outline-danger" :disabled="deletingId === student.id"
                                            @click="deleteStudent(student)">Delete</button>
                                    </div>
                                </td>
                            </tr>
                            <tr v-if="paginatedStudents.length === 0">
                                <td colspan="7" class="text-center text-muted py-3">Koi student nahi mila.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                    <span class="text-muted small">
                        Showing {{ rangeStart }} to {{ rangeEnd }} of {{ filteredStudents.length }} students
                    </span>
                    <nav>
                        <ul class="pagination pagination-sm mb-0">
                            <li class="page-item" :class="{ disabled: currentPage === 1 }">
                                <button class="page-link" @click="goToPage(currentPage - 1)">‹</button>
                            </li>
                            <li v-for="page in totalPages" :key="page" class="page-item"
                                :class="{ active: page === currentPage }">
                                <button class="page-link" @click="goToPage(page)">{{ page }}</button>
                            </li>
                            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                                <button class="page-link" @click="goToPage(currentPage + 1)">›</button>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>
        </div>

        <div class="card" v-if="showForm">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="mb-0">{{ editingId ? 'Edit Student' : 'Add Student' }}</h5>
                    <button class="btn-close" @click="closeForm"></button>
                </div>

                <div v-if="formError" class="alert alert-danger">{{ formError }}</div>

                <form @submit.prevent="submitForm">
                    <div class="row g-3 mb-3">
                        <div class="col-md-6">
                            <label class="form-label">First Name</label>
                            <input v-model="form.firstName" type="text" class="form-control" required />
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Last Name</label>
                            <input v-model="form.lastName" type="text" class="form-control" />
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Email</label>
                            <input v-model="form.email" type="email" class="form-control" required />
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Phone</label>
                            <input v-model="form.phone" type="text" class="form-control" />
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Course</label>
                            <input v-model="form.course" type="text" class="form-control" required />
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Status</label>
                            <select v-model="form.status" class="form-select">
                                <option value="Active">Active</option>
                                <option value="Inactive">Inactive</option>
                            </select>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Address</label>
                        <textarea v-model="form.address" rows="3" class="form-control"></textarea>
                    </div>

                    <div class="d-flex justify-content-end gap-2">
                        <button type="button" class="btn btn-outline-secondary" @click="closeForm">Cancel</button>
                        <button type="submit" class="btn btn-primary" :disabled="submitting">
                            {{ submitting ? 'Saving...' : 'Save Student' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>