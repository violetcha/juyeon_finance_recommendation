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
    video_id: video.id,
    title: video.title,
    channel_title: video.channelTitle,
    channel_id: video.channelId,
    description: video.description,
    thumbnail_url: video.thumbnail,
    published_at: video.publishedAt,
  })
}