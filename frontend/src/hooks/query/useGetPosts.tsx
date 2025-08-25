import { useQuery } from "@tanstack/react-query";
import type {
  GetPostsResponse,
  GetPostsParams,
  PostDetailResponse,
  Post,
} from "@/types/posts";
import instance from "@/lib/axios-instance";

// 실제 API 응답 타입
interface ApiPostResponse {
  id: string;
  title: string;
  content: string;
  userId: string;
  animalId?: string | null;
  adoptionsId?: string | null;
  contentTags?: string | null;
  visibility?: "public" | "center";
  createdAt: string;
  updatedAt: string;
  userNickname: string;
  userImage?: string | null;
  tags?: Array<{
    id: string;
    postId: string;
    tagName: string;
    createdAt: string;
  }>;
  images?: Array<{
    id: string;
    postId: string;
    imageUrl: string;
    orderIndex: number;
    createdAt: string;
  }>;
  postLikes?: Array<{
    id: string;
    postId: string;
    userId: string;
    createdAt: string;
  }>;
  comments?: Array<{
    id: string;
    postId: string;
    userId: string;
    content: string;
    createdAt: string;
    updatedAt: string;
  }>;
}

interface ApiPostsResponse {
  posts: ApiPostResponse[];
}

const getPosts = async (params?: GetPostsParams): Promise<GetPostsResponse> => {
  const searchParams = new URLSearchParams();

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, value.toString());
      }
    });
  }

  const url = `/posts?${searchParams.toString()}`;
  const response = await instance.get<ApiPostsResponse>(url);

  // API 응답을 Post 타입으로 변환
  const transformedPosts: Post[] = response.data.posts.map(
    (post: ApiPostResponse) => ({
      id: post.id,
      title: post.title,
      content: post.content,
      userId: post.userId,
      animalId: post.animalId || null,
      adoptionsId: post.adoptionsId || null,
      contentTags: post.contentTags || null,
      visibility: post.visibility || "public",
      createdAt: post.createdAt,
      updatedAt: post.updatedAt,
      userNickname: post.userNickname,
      userImage: post.userImage || null,
      tags: post.tags || [],
      images: post.images || [],
      postLikes: post.postLikes || [],
      comments: [], // 빈 배열로 설정하여 타입 호환성 문제 해결
    })
  );

  return {
    posts: transformedPosts,
  };
};

const getPostDetail = async (postId: string): Promise<PostDetailResponse> => {
  const response = await instance.get<PostDetailResponse>(`/posts/${postId}`);
  return response.data;
};

export const useGetPosts = (params?: GetPostsParams) => {
  return useQuery({
    queryKey: ["posts", params],
    queryFn: () => getPosts(params),
    staleTime: 3 * 60 * 1000, // 3분
    gcTime: 10 * 60 * 1000, // 10분
    retry: 1,
    refetchOnWindowFocus: false,
  });
};

export const useGetPostDetail = (postId: string) => {
  return useQuery({
    queryKey: ["posts", postId],
    queryFn: () => getPostDetail(postId),
    enabled: !!postId,
    staleTime: 3 * 60 * 1000, // 3분
    gcTime: 10 * 60 * 1000, // 10분
  });
};
