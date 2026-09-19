<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'
import Chart from 'chart.js/auto'
import api from '../api.js'

const students = ref([])
const loading = ref(true)
const error = ref(null)
const courseCanvas = ref(null)
let courseChart = null

const studentCode = (id) => 'ST' + String(id).padStart(3, '0')

const fetchStudents = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await api.get('/students')
    students.value = response.data
  } catch (err) {
    error.value = 'Student report load karne mein error aaya: ' + err.message
  } finally {
    loading.value = false
    await nextTick()
    renderCourseChart()
  }
}

const summary = computed(() => {
  const courses = new Set(students.value.map(s => s.course).filter(Boolean))
  const active = students.value.filter(s => s.status === 'Active').length

  return {
    total: students.value.length,
    active,
    inactive: students.value.length - active,
    courses: courses.size
  }
})

const courseReport = computed(() => {
  const report = students.value.reduce((list, student) => {
    const course = student.course || 'Not Assigned'
    const item = list[course] || { course, total: 0, active: 0, inactive: 0 }

    item.total += 1
    if (student.status === 'Active') {
      item.active += 1
    } else {
      item.inactive += 1
    }

    list[course] = item
    return list
  }, {})

  return Object.values(report).sort((a, b) => b.total - a.total)
})

const statusReport = computed(() => [
  { label: 'Active Students', value: summary.value.active, className: 'text-bg-success' },
  { label: 'Inactive Students', value: summary.value.inactive, className: 'text-bg-secondary' }
])

const recentStudents = computed(() =>
  [...students.value].sort((a, b) => b.id - a.id).slice(0, 8)
)

const chartColors = ['#2563eb', '#16a34a', '#f59e0b', '#dc2626', '#7c3aed', '#0891b2', '#ea580c']

const renderCourseChart = () => {
  if (courseChart) courseChart.destroy()
  if (!courseCanvas.value || loading.value || error.value) return

  courseChart = new Chart(courseCanvas.value, {
    type: 'bar',
    data: {
      labels: courseReport.value.map(item => item.course),
      datasets: [
        {
          label: 'Students',
          data: courseReport.value.map(item => item.total),
          backgroundColor: courseReport.value.map((_, index) => chartColors[index % chartColors.length]),
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1 }
        }
      }
    }
  })
}

const printReport = () => {
  window.print()
}

onMounted(fetchStudents)

onUnmounted(() => {
  if (courseChart) courseChart.destroy()
})
</script>

<template>
  <div class="container-fluid reports-page">
    <div class="d-flex justify-content-between align-items-start gap-3 mb-3">
      <div>
        <h2 class="mb-0">Student Report</h2>
        <p class="text-muted mb-0">Students ka complete summary aur course-wise report</p>
      </div>
      <button class="btn btn-primary print-button" @click="printReport">
        <i class="fa-solid fa-print me-2"></i>Print
      </button>
    </div>

    <div v-if="loading">Loading student report...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <template v-else>
      <div class="row g-3 mb-3">
        <div class="col-md-3">
          <div class="card border-0 bg-primary-subtle h-100">
            <div class="card-body">
              <div class="text-muted small">Total Students</div>
              <div class="fs-3 fw-bold">{{ totalStudents }}</div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 bg-success-subtle h-100">
            <div class="card-body">
              <div class="text-muted small">Active Students</div>
              <div class="fs-3 fw-bold">{{ activeStudents }}</div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 bg-secondary-subtle h-100">
            <div class="card-body">
              <div class="text-muted small">Inactive Students</div>
              <div class="fs-3 fw-bold">{{ inactiveStudents }}</div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 bg-warning-subtle h-100">
            <div class="card-body">
              <div class="text-muted small">Total Courses</div>
              <div class="fs-3 fw-bold">{{ totalCourses }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-3 mb-3">
        <div class="col-lg-8">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="mb-3"><i class="fa-solid fa-chart-column text-primary me-2"></i>Course-wise Students</h5>
              <div class="chart-box">
                <canvas ref="courseCanvas"></canvas>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="mb-3"><i class="fa-solid fa-circle-info text-primary me-2"></i>Status Summary</h5>
              <div class="d-grid gap-2">
                <div
                  v-for="item in statusReport"
                  :key="item.label"
                  class="d-flex justify-content-between align-items-center border rounded px-3 py-2"
                >
                  <span>{{ item.label }}</span>
                  <span class="badge" :class="item.className">{{ item.value }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-3">
        <div class="card-body">
          <h5 class="mb-3"><i class="fa-solid fa-book-open text-primary me-2"></i>Course Report</h5>
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead class="table-light">
                <tr>
                  <th>#</th>
                  <th>Course</th>
                  <th>Total Students</th>
                  <th>Active</th>
                  <th>Inactive</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in courseReport" :key="item.course">
                  <td>{{ index + 1 }}</td>
                  <td>{{ item.course }}</td>
                  <td>{{ item.total }}</td>
                  <td>{{ item.active }}</td>
                  <td>{{ item.inactive }}</td>
                </tr>
                <tr v-if="courseReport.length === 0">
                  <td colspan="5" class="text-center text-muted py-3">Koi course report nahi mila.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <h5 class="mb-3"><i class="fa-solid fa-users text-primary me-2"></i>Student List Report</h5>
          <div class="table-responsive">
            <table class="table table-hover align-middle">
              <thead class="table-light">
                <tr>
                  <th>#</th>
                  <th>Student ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Age</th>
                  <th>Course</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(student, index) in recentStudents" :key="student.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ studentCode(student.id) }}</td>
                  <td>{{ student.name }}</td>
                  <td>{{ student.email }}</td>
                  <td>{{ student.age }}</td>
                  <td>{{ student.course }}</td>
                  <td>
                    <span class="badge" :class="student.status === 'Active' ? 'text-bg-success' : 'text-bg-secondary'">
                      {{ student.status }}
                    </span>
                  </td>
                </tr>
                <tr v-if="recentStudents.length === 0">
                  <td colspan="7" class="text-center text-muted py-3">Koi student nahi mila.</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-if="students.length > recentStudents.length" class="text-muted small mb-0">
            Latest {{ recentStudents.length }} students dikh rahe hain. Full list ke liye Students page open karein.
          </p>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.chart-box {
  height: 300px;
}

@media print {
  .print-button {
    display: none;
  }

  .reports-page {
    background: #fff;
  }
}
</style>
