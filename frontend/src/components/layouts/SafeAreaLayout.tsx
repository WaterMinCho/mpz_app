"use client";

import { ReactNode, useEffect, useState, useCallback } from "react";
import { Capacitor } from "@capacitor/core";

interface SafeAreaLayoutProps {
  children: ReactNode;
}

export function SafeAreaLayout({ children }: SafeAreaLayoutProps) {
  const [safeAreaTop, setSafeAreaTop] = useState(0);
  const [safeAreaBottom, setSafeAreaBottom] = useState(0);
  // 고정 하단 네비게이션 높이 (px)
  const NAV_HEIGHT = 64;

  const clampValue = useCallback((value: number, max = 60) => {
    if (Number.isNaN(value)) return 0;
    return Math.min(Math.max(value, 0), max);
  }, []);

  // Safe area 값을 가져오는 함수
  const updateSafeAreaValues = useCallback(() => {
    if (typeof window === "undefined") return;

    const isAndroid = Capacitor.getPlatform() === "android";
    const isIOS = Capacitor.getPlatform() === "ios";

    if (isAndroid) {
      // Android: CSS 변수에서 값 가져오기
      const top = getComputedStyle(document.documentElement)
        .getPropertyValue("--safe-area-top")
        ?.trim();
      const bottom = getComputedStyle(document.documentElement)
        .getPropertyValue("--safe-area-bottom")
        ?.trim();

      if (top && top !== "0px" && top !== "") {
        const topValue = clampValue(parseFloat(top));
        setSafeAreaTop((prev) => {
          // 값이 실제로 변경된 경우에만 업데이트
          if (Math.abs(prev - topValue) > 1) {
            return topValue;
          }
          return prev;
        });
      }

      if (bottom && bottom !== "0px" && bottom !== "") {
        const bottomValue = clampValue(parseFloat(bottom), 50);
        setSafeAreaBottom((prev) => {
          if (Math.abs(prev - bottomValue) > 1) {
            return bottomValue;
          }
          return prev;
        });
      }
    } else if (isIOS) {
      // iOS: env() 값 사용
      const top = getComputedStyle(document.documentElement)
        .getPropertyValue("env(safe-area-inset-top)")
        ?.trim();
      const bottom = getComputedStyle(document.documentElement)
        .getPropertyValue("env(safe-area-inset-bottom)")
        ?.trim();

      if (top && top !== "0px" && top !== "") {
        const topValue = clampValue(parseFloat(top));
        setSafeAreaTop((prev) => {
          if (Math.abs(prev - topValue) > 1) {
            return topValue;
          }
          return prev;
        });
      }

      if (bottom && bottom !== "0px" && bottom !== "") {
        const bottomValue = clampValue(parseFloat(bottom), 50);
        setSafeAreaBottom((prev) => {
          if (Math.abs(prev - bottomValue) > 1) {
            return bottomValue;
          }
          return prev;
        });
      }
    }
  }, [clampValue]);

  useEffect(() => {
    if (typeof window === "undefined") return;

    const isIOS = Capacitor.getPlatform() === "ios";
    const isAndroid = Capacitor.getPlatform() === "android";

    // 플랫폼 식별 data-attr만 설정
    if (isIOS) {
      document.documentElement.setAttribute("data-capacitor-platform", "ios");
    }
    if (isAndroid) {
      document.documentElement.setAttribute(
        "data-capacitor-platform",
        "android"
      );
    }

    // 초기 1회만 계산
    updateSafeAreaValues();

    // 안드로이드에서 네이티브가 이벤트로 보내줄 경우만 반영
    const handleSafeAreaChange = (event: CustomEvent) => {
      const { top, bottom } = event.detail;
      if (top !== undefined && top >= 0) {
        const clampedTop = clampValue(top);
        setSafeAreaTop((prev) => {
          if (Math.abs(prev - clampedTop) > 1) {
            return clampedTop;
          }
          return prev;
        });
      }
      if (bottom !== undefined && bottom >= 0) {
        const clampedBottom = clampValue(bottom, 50);
        setSafeAreaBottom((prev) => {
          if (Math.abs(prev - clampedBottom) > 1) {
            return clampedBottom;
          }
          return prev;
        });
      }
    };

    window.addEventListener(
      "safeAreaInsetsChanged",
      handleSafeAreaChange as EventListener
    );

    return () => {
      window.removeEventListener(
        "safeAreaInsetsChanged",
        handleSafeAreaChange as EventListener
      );
    };
  }, [updateSafeAreaValues, clampValue]);

  // 비정상적으로 큰 값 방지 (100px 이상이면 0으로 처리)
  const normalizedSafeAreaTop = safeAreaTop > 100 ? 0 : safeAreaTop;
  const normalizedSafeAreaBottom = safeAreaBottom > 100 ? 0 : safeAreaBottom;

  // CSS env() 값을 직접 사용 (더 안정적)
  const safeAreaTopStyle =
    normalizedSafeAreaTop > 0
      ? `${normalizedSafeAreaTop}px`
      : "env(safe-area-inset-top, 0px)";
  const safeAreaBottomStyle =
    normalizedSafeAreaBottom > 0
      ? `${normalizedSafeAreaBottom}px`
      : "env(safe-area-inset-bottom, 0px)";
  const combinedBottomPadding = `calc(${safeAreaBottomStyle} + ${NAV_HEIGHT}px)`;

  return (
    <div
      className="flex min-h-screen flex-col bg-wh"
      style={{
        paddingTop: safeAreaTopStyle,
        // 네비게이션 높이 + safe-area bottom 합산
        paddingBottom: combinedBottomPadding,
      }}
    >
      {children}
    </div>
  );
}
