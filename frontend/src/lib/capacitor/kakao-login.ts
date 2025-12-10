import { KakaoLoginPlugin } from "@kichunsung/capacitor-kakao-login-plugin";

/**
 * 기존 커스텀 플러그인(KakaoLogin) 사용 코드를
 * @kichunsung/capacitor-kakao-login-plugin 기반으로 래핑한다.
 * 기존 인터페이스(초기화/로그인/로그아웃/유저 조회)를 최대한 유지해
 * 앱 코드 변경을 최소화한다.
 */
export const KakaoNativeLogin = {
  // 플러그인 자체에서 별도 초기화가 필요하지 않으므로 noop 처리
  // (web fallback용 initForWeb이 있으나 네이티브에서는 불필요)
  async initialize({ appKey }: { appKey: string }) {
    void appKey;
    return;
  },

  async login() {
    const res = await KakaoLoginPlugin.goLogin();
    return {
      accessToken: res.accessToken,
      refreshToken: res.refreshToken,
      idToken: res.idToken,
    };
  },

  async logout() {
    await KakaoLoginPlugin.goLogout();
  },

  // 패키지에 unlink가 없어 logout으로 대체
  async unlink() {
    await KakaoLoginPlugin.goLogout();
  },

  async getUserInfo() {
    const res = await KakaoLoginPlugin.getUserInfo();
    const user = res?.value ?? {};
    return {
      id: String(user.id ?? ""),
      email: user.kakao_account?.email ?? "",
      nickname: user.kakao_account?.profile?.nickname ?? "",
      profileImageUrl: user.kakao_account?.profile?.profile_image_url ?? "",
    };
  },
};
