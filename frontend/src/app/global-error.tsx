"use client";

import { useEffect } from "react";

/**
 * Global Error Boundary
 * - 루트 레이아웃 에러까지 캐치 (자체 html/body 포함)
 * - 웅크린 강아지 + 고양이 SVG 일러스트
 */
export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("[GlobalError]", error);
  }, [error]);

  return (
    <html lang="ko">
      <body
        style={{
          margin: 0,
          fontFamily:
            '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          backgroundColor: "#ffffff",
        }}
      >
        <div
          style={{
            maxWidth: 420,
            margin: "0 auto",
            width: "100%",
            minHeight: "100vh",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            padding: "0 24px",
            boxSizing: "border-box",
          }}
        >
          {/* 일러스트: 웅크린 강아지 + 고양이 */}
          <div style={{ marginBottom: 32 }}>
            <svg
              width="220"
              height="180"
              viewBox="0 0 220 180"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              {/* 바닥 그림자 */}
              <ellipse cx="110" cy="165" rx="70" ry="8" fill="#e3e3e3" />

              {/* === 왼쪽: 웅크린 강아지 === */}
              {/* 몸통 (웅크린) */}
              <ellipse cx="75" cy="135" rx="30" ry="20" fill="#FFEBD2" />

              {/* 머리 */}
              <circle cx="75" cy="108" r="22" fill="#FFEBD2" />

              {/* 귀 */}
              <ellipse
                cx="57"
                cy="96"
                rx="8"
                ry="16"
                transform="rotate(-10 57 96)"
                fill="#E8C9A0"
              />
              <ellipse
                cx="93"
                cy="96"
                rx="8"
                ry="16"
                transform="rotate(10 93 96)"
                fill="#E8C9A0"
              />

              {/* 눈 (감은 상태) */}
              <path
                d="M66 107 Q69 110 72 107"
                stroke="#595959"
                strokeWidth="1.5"
                fill="none"
                strokeLinecap="round"
              />
              <path
                d="M78 107 Q81 110 84 107"
                stroke="#595959"
                strokeWidth="1.5"
                fill="none"
                strokeLinecap="round"
              />

              {/* 코 */}
              <ellipse cx="75" cy="115" rx="3.5" ry="2.5" fill="#595959" />

              {/* 앞발 (얼굴 가리는) */}
              <ellipse cx="62" cy="140" rx="10" ry="5" fill="#FFEBD2" />
              <ellipse cx="88" cy="140" rx="10" ry="5" fill="#FFEBD2" />

              {/* === 오른쪽: 걱정하는 고양이 === */}
              {/* 몸통 */}
              <ellipse cx="145" cy="133" rx="25" ry="22" fill="#E8E0D8" />

              {/* 머리 */}
              <circle cx="145" cy="105" r="20" fill="#E8E0D8" />

              {/* 귀 */}
              <path d="M132 92 L126 68 L140 86 Z" fill="#E8E0D8" />
              <path d="M134 88 L130 74 L139 86 Z" fill="#FFCFCF" />
              <path d="M158 92 L164 68 L150 86 Z" fill="#E8E0D8" />
              <path d="M156 88 L160 74 L151 86 Z" fill="#FFCFCF" />

              {/* 눈 (걱정스러운) */}
              <circle cx="138" cy="103" r="4" fill="#595959" />
              <circle cx="137" cy="101.5" r="1.2" fill="#FFFFFF" />
              <circle cx="152" cy="103" r="4" fill="#595959" />
              <circle cx="151" cy="101.5" r="1.2" fill="#FFFFFF" />

              {/* 눈썹 (걱정) */}
              <path
                d="M132 97 Q138 94 142 96"
                stroke="#595959"
                strokeWidth="1"
                fill="none"
                strokeLinecap="round"
              />
              <path
                d="M148 96 Q152 94 158 97"
                stroke="#595959"
                strokeWidth="1"
                fill="none"
                strokeLinecap="round"
              />

              {/* 코 */}
              <path d="M143 110 L145 112 L147 110 Z" fill="#FF9999" />

              {/* 입 */}
              <path
                d="M142 114 Q145 116 148 114"
                stroke="#595959"
                strokeWidth="1"
                fill="none"
                strokeLinecap="round"
              />

              {/* 수염 */}
              <line
                x1="122"
                y1="108"
                x2="134"
                y2="110"
                stroke="#C4B8AC"
                strokeWidth="0.8"
              />
              <line
                x1="123"
                y1="113"
                x2="134"
                y2="112"
                stroke="#C4B8AC"
                strokeWidth="0.8"
              />
              <line
                x1="156"
                y1="110"
                x2="168"
                y2="108"
                stroke="#C4B8AC"
                strokeWidth="0.8"
              />
              <line
                x1="156"
                y1="112"
                x2="167"
                y2="113"
                stroke="#C4B8AC"
                strokeWidth="0.8"
              />

              {/* 고양이 꼬리 (강아지 쪽으로 감싸는) */}
              <path
                d="M120 135 Q108 128 105 140"
                stroke="#C4B8AC"
                strokeWidth="4"
                fill="none"
                strokeLinecap="round"
              />

              {/* 고양이 앞발 (강아지 토닥이는) */}
              <ellipse cx="125" cy="128" rx="6" ry="4" fill="#E8E0D8" />

              {/* 하트 (둘 사이) */}
              <g opacity="0.35" transform="translate(108, 82) scale(0.6)">
                <path
                  d="M10 6 C10 2, 5 0, 5 4 C5 0, 0 2, 0 6 C0 10, 5 14, 5 14 C5 14, 10 10, 10 6Z"
                  fill="#ff4f6f"
                />
              </g>

              {/* 구름 장식 */}
              <g opacity="0.08" fill="#8a8a8a">
                <circle cx="30" cy="30" r="10" />
                <circle cx="42" cy="28" r="12" />
                <circle cx="55" cy="30" r="9" />

                <circle cx="170" cy="25" r="8" />
                <circle cx="180" cy="23" r="10" />
                <circle cx="190" cy="26" r="7" />
              </g>
            </svg>
          </div>

          {/* 에러 코드 */}
          <p
            style={{
              fontSize: 56,
              fontWeight: 800,
              color: "#ff4f6f",
              lineHeight: 1,
              letterSpacing: -2,
              margin: 0,
            }}
          >
            500
          </p>

          {/* 메시지 */}
          <div style={{ marginTop: 12, textAlign: "center" }}>
            <h1
              style={{
                fontSize: 18,
                fontWeight: 600,
                color: "#1c1c1c",
                margin: "0 0 8px 0",
              }}
            >
              서비스에 문제가 생겼어요
            </h1>
            <p
              style={{
                fontSize: 14,
                color: "#8a8a8a",
                lineHeight: 1.6,
                margin: 0,
              }}
            >
              지금은 페이지를 보여드리기 어려워요.
              <br />
              잠시 후 다시 방문해 주세요.
            </p>
          </div>

          {/* 에러 참조 */}
          {error.digest && (
            <p
              style={{
                marginTop: 12,
                fontSize: 12,
                color: "#e3e3e3",
                fontFamily: "monospace",
              }}
            >
              ref: {error.digest}
            </p>
          )}

          {/* CTA 버튼 */}
          <div style={{ marginTop: 32, width: "100%" }}>
            <button
              onClick={() => reset()}
              style={{
                display: "block",
                width: "100%",
                textAlign: "center",
                backgroundColor: "#3E93FA",
                color: "#ffffff",
                fontSize: 15,
                fontWeight: 600,
                padding: "12px 0",
                borderRadius: 9999,
                border: "none",
                cursor: "pointer",
                marginBottom: 12,
              }}
            >
              다시 시도하기
            </button>
            <button
              onClick={() => (window.location.href = "/")}
              style={{
                display: "block",
                width: "100%",
                textAlign: "center",
                backgroundColor: "#f7f7f7",
                color: "#595959",
                fontSize: 14,
                fontWeight: 500,
                padding: "12px 0",
                borderRadius: 9999,
                border: "none",
                cursor: "pointer",
              }}
            >
              홈으로 돌아가기
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}
