package com.mpz.app;

import android.app.Activity;
import android.content.Context;

import androidx.annotation.Nullable;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.PluginMethod;
import com.kakao.sdk.auth.model.OAuthToken;
import com.kakao.sdk.common.model.ClientError;
import com.kakao.sdk.common.model.ClientErrorCause;
import com.kakao.sdk.user.UserApiClient;

import kotlin.Unit;
import kotlin.jvm.functions.Function2;

@CapacitorPlugin(name = "KakaoLogin")
public class KakaoLoginPlugin extends Plugin {

    @PluginMethod
    public void login(final PluginCall call) {
        Activity activity = getActivity();
        if (activity == null) {
            call.reject("활성 Activity를 가져올 수 없습니다.");
            return;
        }

        UserApiClient.getInstance()
                .loginWithKakaoTalk(activity, new Function2<OAuthToken, Throwable, Unit>() {
                    @Override
                    public Unit invoke(@Nullable OAuthToken oAuthToken, @Nullable Throwable throwable) {
                        if (throwable != null) {
                            return fallbackToAccountLogin(call, throwable);
                        }
                        if (oAuthToken == null) {
                            call.reject("카카오 로그인에 실패했습니다.");
                            return Unit.INSTANCE;
                        }
                        resolveWithToken(call, oAuthToken);
                        return Unit.INSTANCE;
                    }
                });
    }

    private Unit fallbackToAccountLogin(final PluginCall call, Throwable originalError) {
        if (originalError instanceof ClientError) {
            ClientError clientError = (ClientError) originalError;
            if (clientError.getReason() == ClientErrorCause.Cancelled) {
                call.reject("사용자가 카카오 로그인을 취소했습니다.");
                return Unit.INSTANCE;
            }
        }

        Context context = getContext();
        if (context == null) {
            call.reject("앱 컨텍스트를 가져올 수 없습니다.");
            return Unit.INSTANCE;
        }

        UserApiClient.getInstance()
                .loginWithKakaoAccount(context, new Function2<OAuthToken, Throwable, Unit>() {
                    @Override
                    public Unit invoke(@Nullable OAuthToken oAuthToken, @Nullable Throwable throwable) {
                        if (throwable != null) {
                            call.reject("카카오 계정 로그인을 완료할 수 없습니다.", throwable);
                            return Unit.INSTANCE;
                        }
                        if (oAuthToken == null) {
                            call.reject("카카오 계정 로그인에 실패했습니다.");
                            return Unit.INSTANCE;
                        }
                        resolveWithToken(call, oAuthToken);
                        return Unit.INSTANCE;
                    }
                });

        return Unit.INSTANCE;
    }

    private void resolveWithToken(PluginCall call, OAuthToken token) {
        JSObject result = new JSObject();
        result.put("accessToken", token.getAccessToken());
        if (token.getRefreshToken() != null) {
            result.put("refreshToken", token.getRefreshToken());
        }
        call.resolve(result);
    }
}

