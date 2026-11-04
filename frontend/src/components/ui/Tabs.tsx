"use client";

import React from "react";

interface TabsProps {
  tabs: string[];
  activeTab: string;
  onTabChange: (tab: string) => void;
  className?: string;
}

export default function Tabs({ tabs, activeTab, onTabChange, className = "" }: TabsProps) {
  return (
    <div className={`flex gap-1 bg-slate-800/50 p-1 rounded-lg overflow-x-auto ${className}`}>
      {tabs.map((tab) => (
        <button
          key={tab}
          onClick={() => onTabChange(tab)}
          className={`px-4 py-2 text-sm font-medium rounded-md whitespace-nowrap transition-colors ${
            activeTab === tab
              ? "bg-blue-600 text-white"
              : "text-slate-400 hover:text-slate-200 hover:bg-slate-700"
          }`}
        >
          {tab}
        </button>
      ))}
    </div>
  );
}
