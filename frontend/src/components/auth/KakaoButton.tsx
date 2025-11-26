"use client";

import React, { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Capacitor } from "@capacitor/core";
import instance from "@/lib/axios-instance";
import { useAuth } from "@/components/providers/AuthProvider";
import { KakaoNativeLogin } from "@/lib/capacitor/kakao-login";

interface KakaoButtonProps {
  onClick?: () => void;
  href?: string;
  className?: string;
  children?: React.ReactNode;
}

export function KakaoButton({
  onClick,
  href,
  className = "",
  children = "카카오로 시작하기",
}: KakaoButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { setUserFromToken } = useAuth();

  const handleKakaoLogin = async () => {
    setIsLoading(true);
    const clientId = "e87b92ff4188fc038238a9a22eb0bf35";
    const isNative = Capacitor.isNativePlatform();

    try {
      if (isNative) {
        try {
          const { accessToken } = await KakaoNativeLogin.login();
          if (!accessToken) {
            throw new Error("네이티브 카카오 액세스 토큰을 가져오지 못했습니다.");
          }

          await instance.post("kakao/native/login", {
            access_token: accessToken,
          });
          await setUserFromToken();
          router.replace("/");
          return;
        } catch (nativeError) {
          console.error("네이티브 카카오 로그인 실패, 웹 플로우로 폴백:", nativeError);
        }
      }

      if (!clientId) {
        console.error("카카오 클라이언트 ID가 설정되지 않았습니다.");
        return;
      }

      const redirectUri = isNative
        ? "mpz://oauth/kakao/callback"
        : "https://api.mpz.kr/v1/kakao/login/callback";

      const state = crypto.randomUUID().replace(/-/g, "");
      const kakaoAuthUrl = `https://kauth.kakao.com/oauth/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(
        redirectUri
      )}&response_type=code&state=${state}`;

      console.log("카카오 인증 URL:", kakaoAuthUrl);
      console.log("플랫폼:", isNative ? "네이티브 앱" : "웹");

      window.location.href = kakaoAuthUrl;
    } catch (error) {
      console.error("카카오 로그인 시작 중 오류:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const buttonContent = (
    <>
      <Image src="/img/kakaoLogo.svg" alt="kakao logo" width={20} height={20} />
      {isLoading ? "로그인 중..." : children}
    </>
  );

  if (href) {
    return (
      <Link
        href={href}
        className={`flex items-center justify-center cursor-pointer gap-2 bg-[#FEE404] text-black text-base font-medium rounded-[10px] w-[80%] h-[48px] px-[14px] shadow transition ${className}`}
      >
        {buttonContent}
      </Link>
    );
  }

  return (
    <button
      type="button"
      onClick={onClick || handleKakaoLogin}
      disabled={isLoading}
      className={`flex items-center justify-center cursor-pointer gap-2 bg-[#FEE404] text-black text-base font-medium rounded-[10px] w-[80%] h-[48px] px-[14px] shadow transition disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
    >
      {buttonContent}
    </button>
  );
}
