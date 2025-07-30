'use client';

import { useState, FormEvent } from 'react';
import { api } from '../../lib/api';

export default function SignupPage() {
  const [form, setForm] = useState({
    email: '',
    password: '',
    name: '',
    company: '',
  });
  const [msg, setMsg] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  function upd<K extends keyof typeof form>(k: K, v: string) {
    setForm({ ...form, [k]: v });
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setMsg(null);

    try {
      /* POST  /auth/register  */
      await api('/auth/register', undefined, {
        method: 'POST',
        body: JSON.stringify({
          email:        form.email,
          password:     form.password,
          name:         form.name,
          company_name: form.company,
        }),
      });
      setMsg('✅ Registered – check e-mail for confirmation link.');
      setForm({ email: '', password: '', name: '', company: '' });
    } catch (err: any) {
      setMsg(`❌ ${err.message ?? 'Registration failed'}`);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto max-w-md space-y-6 p-8">
      <h1 className="text-2xl font-semibold">Sign up</h1>
      {msg && <p>{msg}</p>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          required type="email" placeholder="E-mail"
          className="input w-full"
          value={form.email} onChange={e => upd('email', e.target.value)}
        />
        <input
          required type="password" placeholder="Password"
          className="input w-full"
          value={form.password} onChange={e => upd('password', e.target.value)}
        />
        <input
          placeholder="Full name"
          className="input w-full"
          value={form.name} onChange={e => upd('name', e.target.value)}
        />
        <input
          placeholder="Company"
          className="input w-full"
          value={form.company} onChange={e => upd('company', e.target.value)}
        />

        <button disabled={busy} className="btn-primary w-full">
          {busy ? 'Registering…' : 'Register'}
        </button>
      </form>
      <p className="text-sm">
        Already have an account? <a href="/login" className="text-blue-600 underline">Log in</a>
      </p>
    </main>
  );
}
