import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  badge?: React.ReactNode;
  onClick?: () => void;
  hover?: boolean;
}

export default function Card({
  children,
  className = "",
  title,
  badge,
  onClick,
  hover = false,
}: CardProps) {
  return (
    <div
      className={`bg-slate-800 border border-slate-700 rounded-xl p-6 ${
        hover ? "hover:border-blue-500/50 hover:bg-slate-800/80 cursor-pointer transition-all duration-200" : ""
      } ${onClick ? "cursor-pointer" : ""} ${className}`}
      onClick={onClick}
    >
      {(title || badge) && (
        <div className="flex items-center justify-between mb-4">
          {title && (
            <h3 className="text-lg font-semibold text-slate-100">{title}</h3>
          )}
          {badge}
        </div>
      )}
      {children}
    </div>
  );
}
