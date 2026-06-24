import api from '@/api/api'

const COMMUNITY_BASE_URL = '/community/'

export const getPosts = () => {
  return api.get(COMMUNITY_BASE_URL)
}

export const createPost = (payload) => {
  return api.post(COMMUNITY_BASE_URL, payload)
}

export const getPostDetail = (postId) => {
  return api.get(`${COMMUNITY_BASE_URL}${postId}/`)
}

export const updatePost = (postId, payload) => {
  return api.put(`${COMMUNITY_BASE_URL}${postId}/`, payload)
}

export const deletePost = (postId) => {
  return api.delete(`${COMMUNITY_BASE_URL}${postId}/`)
}

export const togglePostLike = (postId) => {
  return api.post(`${COMMUNITY_BASE_URL}${postId}/like/`)
}

export const createComment = (postId, payload) => {
  return api.post(`${COMMUNITY_BASE_URL}${postId}/comments/`, payload)
}

export const updateComment = (commentId, payload) => {
  return api.put(`${COMMUNITY_BASE_URL}comments/${commentId}/`, payload)
}

export const deleteComment = (commentId) => {
  return api.delete(`${COMMUNITY_BASE_URL}comments/${commentId}/`)
}

export const toggleCommentLike = (commentId) => {
  return api.post(`${COMMUNITY_BASE_URL}comments/${commentId}/like/`)
}