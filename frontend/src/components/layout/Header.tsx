"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { LogOut, User } from "lucide-react";
import { clearToken, getUserName } from "@/lib/api";

export default function Header() {
  const router = useRouter();
  const name = getUserName();

  const handleLogout = () => {
    clearToken();
    router.push("/login");
  };

  return (
    <header className="h-16 bg-slate-900/80 backdrop-blur-sm border-b border-slate-800 flex items-center justify-between px-6 lg:px-8">
      <div className="lg:hidden w-10" />
      <div className="flex-1" />
      <div className="flex items-center gap-3">
        {name && (
          <div className="flex items-center gap-2 text-sm text-slate-300">
            <div className="w-7 h-7 rounded-full bg-blue-600/30 border border-blue-500/30 flex items-center justify-center">
              <User className="w-3.5 h-3.5 text-blue-400" />
            </div>
            <span className="hidden sm:inline">{name}</span>
          </div>
        )}
        <button
          onClick={handleLogout}
          className="flex items-center gap-2 px-3 py-2 text-sm text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
        >
          <LogOut className="w-4 h-4" />
          <span className="hidden sm:inline">Logout</span>
        </button>
      </div>
    </header>
  );
}
