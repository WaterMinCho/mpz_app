import { Banner } from "@/components/ui/Banner";
import Link from "next/link";

export function FooterSection() {
  return (
    <>
      <div className="px-4 pb-8">
        <Banner variant="sub" />
      </div>

      {/* Footer 섹션 */}
      <footer className="bg-bg pb-20 pt-6 px-4">
        {/* 로고 + 슬로건 */}
        <div className="flex items-center mb-4">
          <div className="flex items-center">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" className="text-brand mr-1.5">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="currentColor"/>
            </svg>
            <span className="text-[13px] font-bold text-dg">마펫쯔</span>
          </div>
          <span className="text-[10px] text-gr ml-2">모든 아이들에게 따뜻한 가족을</span>
        </div>

        {/* 빠른 링크 */}
        <div className="flex text-[11px] text-gr mb-4">
          <Link href="/list/animal" className="mr-4 hover:text-dg">입양 동물</Link>
          <Link href="/list/center" className="mr-4 hover:text-dg">보호센터</Link>
          <Link href="/community" className="mr-4 hover:text-dg">커뮤니티</Link>
          <Link href="/event/centers" className="hover:text-dg">이벤트</Link>
        </div>

        {/* 구분선 */}
        <div className="border-t border-lg mb-4" />

        {/* 사업자 정보 */}
        <div className="text-[10px] text-gr leading-[18px]">
          <p className="font-medium text-dg mb-1">(주)마이펫가디언즈</p>
          <p>사업자등록번호 246-81-03596 | 대표 유가희</p>
          <p>경기도 안산시 상록구 중보로 27, 401-1449호</p>
          <p className="mt-2 text-[9px]">© {new Date().getFullYear()} MyPetGuardians. All rights reserved.</p>
        </div>
      </footer>
    </>
  );
}
