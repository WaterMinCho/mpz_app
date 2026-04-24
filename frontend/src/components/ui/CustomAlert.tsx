"use client";

import React, { useEffect } from "react";
import { createPortal } from "react-dom";
import { X } from "@phosphor-icons/react";
import { cn } from "@/lib/utils";
import { BigButton } from "./BigButton";
import { IconButton } from "./IconButton";

interface CustomAlertProps {
  open: boolean;
  onClose: () => void;
  /** "center": 화면 중앙 다이얼로그 | "bottom": 하단 바텀시트 */
  variant?: "center" | "bottom";
  title?: string;
  description?: string;
  /** 확인 버튼 텍스트 (미지정 시 버튼 숨김) */
  confirmText?: string;
  /** 취소 버튼 텍스트 (미지정 시 버튼 숨김) */
  cancelText?: string;
  onConfirm?: () => void;
  onCancel?: () => void;
  /** 오버레이 클릭으로 닫기 허용 (기본 true) */
  dismissible?: boolean;
  /** X 닫기 버튼 표시 (기본 true) */
  showClose?: boolean;
  /** 커스텀 컨텐츠 */
  children?: React.ReactNode;
  className?: string;
}

export function CustomAlert({
  open,
  onClose,
  variant = "center",
  title,
  description,
  confirmText,
  cancelText,
  onConfirm,
  onCancel,
  dismissible = true,
  showClose = true,
  children,
  className,
}: CustomAlertProps) {
  // 열릴 때 스크롤 잠금
  useEffect(() => {
    if (!open) return;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  if (!open) return null;

  const handleOverlayClick = () => {
    if (dismissible) onClose();
  };

  const handleCancel = () => {
    onCancel?.();
    onClose();
  };

  const handleConfirm = () => {
    onConfirm?.();
    onClose();
  };

  const hasButtons = confirmText || cancelText;

  const content = (
    <div
      className={cn(
        "fixed inset-0 z-[9999] transition-all",
        variant === "center"
          ? "flex items-center justify-center"
          : "flex items-end justify-center",
      )}
    >
      {/* 오버레이 */}
      <div
        className="absolute inset-0 bg-black/40"
        onClick={handleOverlayClick}
      />

      {/* 패널 */}
      <div
        className={cn(
          "relative bg-white shadow-xl",
          variant === "center"
            ? "w-full max-w-[298px] rounded-2xl animate-in fade-in-0 zoom-in-95 duration-200"
            : "w-full max-w-[420px] rounded-t-2xl animate-slideup",
          className,
        )}
        style={
          variant === "bottom"
            ? {
                paddingBottom: "calc(env(safe-area-inset-bottom, 0px) + 16px)",
              }
            : undefined
        }
      >
        {/* 바텀시트 핸들 */}
        {variant === "bottom" && (
          <div className="absolute top-2 left-1/2 -translate-x-1/2 w-12 h-1.5 bg-gray-200 rounded-full" />
        )}

        <div className="py-4 px-5">
          {/* 헤더 */}
          {(title || showClose) && (
            <div className="flex items-center justify-between mb-2.5">
              {title && <h2 className="text-bk">{title}</h2>}
              {showClose && (
                <IconButton
                  icon={({ size }) => <X size={size} weight="bold" />}
                  size="iconS"
                  onClick={onClose}
                  className="text-gray-400 hover:text-gray-600"
                />
              )}
            </div>
          )}

          {/* 텍스트 */}
          {description && (
            <p className="text-sm text-dg mb-4 whitespace-pre-line">
              {description}
            </p>
          )}

          {/* 커스텀 컨텐츠 */}
          {children && <div className="mb-4">{children}</div>}

          {/* 버튼 */}
          {hasButtons && (
            <div className="flex gap-3">
              {cancelText && (
                <BigButton
                  variant="variant3"
                  onClick={handleCancel}
                  className="bg-bg text-dg flex-1 hover:bg-gray-50"
                >
                  {cancelText}
                </BigButton>
              )}
              {confirmText && (
                <BigButton
                  variant="primary"
                  onClick={handleConfirm}
                  className="flex-1"
                >
                  {confirmText}
                </BigButton>
              )}
            </div>
          )}
        </div>
      </div>

      {variant === "bottom" && (
        <style jsx global>{`
          @keyframes slideup {
            0% {
              transform: translateY(100%);
            }
            100% {
              transform: translateY(0%);
            }
          }
          .animate-slideup {
            animation: slideup 0.25s cubic-bezier(0.4, 0, 0.2, 1);
          }
        `}</style>
      )}
    </div>
  );

  return createPortal(content, document.body);
}
