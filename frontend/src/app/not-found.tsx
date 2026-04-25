import Link from "next/link";

/**
 * 404 Not Found
 * - 길 잃은 강아지 SVG 일러스트
 * - 따뜻한 해요체 메시지
 */
export default function NotFoundPage() {
  return (
    <div className="max-w-[420px] mx-auto w-full min-h-screen flex flex-col items-center justify-center px-6 bg-wh">
      {/* 일러스트: 길 잃은 강아지 */}
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
          <ellipse cx="100" cy="165" rx="60" ry="8" fill="#e3e3e3" />

          {/* 몸통 */}
          <ellipse cx="100" cy="120" rx="38" ry="30" fill="#FFEBD2" />

          {/* 머리 */}
          <circle cx="100" cy="75" r="32" fill="#FFEBD2" />

          {/* 왼쪽 귀 (축 늘어진) */}
          <ellipse
            cx="72"
            cy="58"
            rx="12"
            ry="22"
            transform="rotate(-15 72 58)"
            fill="#E8C9A0"
          />

          {/* 오른쪽 귀 (축 늘어진) */}
          <ellipse
            cx="128"
            cy="58"
            rx="12"
            ry="22"
            transform="rotate(15 128 58)"
            fill="#E8C9A0"
          />

          {/* 왼쪽 눈 (슬픈 표정) */}
          <circle cx="88" cy="72" r="4" fill="#595959" />
          <ellipse cx="88" cy="66" rx="6" ry="2" fill="#FFEBD2" />

          {/* 오른쪽 눈 (슬픈 표정) */}
          <circle cx="112" cy="72" r="4" fill="#595959" />
          <ellipse cx="112" cy="66" rx="6" ry="2" fill="#FFEBD2" />

          {/* 눈썹 (걱정스런) */}
          <path
            d="M82 64 Q88 60 94 63"
            stroke="#595959"
            strokeWidth="1.5"
            fill="none"
            strokeLinecap="round"
          />
          <path
            d="M106 63 Q112 60 118 64"
            stroke="#595959"
            strokeWidth="1.5"
            fill="none"
            strokeLinecap="round"
          />

          {/* 코 */}
          <ellipse cx="100" cy="82" rx="5" ry="3.5" fill="#595959" />

          {/* 입 (살짝 풀린) */}
          <path
            d="M95 87 Q100 91 105 87"
            stroke="#595959"
            strokeWidth="1.5"
            fill="none"
            strokeLinecap="round"
          />

          {/* 앞발 */}
          <ellipse cx="82" cy="148" rx="10" ry="6" fill="#FFEBD2" />
          <ellipse cx="118" cy="148" rx="10" ry="6" fill="#FFEBD2" />

          {/* 꼬리 (축 처진) */}
          <path
            d="M138 115 Q155 118 148 130"
            stroke="#E8C9A0"
            strokeWidth="6"
            fill="none"
            strokeLinecap="round"
          />

          {/* 물음표 */}
          <text
            x="148"
            y="55"
            fontSize="28"
            fontWeight="bold"
            fill="#3E93FA"
            opacity="0.6"
          >
            ?
          </text>
          <text
            x="52"
            y="42"
            fontSize="20"
            fontWeight="bold"
            fill="#3E93FA"
            opacity="0.4"
          >
            ?
          </text>

          {/* 발자국 장식 */}
          <g opacity="0.15" fill="#8a8a8a">
            <circle cx="25" cy="140" r="3" />
            <circle cx="21" cy="135" r="2" />
            <circle cx="29" cy="135" r="2" />
            <circle cx="25" cy="132" r="2" />

            <circle cx="175" cy="130" r="3" />
            <circle cx="171" cy="125" r="2" />
            <circle cx="179" cy="125" r="2" />
            <circle cx="175" cy="122" r="2" />
          </g>
        </svg>
      </div>

      {/* 에러 코드 */}
      <p
        className="text-[64px] font-extrabold text-brand leading-none"
        style={{ letterSpacing: "-2px" }}
      >
        404
      </p>

      {/* 메시지 */}
      <div className="mt-3 text-center space-y-2">
        <h1 className="text-[18px] font-semibold text-bk">
          앗, 여기는 아무도 없어요
        </h1>
        <p className="text-[14px] text-gr leading-relaxed">
          찾으시는 페이지가 사라졌거나
          <br />
          주소가 잘못되었을 수 있어요.
        </p>
      </div>

      {/* CTA 버튼 */}
      <div className="mt-8 w-full space-y-3">
        <Link
          href="/"
          className="block w-full text-center bg-brand text-wh text-[15px] font-semibold py-3 rounded-full hover:bg-brand/90 transition-colors"
        >
          홈으로 돌아가기
        </Link>
        <Link
          href="/list/animal"
          className="block w-full text-center bg-bg text-dg text-[14px] font-medium py-3 rounded-full hover:bg-lg transition-colors"
        >
          입양 동물 보러가기
        </Link>
      </div>
    </div>
  );
}
