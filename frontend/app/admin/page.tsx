/* C:\Users\mxz\Downloads\ai_systems_agent_starter\frontend\app\admin\page.tsx */
"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Pending = { id: number; email: string };

export default function Admin() {
  const [pending, setPending] = useState<Pending[]>([]);

  async function load() {
    setPending(await api("/admin/pending"));
  }
  async function approve(id: number) {
    await api(`/admin/approve/${id}`, { method: "POST" });
    load();
  }

  useEffect(() => { load(); }, []);

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Pending Accounts</h1>
      <ul className="space-y-2">
        {pending.map((u) => (
          <li key={u.id} className="flex items-center gap-2">
            <span>{u.email}</span>
            <button
              onClick={() => approve(u.id)}
              className="bg-green-600 text-white px-2 py-1 rounded text-sm"
            >
              Approve
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
