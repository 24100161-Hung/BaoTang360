import { ref } from 'vue'

const TOKEN_KEY = 'baotang_admin_token'
const USER_KEY = 'baotang_admin_user'

const token = ref(localStorage.getItem(TOKEN_KEY))
const user = ref(JSON.parse(localStorage.getItem(USER_KEY) || 'null'))

export const authStore = {
  token,
  user,
  isAuthenticated: () => !!token.value,
  setAuth: (newToken, newUser) => {
    token.value = newToken
    user.value = newUser
    localStorage.setItem(TOKEN_KEY, newToken)
    localStorage.setItem(USER_KEY, JSON.stringify(newUser))
  },
  clear: () => {
    token.value = null
    user.value = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
  },
}
