package com.mpz.app;

import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.JSObject;
import com.kakao.sdk.user.UserApiClient;
import com.kakao.sdk.auth.model.OAuthToken;
import com.kakao.sdk.user.model.User;
import android.content.Context;
import android.util.Log;

@CapacitorPlugin(name = "KakaoLogin")
public class KakaoLoginPlugin extends Plugin {

    private static final String TAG = "KakaoLoginPlugin";

    @PluginMethod
    public void initialize(PluginCall call) {
        String appKey = call.getString("appKey");
        if (appKey != null) {
            Log.d(TAG, "Kakao SDK 초기화: " + appKey);
            call.resolve();
        } else {
            call.reject("appKey가 필요합니다.");
        }
    }

    @PluginMethod
    public void login(PluginCall call) {
        Log.d(TAG, "카카오 로그인 시작");
        
        UserApiClient.getInstance().loginWithKakaoAccount(getContext(), (OAuthToken token, Throwable error) -> {
            if (error != null) {
                Log.e(TAG, "카카오 로그인 실패", error);
                call.reject("카카오 계정 로그인을 완료할 수 없습니다: " + error.getMessage());
            } else if (token != null) {
                Log.d(TAG, "카카오 로그인 성공");
                JSObject ret = new JSObject();
                
                ret.put("accessToken", token.getAccessToken());
                if (token.getRefreshToken() != null) {
                    ret.put("refreshToken", token.getRefreshToken());
                }
                if (token.getIdToken() != null) {
                    ret.put("idToken", token.getIdToken());
                }
                
                call.resolve(ret);
            }
            return null;
        });
    }

    @PluginMethod
    public void logout(PluginCall call) {
        UserApiClient.getInstance().logout((Throwable error) -> {
            if (error != null) {
                Log.e(TAG, "카카오 로그아웃 실패", error);
                call.reject("로그아웃에 실패했습니다: " + error.getMessage());
            } else {
                Log.d(TAG, "카카오 로그아웃 성공");
                call.resolve();
            }
            return null;
        });
    }

    @PluginMethod
    public void unlink(PluginCall call) {
        UserApiClient.getInstance().unlink((Throwable error) -> {
            if (error != null) {
                Log.e(TAG, "카카오 회원탈퇴 실패", error);
                call.reject("회원탈퇴에 실패했습니다: " + error.getMessage());
            } else {
                Log.d(TAG, "카카오 회원탈퇴 성공");
                call.resolve();
            }
            return null;
        });
    }

    @PluginMethod
    public void getUserInfo(PluginCall call) {
        UserApiClient.getInstance().me((User user, Throwable error) -> {
            if (error != null) {
                Log.e(TAG, "사용자 정보 조회 실패", error);
                call.reject("사용자 정보를 가져올 수 없습니다: " + error.getMessage());
            } else if (user != null) {
                Log.d(TAG, "사용자 정보 조회 성공: " + user.getId());
                JSObject ret = new JSObject();
                ret.put("id", user.getId());
                
                if (user.getKakaoAccount() != null) {
                    ret.put("email", user.getKakaoAccount().getEmail());
                    
                    if (user.getKakaoAccount().getProfile() != null) {
                        ret.put("nickname", user.getKakaoAccount().getProfile().getNickname());
                        ret.put("profileImageUrl", user.getKakaoAccount().getProfile().getProfileImageUrl());
                    }
                }
                
                call.resolve(ret);
            }
            return null;
        });
    }

    @Override
    public Context getContext() {
        return bridge.getContext();
    }
}

