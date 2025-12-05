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

    // iOS 네이티브에서도 safe area를 사용하도록 data 속성만 추가
    // CSS 변수는 env(safe-area-inset-top)을 사용하므로 자동으로 노치 높이가 적용됨
    if (isIOS) {
      // html 요소에 data 속성 추가 (CSS 선택자용)
      document.documentElement.setAttribute("data-capacitor-platform", "ios");
    }

    const isAndroid = /Android/i.test(window.navigator.userAgent);
    const safeBottom = getComputedStyle(document.documentElement)
      .getPropertyValue("env(safe-area-inset-bottom)")
      ?.trim();
    const edgeToEdgeActive =
      isAndroid && safeBottom !== "" && safeBottom !== "0px";

    if (process.env.NODE_ENV !== "production") {
      console.info(
        "[SafeAreaLayout] Edge-to-edge:",
        edgeToEdgeActive ? "active" : "inactive",
        "iOS Native:",
        isIOS
      );
    }
  }, []);

  return (
    <div className="flex min-h-screen flex-col pt-safe-top">{children}</div>
  );
}
