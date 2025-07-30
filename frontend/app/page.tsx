/* C:\Users\mxz\Downloads\ai_systems_agent_starter\frontend\app\page.tsx */
import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold mb-4">
        AI Systems Engineering Agent
      </h1>

      <div className="space-x-4">
        <Link href="/login">
          <button className="px-4 py-2 bg-blue-600 text-white rounded">
            Login
          </button>
        </Link>

        <Link href="/signup">
          <button className="px-4 py-2 bg-green-600 text-white rounded">
            Sign&nbsp;Up
          </button>
        </Link>
      </div>
    </main>
  );
}
