// frontend/src/api/videos.js

import api from './api'

const getVideoId = (video) => {
  if (!video) {
    return ''
  }

  if (typeof video.id === 'string') {
    return video.id
  }

  if (video.id?.videoId) {
    return video.id.videoId
  }

  if (video.video_id) {
    return video.video_id
  }

  return ''
}

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
  const videoId = getVideoId(video)

  return api.post('/videos/saved/', {
    video_id: videoId,
    title: video.title || '',
    channel_title: video.channel_title || video.channelTitle || '',
    channel_id: video.channel_id || video.channelId || '',
    description: video.description || '',
    thumbnail_url: video.thumbnail_url || video.thumbnail || '',
    published_at: video.published_at || video.publishedAt || null,
  })
}

export function getSavedVideos() {
  return api.get('/videos/saved/')
}

export function deleteSavedVideo(videoId) {
  return api.delete(`/videos/saved/${videoId}/`)
}