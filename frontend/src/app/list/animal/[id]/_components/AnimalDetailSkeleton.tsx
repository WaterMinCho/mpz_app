import { Container } from "@/components/common/Container";

export function AnimalDetailSkeleton() {
  return (
    <Container>
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white border-b border-lg">
          <div className="flex items-center justify-between px-4 py-3">
            <div className="w-8 h-8 bg-gray-200 rounded animate-pulse" />
            <div className="w-24 h-6 bg-gray-200 rounded animate-pulse" />
            <div className="w-8 h-8 bg-gray-200 rounded animate-pulse" />
          </div>
        </div>
        <div className="w-full bg-gray-200 h-80 animate-pulse" />
        <div className="px-4 py-6 space-y-4">
          <div className="w-3/4 h-6 bg-gray-200 rounded animate-pulse" />
          <div className="w-1/2 h-4 bg-gray-200 rounded animate-pulse" />
          <div className="w-full h-4 bg-gray-200 rounded animate-pulse" />
          <div className="w-2/3 h-4 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>
    </Container>
  );
}
