import { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "com.mpz.app",
  appName: "MPZ App",
  webDir: ".next",
  server: {
    url: "https://mpz.kr",
    cleartext: true, // TODO: 프로덕션 환경에서는 false로 변경
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 3000,
      launchAutoHide: true,
      backgroundColor: "#ffffffff",
      androidSplashResourceName: "splash",
      androidScaleType: "CENTER_CROP",
      androidSpinnerStyle: "large",
      iosSpinnerStyle: "small",
      webSpinnerStyle: "horizontal",
    },
    // KakaoLogin 네이티브 플러그인 등록
    KakaoLogin: {
      appKey: "30c65f4b266ed8e462b30c91518d174b",
    },
  },
};

export default config;
