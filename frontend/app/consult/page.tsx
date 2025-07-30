/* C:\Users\mxz\Downloads\ai_systems_agent_starter\frontend\app\consult\page.tsx */
"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export default function Consult() {
  const [prompt, setPrompt] = useState("");
  const [answer, setAnswer] = useState("");

  async function ask() {
    setAnswer("Thinking…");
    const res = await api<{ reply: string }>("/consult", {
      method: "POST",
      body: JSON.stringify({ prompt, model: "gpt-4o-mini" }),
    });
    setAnswer(res.reply);
  }

  return (
    <div className="space-y-4 max-w-3xl">
      <h1 className="text-2xl font-semibold">Consult the Agent</h1>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows={4}
        className="w-full p-2 border rounded"
      />
      <button onClick={ask} className="bg-blue-600 text-white px-4 py-2 rounded">
        Ask
      </button>
      {answer && (
        <pre className="whitespace-pre-wrap bg-gray-100 p-3 rounded">{answer}</pre>
      )}
    </div>
  );
}
