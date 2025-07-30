import '@/globals.css';
import NavBar          from '@/app/components/NavBar';
import { Sidebar }     from '@/app/components/SideBar';
import { AuthProvider } from '@/app/_context/AuthContext';

export const metadata = { title: 'AI Systems Engineering Agent' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="flex h-screen flex-col">
        <AuthProvider>
          <NavBar />
          <div className="flex flex-1 overflow-hidden">
            <Sidebar />
            <section className="flex-1 overflow-y-auto">{children}</section>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
