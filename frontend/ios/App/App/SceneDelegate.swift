import UIKit
import KakaoSDKAuth

// MARK: - SceneDelegate for iOS 13+
// iOS 13 이상에서 Scene 기반 앱 라이프사이클을 사용하는 경우
// 카카오 개발자 문서: https://developers.kakao.com/docs/latest/ko/kakaologin/ios
//
// Scene 기반 앱에서도 카카오 로그인 URL 처리를 위해 필요합니다.
// AppDelegate의 application(_:open:options:)와 동일한 로직을 구현합니다.
@available(iOS 13.0, *)
class SceneDelegate: UIResponder, UIWindowSceneDelegate {

    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        // Scene이 연결될 때 호출
        guard let _ = (scene as? UIWindowScene) else { return }
    }

    func sceneDidDisconnect(_ scene: UIScene) {
        // Scene이 연결 해제될 때 호출
    }

    func sceneDidBecomeActive(_ scene: UIScene) {
        // Scene이 활성화될 때 호출
    }

    func sceneWillResignActive(_ scene: UIScene) {
        // Scene이 비활성화될 때 호출
    }

    func sceneWillEnterForeground(_ scene: UIScene) {
        // Scene이 포그라운드로 진입할 때 호출
    }

    func sceneDidEnterBackground(_ scene: UIScene) {
        // Scene이 백그라운드로 진입할 때 호출
    }

    // MARK: - URL Handling for Kakao Login (Scene-based)
    // Scene 기반 앱에서 카카오톡 앱에서 돌아올 때 호출
    // 
    // 카카오톡으로 로그인 시:
    // 1. UserApi.shared.loginWithKakaoTalk() 호출
    // 2. 카카오톡 앱이 열림
    // 3. 사용자가 동의하고 계속하기 선택
    // 4. kakao{NATIVE_APP_KEY}://oauth URL로 앱이 다시 열림
    // 5. 이 메서드가 호출되어 URL 처리
    //
    // AppDelegate의 application(_:open:options:)와 동일한 로직
    func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
        print("🔵 [SceneDelegate] URL 열기 요청 (Scene 기반)")
        
        guard let url = URLContexts.first?.url else {
            print("⚠️ [SceneDelegate] URL이 없습니다")
            return
        }
        
        print("🔵 [SceneDelegate] URL: \(url.absoluteString)")
        
        // 카카오 로그인 URL 처리
        if AuthApi.isKakaoTalkLoginUrl(url) {
            print("✅ [SceneDelegate] 카카오 로그인 URL 감지, AuthController로 전달")
            let handled = AuthController.handleOpenUrl(url: url)
            if handled {
                print("✅ [SceneDelegate] 카카오 로그인 URL 처리 완료")
            } else {
                print("⚠️ [SceneDelegate] 카카오 로그인 URL 처리 실패")
            }
        } else {
            print("ℹ️ [SceneDelegate] 카카오 로그인 URL이 아님")
        }
    }

    // MARK: - Universal Links Support (if enabled)
    // Universal Links를 사용하는 경우 처리
    // 카카오 로그인에서는 일반적으로 필요하지 않지만, 다른 기능에서 사용할 수 있음
    func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
        print("🔵 [SceneDelegate] Universal Link 처리: \(userActivity.activityType)")
        
        // Universal Links는 일반적으로 웹 기반 로그인에서 사용되므로
        // 네이티브 카카오 로그인에서는 필요하지 않을 수 있습니다.
        // 필요시 여기에 처리 로직 추가
    }
}