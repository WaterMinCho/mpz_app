"use client";

import { Suspense } from "react";
import { useCenterFilterOverlayStore } from "@/stores/centerFilterOverlay";
import { CenterFilterContent } from "./CenterFilterContent";

export function CenterFilterOverlay() {
  const { isOpen, close } = useCenterFilterOverlayStore();
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[9998] bg-black/40">
      <div className="absolute inset-0" onClick={close} aria-label="닫기" />
      <div className="fixed inset-0 bg-white overflow-auto">
        <Suspense fallback={<div>로딩 중...</div>}>
          <CenterFilterContent />
        </Suspense>
      </div>
    </div>
  );
}
