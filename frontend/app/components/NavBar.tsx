/* C:\Users\mxz\Downloads\ai_systems_agent_starter\frontend\app\components\NavBar.tsx */
"use client";

import { Menu, X } from "lucide-react";
import { useState } from "react";
import Link from "next/link";

export default function NavBar() {
  const [open, setOpen] = useState(false);
  return (
    <header className="flex items-center bg-white px-4 py-2 shadow">
      <button onClick={() => setOpen(!open)} className="md:hidden mr-2">
        {open ? <X /> : <Menu />}
      </button>
      <Link href="/consult" className="font-semibold text-lg">
        AI Systems Engineer
      </Link>
      <div className="flex-1" />
    </header>
  );
}
