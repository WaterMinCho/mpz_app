"use client";
import Script from "next/script";

let loaded = false;

export default function KakaoMapScript() {
  return (
    <Script
      src={`//dapi.kakao.com/v2/maps/sdk.js?appkey=${
        process.env.NEXT_PUBLIC_KAKAO_MAP_KEY || "YOUR_JAVASCRIPT_KEY_HERE"
      }&libraries=services&autoload=false`}
      strategy="afterInteractive"
      onLoad={() => {
        console.log("Kakao 스크립트 로드됨");
        if (window.kakao?.maps?.load && !loaded) {
          window.kakao.maps.load(() => {
            loaded = true;
          });
        }
      }}
    />
  );
}
