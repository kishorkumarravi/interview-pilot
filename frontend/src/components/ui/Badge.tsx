import React from "react";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "default" | "easy" | "medium" | "hard" | "success" | "warning" | "info";
  className?: string;
}

export default function Badge({
  children,
  variant = "default",
  className = "",
}: BadgeProps) {
  const variants = {
    default: "bg-slate-700 text-slate-300",
    easy: "bg-green-900/50 text-green-400 border border-green-800",
    medium: "bg-yellow-900/50 text-yellow-400 border border-yellow-800",
    hard: "bg-red-900/50 text-red-400 border border-red-800",
    success: "bg-green-900/50 text-green-400",
    warning: "bg-yellow-900/50 text-yellow-400",
    info: "bg-blue-900/50 text-blue-400",
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${variants[variant]} ${className}`}
    >
      {children}
    </span>
  );
}
