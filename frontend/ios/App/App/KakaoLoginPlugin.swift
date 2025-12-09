import Foundation
import Capacitor
import KakaoSDKCommon
import KakaoSDKAuth
import KakaoSDKUser

@objc(KakaoLoginPlugin)
public class KakaoLoginPlugin: CAPPlugin {
    private var appKey: String?
    private var isInitialized = false

    @objc func initialize(_ call: CAPPluginCall) {
        let key = call.getString("appKey") ?? appKey ?? ""
        guard !key.isEmpty else {
            call.reject("Kakao appKey is missing.")
            return
        }
        KakaoSDK.initSDK(appKey: key)
        appKey = key
        isInitialized = true
        call.resolve()
    }

    private func ensureInitIfNeeded() -> Bool {
        if isInitialized { return true }
        guard let key = appKey else { return false }
        KakaoSDK.initSDK(appKey: key)
        isInitialized = true
        return true
    }

    @objc func login(_ call: CAPPluginCall) {
        guard ensureInitIfNeeded() else {
            call.reject("Kakao SDK not initialized. Call initialize(appKey) first.")
            return
        }

        let handleToken: (OAuthToken?, Error?) -> Void = { token, error in
            if let error = error {
                call.reject("Kakao login failed: \(error.localizedDescription)")
                return
            }
            guard let token = token else {
                call.reject("Kakao login failed: no token returned.")
                return
            }
            call.resolve([
                "accessToken": token.accessToken,
                "refreshToken": token.refreshToken ?? "",
                "idToken": token.idToken ?? ""
            ])
        }

        // 카카오톡 앱 우선, 미설치 시 계정 로그인
        if UserApi.isKakaoTalkLoginAvailable() {
            UserApi.shared.loginWithKakaoTalk(completion: handleToken)
        } else {
            UserApi.shared.loginWithKakaoAccount(completion: handleToken)
        }
    }

    @objc func logout(_ call: CAPPluginCall) {
        guard ensureInitIfNeeded() else {
            call.reject("Kakao SDK not initialized.")
            return
        }
        UserApi.shared.logout { error in
            if let error = error {
                call.reject("Kakao logout failed: \(error.localizedDescription)")
                return
            }
            call.resolve()
        }
    }

    @objc func unlink(_ call: CAPPluginCall) {
        guard ensureInitIfNeeded() else {
            call.reject("Kakao SDK not initialized.")
            return
        }
        UserApi.shared.unlink { error in
            if let error = error {
                call.reject("Kakao unlink failed: \(error.localizedDescription)")
                return
            }
            call.resolve()
        }
    }

    @objc func getUserInfo(_ call: CAPPluginCall) {
        guard ensureInitIfNeeded() else {
            call.reject("Kakao SDK not initialized.")
            return
        }
        UserApi.shared.me { user, error in
            if let error = error {
                call.reject("Kakao user info failed: \(error.localizedDescription)")
                return
            }
            guard let user = user else {
                call.reject("Kakao user info failed: no user returned.")
                return
            }
            call.resolve([
                "id": "\(user.id ?? 0)",
                "email": user.kakaoAccount?.email ?? "",
                "nickname": user.kakaoAccount?.profile?.nickname ?? "",
                "profileImageUrl": user.kakaoAccount?.profile?.profileImageUrl?.absoluteString ?? ""
            ])
        }
    }
}
