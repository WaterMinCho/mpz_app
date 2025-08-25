// 게시물 관련 타입 정의

export interface Post {
  id: string;
  title: string;
  content: string;
  userId: string;
  animalId: string | null;
  adoptionsId: string | null;
  contentTags: string | null;
  visibility: "public" | "center";
  createdAt: string;
  updatedAt: string;
  userNickname: string;
  userImage: string | null;
  tags: PostTag[];
  images: PostImage[];
  postLikes: PostLike[];
  comments?: CommentWithReplies[];
}

export interface PostTag {
  id: string;
  postId: string;
  tagName: string;
  createdAt: string;
}

export interface PostImage {
  id: string;
  postId: string;
  imageUrl: string;
  orderIndex: number;
  createdAt: string;
}

export interface PostLike {
  id: string;
  postId: string;
  userId: string;
  createdAt: string;
}

export interface CommentWithReplies {
  id: string;
  postId: string;
  userId: string;
  content: string;
  likeCount: number;
  createdAt: string;
  updatedAt: string;
  replies: Reply[];
  user?: {
    id: string;
    nickname: string | null;
    image: string | null;
  };
}

export interface Reply {
  id: string;
  commentId: string;
  userId: string;
  content: string;
  createdAt: string;
}

export interface GetPostsResponse {
  posts: Post[];
}

export interface PostDetailResponse {
  post: Post;
}

export interface GetPostsParams {
  sort?: "likes" | "latest";
  tag?: string;
  animalId?: string;
  userId?: string;
  visibility?: "public" | "center";
  page?: number;
  page_size?: number;
}
