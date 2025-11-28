import Foundation
import Capacitor
import KakaoSDKAuth
import KakaoSDKUser
import KakaoSDKCommon

@objc(KakaoLoginPlugin)
public class KakaoLoginPlugin: CAPPlugin {
    
    @objc func initialize(_ call: CAPPluginCall) {
        guard let appKey = call.getString("appKey") else {
            call.reject("appKey가 필요합니다.")
            return
        }
        
        KakaoSDK.init(appKey: appKey)
        call.resolve()
    }
    
    @objc func login(_ call: CAPPluginCall) {
        if AuthApi.hasToken() {
            UserApi.shared.accessTokenInfo { (_, error) in
                if let error = error {
                    if let sdkError = error as? SdkError, sdkError.isInvalidTokenError() == true {
                        // 토큰이 유효하지 않으면 재로그인
                        self.loginWithKakaoAccount(call: call)
                    } else {
                        call.reject("토큰 정보 조회 실패: \(error.localizedDescription)")
                    }
                } else {
                    // 토큰이 유효하면 기존 토큰 사용
                    self.getAccessToken(call: call)
                }
            }
        } else {
            // 토큰이 없으면 로그인
            loginWithKakaoAccount(call: call)
        }
    }
    
    private func loginWithKakaoAccount(call: CAPPluginCall) {
        if UserApi.isKakaoTalkLoginAvailable() {
            UserApi.shared.loginWithKakaoTalk { (oauthToken, error) in
                if let error = error {
                    call.reject("카카오톡 로그인 실패: \(error.localizedDescription)")
                } else if let oauthToken = oauthToken {
                    self.returnToken(call: call, token: oauthToken)
                }
            }
        } else {
            UserApi.shared.loginWithKakaoAccount { (oauthToken, error) in
                if let error = error {
                    call.reject("카카오 계정 로그인 실패: \(error.localizedDescription)")
                } else if let oauthToken = oauthToken {
                    self.returnToken(call: call, token: oauthToken)
                }
            }
        }
    }
    
    private func getAccessToken(call: CAPPluginCall) {
        if let token = AuthApi.shared.tokenManager.getToken() {
            returnToken(call: call, token: token)
        } else {
            call.reject("액세스 토큰을 가져올 수 없습니다.")
        }
    }
    
    private func returnToken(call: CAPPluginCall, token: OAuthToken) {
        var ret = JSObject()
        ret["accessToken"] = token.accessToken
        if let refreshToken = token.refreshToken {
            ret["refreshToken"] = refreshToken
        }
        if let idToken = token.idToken {
            ret["idToken"] = idToken
        }
        call.resolve(ret)
    }
    
    @objc func logout(_ call: CAPPluginCall) {
        UserApi.shared.logout { (error) in
            if let error = error {
                call.reject("로그아웃 실패: \(error.localizedDescription)")
            } else {
                call.resolve()
            }
        }
    }
    
    @objc func unlink(_ call: CAPPluginCall) {
        UserApi.shared.unlink { (error) in
            if let error = error {
                call.reject("회원탈퇴 실패: \(error.localizedDescription)")
            } else {
                call.resolve()
            }
        }
    }
    
    @objc func getUserInfo(_ call: CAPPluginCall) {
        UserApi.shared.me { (user, error) in
            if let error = error {
                call.reject("사용자 정보 조회 실패: \(error.localizedDescription)")
            } else if let user = user {
                var ret = JSObject()
                ret["id"] = String(user.id)
                
                if let kakaoAccount = user.kakaoAccount {
                    ret["email"] = kakaoAccount.email
                    
                    if let profile = kakaoAccount.profile {
                        ret["nickname"] = profile.nickname
                        ret["profileImageUrl"] = profile.profileImageUrl?.absoluteString
                    }
                }
                
                call.resolve(ret)
            }
        }
    }
}

