import { registerPlugin } from "@capacitor/core";

export interface KakaoNativeLoginResult {
  accessToken: string;
  refreshToken?: string;
  idToken?: string;
}

export interface KakaoNativeLoginPlugin {
  initialize(options: { appKey: string }): Promise<void>;
  login(): Promise<KakaoNativeLoginResult>;
  logout(): Promise<void>;
  unlink(): Promise<void>;
  getUserInfo(): Promise<{
    id: string;
    email?: string;
    nickname?: string;
    profileImageUrl?: string;
  }>;
}

export const KakaoNativeLogin =
  registerPlugin<KakaoNativeLoginPlugin>("KakaoLogin");
