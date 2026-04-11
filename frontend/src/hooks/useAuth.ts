import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import type { User } from '../types'
import { login as apiLogin, getMe } from '../services/api'

interface AuthCtx {
  user: User | null
  token: string | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

export const AuthContext = createContext<AuthCtx>({
  user: null,
  token: null,
  loading: true,
  login: async () => {},
  logout: () => {},
})

export function useAuthProvider() {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!token) { setLoading(false); return }
    getMe()
      .then((res) => setUser(res.data))
      .catch(() => { localStorage.removeItem('token'); setToken(null) })
      .finally(() => setLoading(false))
  }, [token])

  const login = useCallback(async (email: string, password: string) => {
    const res = await apiLogin(email, password)
    const t = res.data.access_token
    localStorage.setItem('token', t)
    setToken(t)
    const me = await getMe()
    setUser(me.data)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }, [])

  return { user, token, loading, login, logout }
}

export const useAuth = () => useContext(AuthContext)
