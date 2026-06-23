// frontend/src/api/videos.js

import api from './api'

export function searchVideos(keyword, maxResults = 3) {
  return api.get('/videos/search/', {
    params: {
      q: keyword,
      max_results: maxResults,
    },
  })
}

export function getVideoDetail(videoId) {
  return api.get(`/videos/${videoId}/`)
}

export function saveVideo(video) {
  return api.post('/videos/saved/', {
    video_id: video.video_id,
    title: video.title,
    channel_title: video.channel_title,
    channel_id: video.channel_id,
    description: video.description,
    thumbnail_url: video.thumbnail_url,
    published_at: video.published_at,
  })
}

export function getSavedVideos() {
  return api.get('/videos/saved/')
}

export function deleteSavedVideo(videoId) {
  return api.delete(`/videos/saved/${videoId}/`)
}