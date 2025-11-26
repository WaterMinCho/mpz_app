import React from "react";

interface CommunityCardSkeletonProps {
  className?: string;
}

export function CommunityCardSkeleton({
  className = "",
}: CommunityCardSkeletonProps) {
  return (
    <div className={`max-w-[420px] border-b border-bg pb-6 ${className}`}>
      {/* 프로필 정보 스켈레톤 */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {/* 프로필 이미지 스켈레톤 (md: w-6 h-6) */}
          <div className="w-6 h-6 bg-gray-200 rounded-full animate-pulse flex-shrink-0" />
          {/* 사용자 이름 스켈레톤 */}
          <div className="w-20 h-4 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>

      {/* 갤러리 스켈레톤 (100x100 이미지들) */}
      <div className="flex gap-1 mb-3 overflow-x-auto scrollbar-hide">
        <div className="w-[100px] h-[100px] bg-gray-200 rounded-sm animate-pulse flex-shrink-0" />
        <div className="w-[100px] h-[100px] bg-gray-200 rounded-sm animate-pulse flex-shrink-0" />
        <div className="w-[100px] h-[100px] bg-gray-200 rounded-sm animate-pulse flex-shrink-0" />
      </div>

      {/* 제목 스켈레톤 */}
      <div className="mb-2">
        <div className="w-3/4 h-5 bg-gray-200 rounded animate-pulse" />
      </div>

      {/* 내용 스켈레톤 (line-clamp-3) */}
      <div className="mb-2">
        <div className="w-full h-4 bg-gray-200 rounded animate-pulse mb-1" />
        <div className="w-full h-4 bg-gray-200 rounded animate-pulse mb-1" />
        <div className="w-2/3 h-4 bg-gray-200 rounded animate-pulse" />
      </div>

      {/* 하단 상호작용 영역 스켈레톤 */}
      <div className="flex items-center justify-between gap-6 mt-2">
        <div className="flex items-center gap-2">
          {/* 좋아요 버튼 스켈레톤 */}
          <div className="flex items-center gap-1">
            <div className="w-5 h-5 bg-gray-200 rounded animate-pulse" />
            <div className="w-6 h-4 bg-gray-200 rounded animate-pulse" />
          </div>
          {/* 댓글 버튼 스켈레톤 */}
          <div className="flex items-center gap-1">
            <div className="w-5 h-5 bg-gray-200 rounded animate-pulse" />
            <div className="w-6 h-4 bg-gray-200 rounded animate-pulse" />
          </div>
        </div>
        {/* 날짜 스켈레톤 */}
        <div className="w-16 h-4 bg-gray-200 rounded animate-pulse" />
      </div>
    </div>
  );
}
