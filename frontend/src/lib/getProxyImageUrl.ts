export function getProxyImageUrl(imageUrl?: string | null) {
  if (!imageUrl || imageUrl.trim() === "") return null;

  const trimmedUrl = imageUrl.trim();

  if (
    trimmedUrl.startsWith("/") ||
    trimmedUrl.startsWith("data:") ||
    trimmedUrl.startsWith("blob:") ||
    trimmedUrl.startsWith("/api/proxy-image")
  ) {
    return trimmedUrl;
  }

  // http/https 외 URL은 그대로 반환
  if (!/^https?:\/\//i.test(trimmedUrl)) {
    return trimmedUrl;
  }

  return `/api/proxy-image?url=${encodeURIComponent(trimmedUrl)}`;
}
