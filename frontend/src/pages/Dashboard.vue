<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import api from '../api.js'
import Chart from 'chart.js/auto'

const students = ref([])
const loading = ref(true)
const error = ref(null)

const lineCanvas = ref(null)
const donutCanvas = ref(null)
let lineChartInstance = null
let donutChartInstance = null

const today = new Date().toLocaleDateString('en-GB', {
  weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
})

const fetchStudents = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get('/students')
    students.value = response.data
  } catch (err) {
    error.value = 'Data fetch karne mein error aaya: ' + err.message
  } finally {
    loading.value = false
    await nextTick()
    renderCharts()
  }
}

const totalStudents = computed(() => students.value.length)
const totalCourses = computed(() => new Set(students.value.map(s => s.course)).size)
const activeStudents = computed(() => students.value.filter(s => s.status === 'Active').length)
const inactiveStudents = computed(() => students.value.filter(s => s.status === 'Inactive').length)

const recentStudents = computed(() =>
  [...students.value].sort((a, b) => b.id - a.id).slice(0, 5)
)

// Students by Course (real data)
const courseBreakdown = computed(() => {
  const counts = {}
  students.value.forEach(s => {
    counts[s.course] = (counts[s.course] || 0) + 1
  })
  return Object.entries(counts).map(([course, count]) => ({ course, count }))
})

// Enrollment by month (based on created_at, real data)
const enrollmentByMonth = computed(() => {
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  const counts = new Array(12).fill(0)
  students.value.forEach(s => {
    if (s.created_at) {
      const m = new Date(s.created_at).getMonth()
      counts[m]++
    }
  })
  return { labels: months, data: counts }
})

const donutColors = ['#3b82f6', '#22c55e', '#f59e0b', '#a855f7', '#ef4444', '#06b6d4']

const renderCharts = () => {
  if (lineChartInstance) lineChartInstance.destroy()
  if (donutChartInstance) donutChartInstance.destroy()

  if (lineCanvas.value) {
    lineChartInstance = new Chart(lineCanvas.value, {
      type: 'line',
      data: {
        labels: enrollmentByMonth.value.labels,
        datasets: [{
          label: 'Students Added',
          data: enrollmentByMonth.value.data,
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59,130,246,0.15)',
          fill: true,
          tension: 0.3,
          pointBackgroundColor: '#3b82f6'
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
      }
    })
  }

  if (donutCanvas.value) {
    donutChartInstance = new Chart(donutCanvas.value, {
      type: 'doughnut',
      data: {
        labels: courseBreakdown.value.map(c => c.course),
        datasets: [{
          data: courseBreakdown.value.map(c => c.count),
          backgroundColor: donutColors,
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        cutout: '65%',
        plugins: { legend: { display: false } }
      }
    })
  }
}

onMounted(fetchStudents)
</script>

<template>
  <div class="container-fluid">
    <div class="d-flex justify-content-between align-items-start mb-3">
      <div>
        <h2 class="mb-0">Dashboard</h2>
        <p class="text-muted mb-0">Welcome back, Admin! overview of your system.</p>
      </div>
      <span class="badge text-bg-light border">
        <i class="fa-regular fa-calendar me-1"></i>{{ today }}
      </span>
    </div>

    <div v-if="loading">Loading dashboard...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <template v-else>
 
      <div class="row g-3 mb-3">
        <div class="col-md-3">
          <div class="card border-0 bg-primary-subtle h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="stat-icon bg-primary text-white"><i class="fa-solid fa-users"></i></div>
              <div>
                <div class="text-muted small">Total Students</div>
                <div class="fs-4 fw-bold">{{ totalStudents }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 bg-success-subtle h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="stat-icon bg-success text-white"><i class="fa-solid fa-book"></i></div>
              <div>
                <div class="text-muted small">Total Courses</div>
                <div class="fs-4 fw-bold">{{ totalCourses }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 bg-warning-subtle h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="stat-icon bg-warning text-white"><i class="fa-solid fa-user-check"></i></div>
              <div>
                <div class="text-muted small">Active Students</div>
                <div class="fs-4 fw-bold">{{ activeStudents }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 bg-danger-subtle h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="stat-icon bg-danger text-white"><i class="fa-solid fa-user-slash"></i></div>
              <div>
                <div class="text-muted small">Inactive Students</div>
                <div class="fs-4 fw-bold">{{ inactiveStudents }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CHARTS -->
      <div class="row g-3 mb-3">
        <div class="col-lg-7">
          <div class="card h-100">
            <div class="card-body">
              <h6 class="fw-bold mb-3"><i class="fa-solid fa-chart-line me-2"></i>Student Enrollment</h6>
              <canvas ref="lineCanvas" height="120"></canvas>
            </div>
          </div>
        </div>
        <div class="col-lg-5">
          <div class="card h-100">
            <div class="card-body">
              <h6 class="fw-bold mb-3"><i class="fa-solid fa-chart-pie me-2"></i>Students by Course</h6>
              <div class="d-flex align-items-center gap-3">
                <div style="width: 160px; height: 160px;">
                  <canvas ref="donutCanvas"></canvas>
                </div>
                <ul class="list-unstyled mb-0 flex-grow-1">
                  <li v-for="(c, i) in courseBreakdown" :key="c.course" class="d-flex justify-content-between mb-2">
                    <span>
                      <span class="dot me-2" :style="{ background: donutColors[i % donutColors.length] }"></span>
                      {{ c.course }}
                    </span>
                    <strong>{{ c.count }}</strong>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TABLES -->
      <div class="row g-3">
        <div class="col-lg-7">
          <div class="card h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="fw-bold mb-0"><i class="fa-regular fa-clock me-2"></i>Recent Students</h6>
                <RouterLink to="/students" class="small">View All</RouterLink>
              </div>
              <div class="table-responsive">
                <table class="table table-sm align-middle">
                  <thead class="table-light">
                    <tr>
                      <th>#</th>
                      <th>Name</th>
                      <th>Course</th>
                      <th>Email</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(s, i) in recentStudents" :key="s.id">
                      <td>{{ i + 1 }}</td>
                      <td>{{ s.name }}</td>
                      <td>{{ s.course }}</td>
                      <td>{{ s.email }}</td>
                      <td>
                        <span class="badge" :class="s.status === 'Active' ? 'text-bg-success' : 'text-bg-danger'">
                          {{ s.status }}
                        </span>
                      </td>
                    </tr>
                    <tr v-if="recentStudents.length === 0">
                      <td colspan="5" class="text-center text-muted py-3">Koi student nahi mila.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}
.dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
</style>