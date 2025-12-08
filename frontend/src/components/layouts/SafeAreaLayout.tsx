"use client";

import { ReactNode, useEffect } from "react";
import { Capacitor } from "@capacitor/core";

interface SafeAreaLayoutProps {
  children: ReactNode;
}

export function SafeAreaLayout({ children }: SafeAreaLayoutProps) {
  useEffect(() => {
    if (typeof window === "undefined") return;

    const isIOS = Capacitor.getPlatform() === "ios";
    const isAndroid = Capacitor.getPlatform() === "android";

    // iOS 네이티브에서도 safe area를 사용하도록 data 속성만 추가
    // CSS 변수는 env(safe-area-inset-top)을 사용하므로 자동으로 노치 높이가 적용됨
    if (isIOS) {
      // html 요소에 data 속성 추가 (CSS 선택자용)
      document.documentElement.setAttribute("data-capacitor-platform", "ios");
    }

    // Android의 경우 JavaScript로 전달된 safe area insets 사용
    if (isAndroid) {
      document.documentElement.setAttribute(
        "data-capacitor-platform",
        "android"
      );
    }
  }, []);

  return <div className="flex min-h-screen flex-col">{children}</div>;
}
