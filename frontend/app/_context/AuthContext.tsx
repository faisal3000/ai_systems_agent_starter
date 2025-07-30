'use client';

import {
  createContext, useContext, useState, useEffect, ReactNode,
} from 'react';
import { api } from '@/lib/api';

export interface Me {
  id: number;
  email: string;
  is_admin: boolean;
  name?: string | null;
  company_name?: string | null;
}
interface AuthCtx {
  token: string | null;
  me: Me | null;
  isAdmin: boolean;
  saveAuth: (t: string, m?: Me) => void;
  signOut: () => void;
}
const Ctx = createContext<AuthCtx>({
  token: null, me: null, isAdmin: false, saveAuth() {}, signOut() {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(
    () => (typeof window !== 'undefined' ? localStorage.getItem('token') : null),
  );
  const [me, setMe] = useState<Me | null>(null);

  /* refresh /me once after page reload */
  useEffect(() => {
    if (!token || me) return;
    (async () => {
      try { setMe(await api('/me', token)); }
      catch { localStorage.removeItem('token'); setToken(null); }
    })();
  }, [token, me]);

  /* keep localStorage in sync */
  useEffect(() => {
    if (token) localStorage.setItem('token', token);
    else       localStorage.removeItem('token');
  }, [token]);

  function saveAuth(t: string, m?: Me) {
    setToken(t);
    if (m) setMe(m);
  }
  function signOut() { setToken(null); setMe(null); }

  return (
    <Ctx.Provider value={{ token, me, isAdmin: !!me?.is_admin, saveAuth, signOut }}>
      {children}
    </Ctx.Provider>
  );
}
export const useAuth = () => useContext(Ctx);
