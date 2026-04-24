import React from "react";

interface CenterCardSkeletonProps {
  className?: string;
}

export function CenterCardSkeleton({
  className = "",
}: CenterCardSkeletonProps) {
  return (
    <div
      className={`w-full flex items-center bg-wh rounded-xl border border-lg p-3 ${className}`}
    >
      <div className="w-[63px] h-[63px] rounded-md bg-gray-200 animate-pulse flex-shrink-0 mr-3" />
      <div className="flex-1 min-w-0">
        <div className="h-4 bg-gray-200 rounded animate-pulse w-1/2" />
        <div className="h-3 bg-gray-200 rounded animate-pulse w-1/3 mt-2" />
      </div>
      <div className="h-3 bg-gray-200 rounded animate-pulse w-14 ml-2" />
    </div>
  );
}
