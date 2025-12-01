package com.mpz.app;

import android.graphics.Color;
import android.os.Bundle;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;
import java.util.concurrent.atomic.AtomicBoolean;

public class MainActivity extends BridgeActivity {
    private Runnable lightInsetsRunnable;
    private final AtomicBoolean safeAreaInsetsInitialized = new AtomicBoolean(false);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        registerPlugin(KakaoLoginPlugin.class);
        super.onCreate(savedInstanceState);

        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        getWindow().setStatusBarColor(Color.TRANSPARENT);
        getWindow().setNavigationBarColor(Color.TRANSPARENT);

        lightInsetsRunnable = () -> {
            WindowInsetsControllerCompat insetsController =
                WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
            if (insetsController != null) {
                insetsController.setAppearanceLightStatusBars(true);
                insetsController.setAppearanceLightNavigationBars(true);
            }
        };

        renderSafeAreaInsetsIfInitialized();
    }

    private void renderSafeAreaInsetsIfInitialized() {
        if (!safeAreaInsetsInitialized.get() || lightInsetsRunnable == null) {
            return;
        }

        runOnUiThread(() -> {
            lightInsetsRunnable.run();
            getWindow().getDecorView().post(lightInsetsRunnable);
        });
    }

    // 플러그인에서 안전 영역 값이 준비되면 호출
    public void notifySafeAreaInsetsInitialized() {
        safeAreaInsetsInitialized.set(true);
        renderSafeAreaInsetsIfInitialized();
    }
}
