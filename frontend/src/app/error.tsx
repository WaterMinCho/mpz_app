"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

/**
 * Error Boundary (route-level)
 * - 놀란 고양이 SVG 일러스트
 * - reset + 홈 이동 지원
 */
export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const router = useRouter();

  useEffect(() => {
    console.error("[ErrorBoundary]", error);
  }, [error]);

  return (
    <div className="max-w-[420px] mx-auto w-full min-h-screen flex flex-col items-center justify-center px-6 bg-wh">
      {/* 일러스트: 놀란 고양이 */}
      <div className="mb-8">
        <svg
          width="200"
          height="180"
          viewBox="0 0 200 180"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          {/* 바닥 그림자 */}
          <ellipse cx="100" cy="168" rx="55" ry="7" fill="#e3e3e3" />

          {/* 꼬리 (놀라서 곤두선) */}
          <path
            d="M140 130 Q165 100 155 65 Q152 55 148 60"
            stroke="#D4A574"
            strokeWidth="6"
            fill="none"
            strokeLinecap="round"
          />

          {/* 몸통 */}
          <ellipse cx="100" cy="125" rx="35" ry="32" fill="#FFE4C9" />

          {/* 머리 */}
          <circle cx="100" cy="78" r="30" fill="#FFE4C9" />

          {/* 왼쪽 귀 (삼각형, 곤두선) */}
          <path d="M78 58 L68 28 L90 50 Z" fill="#FFE4C9" />
          <path d="M80 54 L72 34 L88 50 Z" fill="#FFCFCF" />

          {/* 오른쪽 귀 (삼각형, 곤두선) */}
          <path d="M122 58 L132 28 L110 50 Z" fill="#FFE4C9" />
          <path d="M120 54 L128 34 L112 50 Z" fill="#FFCFCF" />

          {/* 왼쪽 눈 (놀라서 동그래진) */}
          <circle cx="88" cy="75" r="7" fill="#FFFFFF" stroke="#595959" strokeWidth="1.5" />
          <circle cx="88" cy="75" r="4" fill="#595959" />
          <circle cx="86" cy="73" r="1.5" fill="#FFFFFF" />

          {/* 오른쪽 눈 (놀라서 동그래진) */}
          <circle cx="112" cy="75" r="7" fill="#FFFFFF" stroke="#595959" strokeWidth="1.5" />
          <circle cx="112" cy="75" r="4" fill="#595959" />
          <circle cx="110" cy="73" r="1.5" fill="#FFFFFF" />

          {/* 코 */}
          <path d="M97 86 L100 89 L103 86 Z" fill="#FF9999" />

          {/* 입 (놀란 O) */}
          <ellipse cx="100" cy="93" rx="4" ry="3" fill="#595959" opacity="0.6" />

          {/* 수염 */}
          <line x1="70" y1="82" x2="85" y2="85" stroke="#D4A574" strokeWidth="1" />
          <line x1="68" y1="88" x2="84" y2="88" stroke="#D4A574" strokeWidth="1" />
          <line x1="115" y1="85" x2="130" y2="82" stroke="#D4A574" strokeWidth="1" />
          <line x1="116" y1="88" x2="132" y2="88" stroke="#D4A574" strokeWidth="1" />

          {/* 앞발 (당황해서 들어올린) */}
          <ellipse cx="80" cy="140" rx="10" ry="7" fill="#FFE4C9" />
          <ellipse cx="120" cy="140" rx="10" ry="7" fill="#FFE4C9" />

          {/* 놀란 효과 (번개) */}
          <g opacity="0.5">
            <path
              d="M42 45 L48 55 L44 55 L50 68"
              stroke="#FFC800"
              strokeWidth="2.5"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M155 40 L149 50 L153 50 L147 63"
              stroke="#FFC800"
              strokeWidth="2.5"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </g>

          {/* 느낌표 */}
          <text
            x="38"
            y="38"
            fontSize="22"
            fontWeight="bold"
            fill="#ff4f6f"
            opacity="0.5"
          >
            !
          </text>
          <text
            x="156"
            y="35"
            fontSize="18"
            fontWeight="bold"
            fill="#ff4f6f"
            opacity="0.4"
          >
            !
          </text>
        </svg>
      </div>

      {/* 에러 메시지 */}
      <p className="text-[14px] font-semibold text-error tracking-wide">
        OOPS!
      </p>

      <div className="mt-2 text-center space-y-2">
        <h1 className="text-[18px] font-semibold text-bk">
          앗, 문제가 생겼어요
        </h1>
        <p className="text-[14px] text-gr leading-relaxed">
          일시적인 오류가 발생했어요.
          <br />
          잠시 후 다시 시도해 주세요.
        </p>
      </div>

      {/* 에러 코드 (digest가 있을 때) */}
      {error.digest && (
        <p className="mt-3 text-[12px] text-lg font-mono">
          ref: {error.digest}
        </p>
      )}

      {/* CTA 버튼 */}
      <div className="mt-8 w-full space-y-3">
        <button
          onClick={() => reset()}
          className="block w-full text-center bg-brand text-wh text-[15px] font-semibold py-3 rounded-full hover:bg-brand/90 transition-colors cursor-pointer"
        >
          다시 시도하기
        </button>
        <button
          onClick={() => router.push("/")}
          className="block w-full text-center bg-bg text-dg text-[14px] font-medium py-3 rounded-full hover:bg-lg transition-colors cursor-pointer"
        >
          홈으로 돌아가기
        </button>
      </div>
    </div>
  );
}
