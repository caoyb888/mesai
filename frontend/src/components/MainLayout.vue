<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { logout } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()
const isCollapse = ref(false)

const roleLabel = {
  TECH_LEAD: '技术负责人',
  AI_ENGINEER: 'AI 工程师',
  IT_MANAGER: 'IT 负责人',
  IT_REVIEWER: 'IT 审核专员',
  BIZ_USER: '业务用户',
  AI_AGENT: 'AI 智能体'
}

async function handleLogout() {
  await ElMessageBox.confirm('确认退出登录？', '提示', {
    confirmButtonText: '确认退出',
    cancelButtonText: '取消',
    type: 'warning'
  })
  try {
    await logout()
  } catch (_) {
    // 即使接口失败也清除本地状态
  }
  userStore.logout()
  router.push('/login')
  ElMessage.success('已退出登录')
}
</script>

<template>
  <el-container class="main-layout">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '64px' : '220px'" class="sidebar">
      <div class="sidebar-header">
        <img src="/favicon.svg" alt="logo" class="logo" v-if="!isCollapse" />
        <span v-if="!isCollapse" class="brand-name">芯智云匠</span>
      </div>

      <el-menu
        router
        :collapse="isCollapse"
        :collapse-transition="false"
        background-color="#1a1f36"
        text-color="#a0aec0"
        active-text-color="#63b3ed"
        default-active="/demo"
      >
        <el-menu-item index="/demo">
          <el-icon><MagicStick /></el-icon>
          <template #title>AI 能力演示</template>
        </el-menu-item>
        <el-menu-item index="/mes-qa">
          <el-icon><ChatDotRound /></el-icon>
          <template #title>MES 数据问答</template>
        </el-menu-item>
      </el-menu>

      <div class="sidebar-collapse" @click="isCollapse = !isCollapse">
        <el-icon>
          <component :is="isCollapse ? 'Expand' : 'Fold'" />
        </el-icon>
      </div>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <!-- 顶栏 -->
      <el-header class="header">
        <div class="header-right">
          <el-dropdown @command="handleLogout" trigger="click">
            <div class="user-info">
              <el-avatar size="small" :style="{ background: '#3b82f6' }">
                {{ userStore.username?.charAt(0)?.toUpperCase() }}
              </el-avatar>
              <span class="username">{{ userStore.username }}</span>
              <el-tag size="small" type="info" style="margin-left: 6px">
                {{ roleLabel[userStore.role] || userStore.role }}
              </el-tag>
              <el-icon style="margin-left: 4px; color: #6b7280"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout" icon="SwitchButton">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 页面内容 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.main-layout {
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  background: #1a1f36;
  display: flex;
  flex-direction: column;
  transition: width 0.2s;
  overflow: hidden;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-bottom: 1px solid #2d3748;
}

.logo {
  width: 28px;
  height: 28px;
  margin-right: 8px;
}

.brand-name {
  color: #e2e8f0;
  font-size: 16px;
  font-weight: 700;
  white-space: nowrap;
}

.el-menu {
  border-right: none;
  flex: 1;
}

.sidebar-collapse {
  padding: 12px 16px;
  cursor: pointer;
  color: #a0aec0;
  display: flex;
  align-items: center;
  border-top: 1px solid #2d3748;
}

.sidebar-collapse:hover {
  color: #63b3ed;
}

.header {
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 24px;
  height: 60px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}

.user-info:hover {
  background: #f3f4f6;
}

.username {
  margin-left: 8px;
  font-size: 14px;
  color: #374151;
}

.main-content {
  background: #f8fafc;
  overflow-y: auto;
  padding: 24px;
}
</style>
