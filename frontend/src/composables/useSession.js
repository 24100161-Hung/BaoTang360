import { ref } from 'vue'

const SESSION_KEY = 'baotang_session_id'

export function useSession() {
  const sessionId = ref(getOrCreateSessionId())

  function getOrCreateSessionId() {
    let sid = localStorage.getItem(SESSION_KEY)
    if (!sid) {
      sid = 'sess-' + Date.now() + '-' + Math.random().toString(36).substring(2, 10)
      localStorage.setItem(SESSION_KEY, sid)
    }
    return sid
  }

  return { sessionId }
}
