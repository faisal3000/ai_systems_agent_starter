'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Layers, FileText, Workflow, Upload, Users, Settings } from 'lucide-react';
import { useAuth } from '@/app/_context/AuthContext';

const ALL = [
  { href: '/dashboard',           label: 'Dashboard',      icon: Layers   },
  { href: '/dashboard/consult',   label: 'Consult',        icon: FileText },
  { href: '/dashboard/deep-dive', label: 'Deep Dive',      icon: Workflow },
  { href: '/kb',                  label: 'Knowledge Base', icon: Upload   },
  { href: '/admin',               label: 'Admin',          icon: Users    },
  { href: '/account',             label: 'Account',        icon: Settings },
];

export function Sidebar() {
  const pathname         = usePathname();
  const { token, isAdmin, me } = useAuth();

  const NAV = ALL.filter(i =>
    i.href === '/admin'
      ? !!token && (isAdmin ?? true)
      : i.href === '/account'
      ? !!me && !isAdmin
      : true
  );

  const active =
    NAV.filter(n => pathname === n.href || pathname.startsWith(`${n.href}/`))
       .sort((a,b)=>b.href.length-a.href.length)[0]?.href;

  return (
    <aside className="hidden w-60 border-r bg-slate-900 text-slate-100 lg:block">
      <nav className="space-y-1 py-6">
        {NAV.map(({href,label,icon:Icon})=>(
          <Link key={href} href={href}
            className={`group flex items-center gap-3 px-6 py-2
              ${href===active?'bg-blue-700 font-medium':'text-slate-300 hover:bg-slate-800'}`}>
            <Icon size={16} className={href===active?'text-white':'text-blue-400'} />
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
