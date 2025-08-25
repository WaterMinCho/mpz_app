import { useQuery } from "@tanstack/react-query";
import type { CommentWithReplies } from "@/types/posts";
import instance from "@/lib/axios-instance";

interface GetCommentsResponse {
  comments: CommentWithReplies[];
}

const getComments = async (postId: string): Promise<GetCommentsResponse> => {
  const response = await instance.get<GetCommentsResponse>(
    `/community/${postId}/comments`
  );
  return response.data;
};

export const useGetComments = (postId: string) => {
  return useQuery({
    queryKey: ["comments", postId],
    queryFn: () => getComments(postId),
    enabled: !!postId,
    staleTime: 3 * 60 * 1000, // 3분
    gcTime: 10 * 60 * 1000, // 10분
  });
};
