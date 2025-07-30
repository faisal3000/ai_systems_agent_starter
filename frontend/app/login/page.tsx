'use client';

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '../../lib/api';          // stays the same
import { useAuth } from '../_context/AuthContext';

export default function LoginPage() {
  const router        = useRouter();
  const { saveAuth }  = useAuth();

  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');
  const [busy, setBusy]         = useState(false);
  const [error, setError]       = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);

    try {
      /* --------------------------------------------------------
         Send as  x-www-form-urlencoded:  username=…&password=…
         -------------------------------------------------------- */
      const body = new URLSearchParams({
        username: email,
        password,
      });

      const { access_token } = await api<{ access_token: string }>(
        '/auth/login',
        undefined,
        {
          method: 'POST',
          body,
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        },
      );

      /* 2️⃣  Fetch profile */
      const me = await api('/me', access_token);

      /* 3️⃣  Persist + route */
      saveAuth(access_token, me);
      router.replace(me.is_admin ? '/admin' : '/dashboard');
    } catch (err: any) {
      setError(err.message ?? 'Login failed');
    } finally {
      setBusy(false);
    }
  }

  /* ---------------- UI --------------- */
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg"
      >
        <h1 className="mb-6 text-center text-2xl font-semibold">Sign in</h1>

        <input
          required type="email" placeholder="E-mail"
          className="input w-full mb-4"
          value={email} onChange={e => setEmail(e.target.value)}
        />

        <input
          required type="password" placeholder="Password"
          className="input w-full mb-6"
          value={password} onChange={e => setPassword(e.target.value)}
        />

        {error && (
          <p className="mb-4 rounded bg-red-100 px-3 py-2 text-sm text-red-700">
            {error}
          </p>
        )}

        <button
          disabled={busy}
          className="btn-primary w-full"
        >
          {busy ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
    </main>
  );
}
