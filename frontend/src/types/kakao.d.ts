declare global {
  interface Window {
    Kakao?: {
      init?: (key: string) => void;
      isInitialized?: () => boolean;
      Auth?: {
        logout: (callback?: () => void) => void;
        setAccessToken?: (token: string | null) => void;
      };
      Link?: {
        sendDefault: (options: {
          objectType: string;
          content: {
            title: string;
            description: string;
            imageUrl: string;
            link: {
              mobileWebUrl: string;
              webUrl: string;
            };
          };
          buttons: Array<{
            title: string;
            link: {
              mobileWebUrl: string;
              webUrl: string;
            };
          }>;
        }) => void;
      };
      Share?: {
        sendScrap: (options: { requestUrl: string }) => void;
      };
    };
  }
}

export {};
