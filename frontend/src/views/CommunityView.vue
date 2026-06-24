<template>
  <main class="community-page">
    <section class="community-hero">
      <div>
        <p class="eyebrow">FINANCIAL COMMUNITY</p>
        <h1>금융 커뮤니티</h1>
        <p>
          예적금 후기, 금융상품 질문, 재테크 팁을 실제 회원들과 나누는 공간입니다.
        </p>
      </div>

      <div class="community-hero-art" aria-hidden="true">
        <div class="bubble-card">💬</div>
        <div class="piggy-card">🐷</div>
        <div class="coin-card">₩</div>
      </div>
    </section>

    <p v-if="errorMessage" class="error-message global">
      {{ errorMessage }}
    </p>

    <template v-if="viewMode === 'list'">
      <div class="community-layout">
        <section class="board-card">
          <div class="category-tabs">
            <button
              v-for="category in categoryItems"
              :key="category.value"
              type="button"
              :class="{ active: selectedCategory === category.value }"
              @click="changeCategory(category.value)"
            >
              {{ category.label }}
              <span>{{ category.count }}</span>
            </button>
          </div>

          <div class="board-tools">
            <label class="search-box">
              <input
                v-model.trim="keyword"
                type="text"
                placeholder="제목, 내용, 작성자를 검색해보세요."
              >
              <span>⌕</span>
            </label>

            <select v-model="searchTarget">
              <option value="all">전체 검색</option>
              <option value="title">제목</option>
              <option value="content">내용</option>
              <option value="author">작성자</option>
            </select>

            <select v-model="sortType">
              <option value="latest">최신순</option>
              <option value="oldest">오래된순</option>
              <option value="likes">좋아요순</option>
              <option value="views">조회수순</option>
              <option value="comments">댓글순</option>
            </select>

            <button type="button" class="primary-button write-button" @click="openCreateForm">
              ✎ 글쓰기
            </button>
          </div>

          <p v-if="loading" class="state-message">게시글을 불러오는 중입니다...</p>

          <div v-else-if="filteredPosts.length === 0" class="empty-box">
            <strong>조건에 맞는 게시글이 없습니다.</strong>
            <span>검색어를 바꾸거나 다른 카테고리를 선택해보세요.</span>
          </div>

          <div v-else class="post-list">
            <article
              v-for="post in filteredPosts"
              :key="post.id"
              class="post-list-item"
              @click="openPost(post.id)"
            >
              <div class="post-main">
                <div class="post-title-row">
                  <h2>{{ post.title }}</h2>
                  <span
                    v-if="getRelativeTime(post.created_at).includes('시간') || getRelativeTime(post.created_at).includes('분') || getRelativeTime(post.created_at) === '방금 전'"
                    class="new-dot"
                  >
                    N
                  </span>
                </div>

                <p class="post-preview">
                  {{ getPreview(post.content) }}
                </p>
              </div>

              <div class="post-author">
                <span class="author-avatar" :class="getCategoryTone(post.category)">
                  {{ getAuthorInitial(post.username) }}
                </span>
                <strong>{{ post.username || '익명' }}</strong>
              </div>

              <span class="category-badge" :class="getCategoryTone(post.category)">
                {{ getCategoryLabel(post.category) }}
              </span>

              <div class="post-stats">
                <span>👍 {{ post.like_count || 0 }}</span>
                <span>💬 {{ post.comment_count || 0 }}</span>
                <span>👁 {{ post.view_count || 0 }}</span>
              </div>

              <time>{{ getRelativeTime(post.created_at) }}</time>
            </article>
          </div>
        </section>

        <aside class="community-sidebar">
          <section class="side-card">
            <div class="side-title">
              <h2>인기 게시글</h2>
              <span>Top 5</span>
            </div>

            <button
              v-for="(post, index) in popularPosts"
              :key="post.id"
              type="button"
              class="popular-post"
              @click="openPost(post.id)"
            >
              <span class="rank-badge">{{ index + 1 }}</span>
              <strong>{{ post.title }}</strong>
              <em>👍 {{ post.like_count || 0 }}</em>
            </button>

            <p v-if="popularPosts.length === 0" class="side-empty">
              아직 인기 게시글이 없습니다.
            </p>
          </section>

          <section class="side-card">
            <div class="side-title">
              <h2>인기 태그</h2>
              <span>실제 카테고리 기준</span>
            </div>

            <div class="tag-cloud">
              <button
                v-for="tag in popularTags"
                :key="tag"
                type="button"
              >
                # {{ tag }}
              </button>
            </div>
          </section>

          <section class="side-card guide">
            <div class="side-title">
              <h2>커뮤니티 이용 가이드</h2>
            </div>

            <ul>
              <li>서로 존중하는 마음으로 소통해주세요.</li>
              <li>금융 정보는 확인 후 공유해주세요.</li>
              <li>광고성 글은 삭제될 수 있습니다.</li>
              <li>개인정보는 게시하지 말아주세요.</li>
            </ul>
          </section>
        </aside>
      </div>
    </template>

    <section v-else-if="viewMode === 'write'" class="post-form-card">
      <div class="detail-header">
        <div>
          <p class="eyebrow">WRITE</p>
          <h2>{{ editingPostId ? '게시글 수정' : '새 게시글 작성' }}</h2>
          <p>금융 정보를 나누되 개인정보나 광고성 내용은 제외해주세요.</p>
        </div>

        <button type="button" class="ghost-button" @click="goList">
          목록으로
        </button>
      </div>

      <form class="post-form" @submit.prevent="submitPost">
        <div class="form-group">
          <label for="post-category">카테고리</label>
          <select id="post-category" v-model="postForm.category">
            <option value="free">자유게시판</option>
            <option value="product">상품질문</option>
            <option value="review">가입후기</option>
            <option value="tip">금융팁</option>
          </select>
        </div>

        <div class="form-group">
          <label for="post-title">제목</label>
          <input
            id="post-title"
            v-model.trim="postForm.title"
            type="text"
            placeholder="제목을 입력하세요"
          >
        </div>

        <div class="form-group">
          <label for="post-content">내용</label>
          <textarea
            id="post-content"
            v-model.trim="postForm.content"
            rows="14"
            placeholder="내용을 입력하세요"
          ></textarea>
        </div>

        <div class="form-actions">
          <button type="button" class="ghost-button" @click="goList">
            취소
          </button>

          <button type="submit" class="primary-button" :disabled="submitting">
            {{ submitting ? '저장 중...' : editingPostId ? '수정하기' : '등록하기' }}
          </button>
        </div>
      </form>
    </section>

    <section
      v-else-if="viewMode === 'detail' && selectedPost"
      class="post-detail-card"
    >
      <div class="detail-header">
        <div>
          <span class="category-badge" :class="getCategoryTone(selectedPost.category)">
            {{ getCategoryLabel(selectedPost.category) }}
          </span>

          <h2>{{ selectedPost.title }}</h2>

          <div class="detail-meta">
            <span>{{ selectedPost.username || '익명' }}</span>
            <span>{{ formatDateTime(selectedPost.created_at) }}</span>
            <span>조회 {{ selectedPost.view_count || 0 }}</span>
            <span>댓글 {{ selectedPost.comments?.length || 0 }}</span>
            <span>좋아요 {{ selectedPost.like_count || 0 }}</span>
          </div>
        </div>

        <div class="detail-actions">
          <button type="button" class="ghost-button" @click="goList">
            목록으로
          </button>

          <button
            type="button"
            class="like-button"
            :class="{ liked: selectedPost.is_liked }"
            @click="handleTogglePostLike"
          >
            {{ selectedPost.is_liked ? '❤️' : '🤍' }}
            좋아요 {{ selectedPost.like_count || 0 }}
          </button>

          <button
            v-if="selectedPost.is_author"
            type="button"
            class="ghost-button"
            @click="startEditPost"
          >
            수정
          </button>

          <button
            v-if="selectedPost.is_author"
            type="button"
            class="danger-button"
            @click="handleDeletePost"
          >
            삭제
          </button>
        </div>
      </div>

      <article class="post-content">
        {{ selectedPost.content }}
      </article>

      <section class="comment-section">
        <div class="comment-header">
          <h3>댓글 {{ selectedPost.comments?.length || 0 }}</h3>
        </div>

        <form class="comment-form" @submit.prevent="submitComment">
          <textarea
            v-model.trim="commentContent"
            rows="3"
            placeholder="댓글을 입력하세요"
          ></textarea>

          <button type="submit" :disabled="commentSubmitting">
            {{ commentSubmitting ? '등록 중...' : '댓글 등록' }}
          </button>
        </form>

        <div
          v-if="!selectedPost.comments || selectedPost.comments.length === 0"
          class="empty-comment"
        >
          아직 댓글이 없습니다.
        </div>

        <div v-else class="comment-list">
          <article
            v-for="comment in selectedPost.comments"
            :key="comment.id"
            class="comment-item"
          >
            <div class="comment-top">
              <div>
                <strong>{{ comment.username || '익명' }}</strong>
                <span>{{ formatDateTime(comment.created_at) }}</span>
              </div>
            </div>

            <div
              v-if="editingCommentId === comment.id"
              class="comment-edit-box"
            >
              <textarea
                v-model.trim="editingCommentContent"
                rows="3"
                placeholder="댓글을 수정하세요"
              ></textarea>

              <div class="comment-edit-actions">
                <button
                  type="button"
                  class="comment-save-button"
                  @click="submitEditComment(comment.id)"
                >
                  저장
                </button>

                <button
                  type="button"
                  class="comment-cancel-button"
                  @click="cancelEditComment"
                >
                  취소
                </button>
              </div>
            </div>

            <p v-else>{{ comment.content }}</p>

            <div class="comment-actions">
              <button
                type="button"
                class="comment-like-button"
                :class="{ liked: comment.is_liked }"
                @click="handleToggleCommentLike(comment.id)"
              >
                {{ comment.is_liked ? '❤️' : '🤍' }}
                {{ comment.like_count || 0 }}
              </button>

              <button
                v-if="comment.is_author && editingCommentId !== comment.id"
                type="button"
                class="comment-edit-button"
                @click="startEditComment(comment)"
              >
                수정
              </button>

              <button
                v-if="comment.is_author"
                type="button"
                class="comment-delete-button"
                @click="handleDeleteComment(comment.id)"
              >
                삭제
              </button>
            </div>
          </article>
        </div>
      </section>
    </section>
  </main>
</template>


<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  getPosts,
  createPost,
  getPostDetail,
  updatePost,
  deletePost,
  togglePostLike,
  createComment,
  updateComment,
  deleteComment,
  toggleCommentLike,
} from '@/api/community'

const route = useRoute()
const router = useRouter()

const posts = ref([])
const selectedPost = ref(null)

const viewMode = ref('list')
const loading = ref(false)
const submitting = ref(false)
const commentSubmitting = ref(false)

const errorMessage = ref('')
const selectedCategory = ref('all')
const searchTarget = ref('all')
const keyword = ref('')
const sortType = ref('latest')

const editingPostId = ref(null)
const commentContent = ref('')
const editingCommentId = ref(null)
const editingCommentContent = ref('')

const postForm = reactive({
  title: '',
  content: '',
  category: 'free',
})

const categoryMap = {
  free: '자유게시판',
  product: '상품질문',
  review: '가입후기',
  tip: '금융팁',
}

const filteredPosts = computed(() => {
  const searchText = keyword.value.toLowerCase()

  const filtered = posts.value.filter((post) => {
    const categoryMatched =
      selectedCategory.value === 'all' ||
      post.category === selectedCategory.value

    const title = post.title?.toLowerCase() || ''
    const content = post.content?.toLowerCase() || ''
    const author = post.username?.toLowerCase() || ''

    let keywordMatched = true

    if (searchText) {
      if (searchTarget.value === 'title') {
        keywordMatched = title.includes(searchText)
      } else if (searchTarget.value === 'content') {
        keywordMatched = content.includes(searchText)
      } else if (searchTarget.value === 'author') {
        keywordMatched = author.includes(searchText)
      } else {
        keywordMatched =
          title.includes(searchText) ||
          content.includes(searchText)
      }
    }

    return categoryMatched && keywordMatched
  })

  return filtered.sort((a, b) => {
    if (sortType.value === 'oldest') {
      return new Date(a.created_at) - new Date(b.created_at)
    }

    if (sortType.value === 'likes') {
      return (b.like_count || 0) - (a.like_count || 0)
    }

    if (sortType.value === 'views') {
      return (b.view_count || 0) - (a.view_count || 0)
    }

    if (sortType.value === 'comments') {
      return (b.comment_count || 0) - (a.comment_count || 0)
    }

    return new Date(b.created_at) - new Date(a.created_at)
  })
})

const fetchPosts = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await getPosts()
    posts.value = response.data || []
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error.response?.data?.message ||
      '게시글을 불러오지 못했습니다. community API를 확인해주세요.'
  } finally {
    loading.value = false
  }
}

const resetPostForm = () => {
  postForm.title = ''
  postForm.content = ''
  postForm.category = 'free'
}

const resetCommentEditState = () => {
  editingCommentId.value = null
  editingCommentContent.value = ''
}

const showList = async () => {
  viewMode.value = 'list'
  editingPostId.value = null
  selectedPost.value = null
  commentContent.value = ''
  resetCommentEditState()
  resetPostForm()
  await fetchPosts()
}

const loadPostDetail = async (postId) => {
  errorMessage.value = ''

  try {
    const response = await getPostDetail(postId)
    selectedPost.value = response.data
    viewMode.value = 'detail'
    editingPostId.value = null
    resetCommentEditState()
    await fetchPosts()
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error.response?.data?.message ||
      '게시글 상세 정보를 불러오지 못했습니다.'

    viewMode.value = 'list'
    selectedPost.value = null
    resetCommentEditState()
    await fetchPosts()
  }
}

const openPost = async (postId) => {
  await router.push({
    path: '/community',
    query: {
      post: postId,
    },
  })
}

const openCreateForm = async () => {
  await router.push({
    path: '/community',
    query: {
      mode: 'write',
    },
  })
}

const goList = async () => {
  if (route.path === '/community' && !route.query.post && route.query.mode !== 'write') {
    await showList()
    return
  }

  await router.push({
    path: '/community',
  })
}

const submitPost = async () => {
  if (!postForm.title || !postForm.content) {
    alert('제목과 내용을 입력해주세요.')
    return
  }

  submitting.value = true
  errorMessage.value = ''

  try {
    const payload = {
      title: postForm.title,
      content: postForm.content,
      category: postForm.category,
    }

    let response

    if (editingPostId.value) {
      response = await updatePost(editingPostId.value, payload)
    } else {
      response = await createPost(payload)
    }

    resetPostForm()
    editingPostId.value = null

    await router.push({
      path: '/community',
      query: {
        post: response.data.id,
      },
    })
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error.response?.data?.message ||
      '게시글 저장에 실패했습니다. 로그인 여부를 확인해주세요.'
  } finally {
    submitting.value = false
  }
}

const startEditPost = () => {
  if (!selectedPost.value) return

  if (!selectedPost.value.is_author) {
    alert('본인이 작성한 게시글만 수정할 수 있습니다.')
    return
  }

  editingPostId.value = selectedPost.value.id
  postForm.title = selectedPost.value.title
  postForm.content = selectedPost.value.content
  postForm.category = selectedPost.value.category
  viewMode.value = 'write'
}

const handleDeletePost = async () => {
  if (!selectedPost.value) return

  if (!selectedPost.value.is_author) {
    alert('본인이 작성한 게시글만 삭제할 수 있습니다.')
    return
  }

  const confirmed = window.confirm('게시글을 삭제할까요?')

  if (!confirmed) return

  try {
    await deletePost(selectedPost.value.id)

    await router.push({
      path: '/community',
    })
  } catch (error) {
    console.error(error)

    alert(
      error.response?.data?.message ||
      '게시글 삭제에 실패했습니다. 본인이 작성한 글인지 확인해주세요.'
    )
  }
}

const handleTogglePostLike = async () => {
  if (!selectedPost.value) return

  try {
    const response = await togglePostLike(selectedPost.value.id)

    selectedPost.value.is_liked = response.data.liked
    selectedPost.value.like_count = response.data.like_count

    const targetPost = posts.value.find((post) => post.id === selectedPost.value.id)

    if (targetPost) {
      targetPost.is_liked = response.data.liked
      targetPost.like_count = response.data.like_count
    }
  } catch (error) {
    console.error(error)

    alert(
      error.response?.data?.message ||
      '좋아요 처리에 실패했습니다. 로그인 여부를 확인해주세요.'
    )
  }
}

const submitComment = async () => {
  if (!selectedPost.value) return

  if (!commentContent.value) {
    alert('댓글 내용을 입력해주세요.')
    return
  }

  commentSubmitting.value = true

  try {
    await createComment(selectedPost.value.id, {
      content: commentContent.value,
    })

    commentContent.value = ''
    await loadPostDetail(selectedPost.value.id)
  } catch (error) {
    console.error(error)

    alert(
      error.response?.data?.message ||
      '댓글 등록에 실패했습니다. 로그인 여부를 확인해주세요.'
    )
  } finally {
    commentSubmitting.value = false
  }
}

const startEditComment = (comment) => {
  if (!comment.is_author) {
    alert('본인이 작성한 댓글만 수정할 수 있습니다.')
    return
  }

  editingCommentId.value = comment.id
  editingCommentContent.value = comment.content
}

const cancelEditComment = () => {
  resetCommentEditState()
}

const submitEditComment = async (commentId) => {
  if (!selectedPost.value) return

  if (!editingCommentContent.value) {
    alert('댓글 내용을 입력해주세요.')
    return
  }

  try {
    await updateComment(commentId, {
      content: editingCommentContent.value,
    })

    resetCommentEditState()
    await loadPostDetail(selectedPost.value.id)
  } catch (error) {
    console.error(error)

    alert(
      error.response?.data?.message ||
      '댓글 수정에 실패했습니다. 본인이 작성한 댓글인지 확인해주세요.'
    )
  }
}

const handleDeleteComment = async (commentId) => {
  if (!selectedPost.value) return

  const targetComment = selectedPost.value.comments?.find(
    (comment) => comment.id === commentId
  )

  if (targetComment && !targetComment.is_author) {
    alert('본인이 작성한 댓글만 삭제할 수 있습니다.')
    return
  }

  const confirmed = window.confirm('댓글을 삭제할까요?')

  if (!confirmed) return

  try {
    await deleteComment(commentId)
    resetCommentEditState()
    await loadPostDetail(selectedPost.value.id)
  } catch (error) {
    console.error(error)

    alert(
      error.response?.data?.message ||
      '댓글 삭제에 실패했습니다. 본인이 작성한 댓글인지 확인해주세요.'
    )
  }
}

const handleToggleCommentLike = async (commentId) => {
  if (!selectedPost.value) return

  try {
    const response = await toggleCommentLike(commentId)

    const targetComment = selectedPost.value.comments.find(
      (comment) => comment.id === commentId
    )

    if (targetComment) {
      targetComment.is_liked = response.data.liked
      targetComment.like_count = response.data.like_count
    }
  } catch (error) {
    console.error(error)

    alert(
      error.response?.data?.message ||
      '댓글 좋아요 처리에 실패했습니다. 로그인 여부를 확인해주세요.'
    )
  }
}

const getCategoryLabel = (category) => {
  return categoryMap[category] || '기타'
}

const getPreview = (content) => {
  if (!content) return '내용 미리보기가 없습니다.'

  if (content.length <= 70) {
    return content
  }

  return `${content.slice(0, 70)}...`
}

const formatDate = (value) => {
  if (!value) return '-'

  const date = new Date(value)

  return date.toLocaleDateString('ko-KR', {
    year: '2-digit',
    month: '2-digit',
    day: '2-digit',
  })
}

const formatDateTime = (value) => {
  if (!value) return '-'

  const date = new Date(value)

  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}


const categoryItems = computed(() => {
  const base = [
    { value: 'all', label: '전체' },
    { value: 'free', label: '자유게시판' },
    { value: 'review', label: '예적금 후기' },
    { value: 'tip', label: '재테크 팁' },
    { value: 'product', label: '질문답변' },
  ]

  return base.map((item) => ({
    ...item,
    count: getCategoryCount(item.value),
  }))
})

const popularPosts = computed(() => {
  return [...posts.value]
    .sort((a, b) => getPostScore(b) - getPostScore(a))
    .slice(0, 5)
})

const popularTags = computed(() => {
  const tags = [
    { label: '예적금', value: 'review' },
    { label: '상품질문', value: 'product' },
    { label: '재테크', value: 'tip' },
    { label: '자유게시판', value: 'free' },
  ]

  const dynamicTags = posts.value
    .map((post) => getCategoryLabel(post.category))
    .filter(Boolean)

  const uniqueLabels = [...new Set([...tags.map((tag) => tag.label), ...dynamicTags])]

  return uniqueLabels.slice(0, 8)
})

const getCategoryCount = (category) => {
  if (category === 'all') {
    return posts.value.length
  }

  return posts.value.filter((post) => post.category === category).length
}

const getPostScore = (post) => {
  return (post.like_count || 0) * 5 + (post.comment_count || 0) * 3 + (post.view_count || 0)
}

const getCategoryTone = (category) => {
  const tones = {
    free: 'mint',
    product: 'purple',
    review: 'green',
    tip: 'blue',
  }

  return tones[category] || 'gray'
}

const getAuthorInitial = (name) => {
  if (!name) {
    return '익'
  }

  return String(name).slice(0, 1).toUpperCase()
}

const getRelativeTime = (value) => {
  if (!value) {
    return '-'
  }

  const createdAt = new Date(value)
  const diffMs = Date.now() - createdAt.getTime()
  const diffMinutes = Math.floor(diffMs / 1000 / 60)

  if (diffMinutes < 1) {
    return '방금 전'
  }

  if (diffMinutes < 60) {
    return `${diffMinutes}분 전`
  }

  const diffHours = Math.floor(diffMinutes / 60)

  if (diffHours < 24) {
    return `${diffHours}시간 전`
  }

  const diffDays = Math.floor(diffHours / 24)

  if (diffDays < 7) {
    return `${diffDays}일 전`
  }

  return formatDate(value)
}

const changeCategory = (category) => {
  selectedCategory.value = category
}

watch(
  () => route.fullPath,
  async () => {
    if (route.query.post) {
      await loadPostDetail(route.query.post)
      return
    }

    if (route.query.mode === 'write') {
      viewMode.value = 'write'
      editingPostId.value = null
      selectedPost.value = null
      commentContent.value = ''
      resetCommentEditState()
      resetPostForm()
      return
    }

    await showList()
  },
  { immediate: true }
)
</script>



<style scoped>
.community-page {
  width: min(var(--container-width), calc(100% - 48px));
  margin: 0 auto;
  padding: 36px 0 64px;
}

.community-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 420px;
  gap: 32px;
  align-items: center;
  min-height: 190px;
  margin-bottom: 24px;
}

.eyebrow {
  margin: 0 0 10px;
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 950;
  letter-spacing: 0.12em;
}

.community-hero h1 {
  margin: 0;
  color: var(--color-text);
  font-size: clamp(38px, 5vw, 54px);
  line-height: 1.08;
  font-weight: 950;
  letter-spacing: -0.06em;
}

.community-hero p {
  margin: 16px 0 0;
  color: var(--color-text-muted);
  font-size: 17px;
  line-height: 1.6;
}

.community-hero-art {
  position: relative;
  height: 150px;
}

.bubble-card,
.piggy-card,
.coin-card {
  position: absolute;
  display: grid;
  place-items: center;
  border: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-soft);
}

.bubble-card {
  left: 40px;
  top: 28px;
  width: 116px;
  height: 86px;
  border-radius: 26px;
  font-size: 42px;
  background: #eff6ff;
}

.piggy-card {
  left: 178px;
  top: 0;
  width: 120px;
  height: 120px;
  border-radius: 42px;
  font-size: 58px;
  background: var(--color-accent-soft);
}

.coin-card {
  right: 36px;
  bottom: 22px;
  width: 74px;
  height: 74px;
  border-radius: 28px;
  color: #d97706;
  background: #fff7e5;
  font-size: 34px;
  font-weight: 950;
}

.community-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 330px;
  gap: 20px;
  align-items: flex-start;
}

.board-card,
.post-detail-card,
.post-form-card,
.side-card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: #ffffff;
  box-shadow: var(--shadow-soft);
}

.board-card {
  overflow: hidden;
}

.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 18px 18px 14px;
  border-bottom: 1px solid var(--color-border);
}

.category-tabs button {
  min-height: 42px;
  padding: 0 18px;
  border: 1px solid var(--color-border);
  border-radius: 14px;
  background: #fff;
  color: var(--color-text-muted);
  font-weight: 900;
}

.category-tabs button.active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: #fff;
  box-shadow: 0 10px 20px rgba(17, 22, 184, 0.18);
}

.category-tabs span {
  margin-left: 6px;
  font-size: 12px;
  opacity: 0.72;
}

.board-tools {
  display: grid;
  grid-template-columns: minmax(280px, 1fr) 132px 132px 116px;
  gap: 12px;
  align-items: center;
  padding: 18px;
  border-bottom: 1px solid var(--color-border);
}

.search-box {
  position: relative;
}

.search-box input,
.board-tools select,
.post-form input,
.post-form select,
.post-form textarea,
.comment-form textarea,
.comment-edit-box textarea {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid var(--color-border-strong);
  border-radius: 14px;
  background: #fff;
  color: var(--color-text);
  outline: none;
  font-size: 14px;
}

.search-box input,
.board-tools select {
  min-height: 46px;
  padding: 0 42px 0 14px;
}

.search-box input:focus,
.board-tools select:focus,
.post-form input:focus,
.post-form select:focus,
.post-form textarea:focus,
.comment-form textarea:focus,
.comment-edit-box textarea:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(17, 22, 184, 0.08);
}

.search-box span {
  position: absolute;
  right: 15px;
  top: 50%;
  color: var(--color-text);
  font-size: 20px;
  font-weight: 950;
  transform: translateY(-50%);
}

.primary-button,
.comment-form button {
  border: 0;
  border-radius: 14px;
  background: var(--color-primary);
  color: #fff;
  font-weight: 950;
  cursor: pointer;
  box-shadow: 0 14px 24px rgba(17, 22, 184, 0.18);
}

.write-button {
  min-height: 46px;
}

.post-list {
  display: grid;
}

.post-list-item {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 140px 112px 170px 82px;
  gap: 16px;
  align-items: center;
  padding: 18px;
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.post-list-item:hover {
  background: var(--color-surface-soft);
}

.post-main {
  min-width: 0;
}

.post-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.post-title-row h2 {
  overflow: hidden;
  margin: 0;
  color: var(--color-text);
  font-size: 17px;
  font-weight: 950;
  letter-spacing: -0.03em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.new-dot {
  display: inline-grid;
  place-items: center;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #ef4444;
  color: #fff;
  font-size: 10px;
  font-weight: 950;
  flex-shrink: 0;
}

.post-preview {
  overflow: hidden;
  margin: 7px 0 0;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.5;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.author-avatar {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 14px;
  color: #fff;
  font-size: 13px;
  font-weight: 950;
  flex-shrink: 0;
}

.post-author strong {
  overflow: hidden;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.category-badge {
  display: inline-flex;
  justify-content: center;
  width: fit-content;
  min-width: 74px;
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 950;
}

.category-badge.blue,
.author-avatar.blue {
  background: #eaf0ff;
  color: #3151db;
}

.category-badge.mint,
.author-avatar.mint {
  background: #e7fbf7;
  color: #0f9f8b;
}

.category-badge.green,
.author-avatar.green {
  background: #ecfdf5;
  color: #059669;
}

.category-badge.purple,
.author-avatar.purple {
  background: #f3e8ff;
  color: #7c3aed;
}

.category-badge.gray,
.author-avatar.gray {
  background: #f1f5f9;
  color: #475569;
}

.author-avatar.blue,
.author-avatar.mint,
.author-avatar.green,
.author-avatar.purple,
.author-avatar.gray {
  color: #fff;
}

.author-avatar.blue { background: linear-gradient(135deg, #60a5fa, #2563eb); }
.author-avatar.mint { background: linear-gradient(135deg, #4be0c8, #0f9f8b); }
.author-avatar.green { background: linear-gradient(135deg, #34d399, #059669); }
.author-avatar.purple { background: linear-gradient(135deg, #a78bfa, #7c3aed); }
.author-avatar.gray { background: linear-gradient(135deg, #94a3b8, #475569); }

.post-stats {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 800;
}

.post-list-item time {
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 800;
  text-align: right;
}

.community-sidebar {
  display: grid;
  gap: 16px;
  position: sticky;
  top: calc(var(--header-height) + 18px);
}

.side-card {
  padding: 18px;
}

.side-title {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 14px;
}

.side-title h2 {
  margin: 0;
  color: var(--color-text);
  font-size: 18px;
  font-weight: 950;
}

.side-title span {
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 900;
}

.popular-post {
  display: grid;
  grid-template-columns: 28px minmax(0, 1fr) auto;
  gap: 10px;
  align-items: center;
  width: 100%;
  padding: 10px 0;
  border: 0;
  border-bottom: 1px solid var(--color-border);
  background: transparent;
  color: var(--color-text);
  text-align: left;
  cursor: pointer;
}

.popular-post:last-of-type {
  border-bottom: 0;
}

.rank-badge {
  display: grid;
  place-items: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  font-size: 12px;
  font-weight: 950;
}

.popular-post strong {
  overflow: hidden;
  font-size: 13px;
  font-weight: 900;
  line-height: 1.45;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.popular-post em {
  color: var(--color-text-muted);
  font-size: 12px;
  font-style: normal;
  font-weight: 800;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-cloud button {
  min-height: 32px;
  padding: 0 11px;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 900;
}

.guide ul {
  display: grid;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.guide li {
  position: relative;
  padding-left: 24px;
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.55;
  font-weight: 700;
}

.guide li::before {
  content: '✓';
  position: absolute;
  left: 0;
  top: 0;
  color: var(--color-primary);
  font-weight: 950;
}

.state-message,
.empty-box,
.empty-comment,
.side-empty {
  margin: 18px;
  padding: 28px 18px;
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
  color: var(--color-text-muted);
  text-align: center;
  font-weight: 800;
}

.empty-box {
  display: grid;
  gap: 6px;
}

.empty-box strong {
  color: var(--color-text);
}

.error-message {
  color: var(--color-danger);
  font-weight: 900;
}

.error-message.global {
  margin: 0 0 18px;
  padding: 14px 18px;
  border: 1px solid #fecaca;
  border-radius: var(--radius-md);
  background: #fff5f5;
}

.post-detail-card,
.post-form-card {
  padding: 26px;
}

.detail-header,
.comment-header {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: flex-start;
}

.detail-header h2 {
  margin: 14px 0 0;
  color: var(--color-text);
  font-size: 30px;
  line-height: 1.25;
  font-weight: 950;
  letter-spacing: -0.04em;
}

.detail-header p {
  margin: 8px 0 0;
  color: var(--color-text-muted);
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 800;
}

.detail-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-end;
  flex-shrink: 0;
}

.ghost-button,
.danger-button,
.like-button {
  min-height: 40px;
  border: 1px solid var(--color-border-strong);
  border-radius: 12px;
  padding: 0 14px;
  background: #ffffff;
  color: var(--color-text);
  font-weight: 900;
  cursor: pointer;
}

.danger-button {
  border-color: #fecaca;
  color: var(--color-danger);
}

.like-button {
  border-color: #fecaca;
  color: var(--color-danger);
}

.like-button.liked {
  border-color: var(--color-danger);
  background: #fff1f2;
}

.post-content {
  min-height: 260px;
  margin-top: 24px;
  padding: 26px;
  border-radius: var(--radius-md);
  background: var(--color-surface-soft);
  color: var(--color-text);
  line-height: 1.85;
  white-space: pre-wrap;
}

.post-form {
  display: grid;
  gap: 16px;
  margin-top: 22px;
}

.form-group {
  display: grid;
  gap: 8px;
}

.form-group label {
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 950;
}

.post-form input,
.post-form select,
.post-form textarea,
.comment-form textarea,
.comment-edit-box textarea {
  padding: 13px 14px;
}

.post-form textarea,
.comment-form textarea,
.comment-edit-box textarea {
  resize: vertical;
  line-height: 1.6;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.primary-button:disabled,
.comment-form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.comment-section {
  margin-top: 34px;
}

.comment-header h3 {
  margin: 0 0 14px;
  color: var(--color-text);
  font-size: 22px;
}

.comment-form {
  display: grid;
  gap: 10px;
  margin-bottom: 18px;
}

.comment-form button {
  justify-self: end;
  min-height: 42px;
  padding: 0 16px;
}

.comment-list {
  display: grid;
  gap: 12px;
}

.comment-item {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px;
  background: #ffffff;
}

.comment-top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.comment-top div {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.comment-item strong {
  color: var(--color-text);
}

.comment-item span {
  color: var(--color-text-light);
  font-size: 12px;
}

.comment-item p {
  margin: 0;
  color: var(--color-text-muted);
  line-height: 1.65;
  white-space: pre-wrap;
}

.comment-actions {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-top: 12px;
}

.comment-like-button,
.comment-delete-button,
.comment-edit-button,
.comment-save-button,
.comment-cancel-button {
  border: none;
  background: transparent;
  font-weight: 950;
  cursor: pointer;
  padding: 0;
}

.comment-like-button,
.comment-delete-button {
  color: var(--color-danger);
}

.comment-edit-button,
.comment-save-button {
  color: var(--color-primary);
}

.comment-cancel-button {
  color: var(--color-text-muted);
}

.comment-edit-box {
  display: grid;
  gap: 8px;
  margin-top: 8px;
}

.comment-edit-actions {
  display: flex;
  gap: 10px;
}

@media (max-width: 1100px) {
  .community-layout {
    grid-template-columns: 1fr;
  }

  .community-sidebar {
    position: static;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .community-sidebar .guide {
    grid-column: 1 / -1;
  }

  .post-list-item {
    grid-template-columns: minmax(0, 1fr) 120px 100px 150px 76px;
  }
}

@media (max-width: 820px) {
  .community-page {
    width: min(100% - 28px, var(--container-width));
  }

  .community-hero {
    grid-template-columns: 1fr;
  }

  .community-hero-art {
    display: none;
  }

  .board-tools {
    grid-template-columns: 1fr;
  }

  .post-list-item {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .post-stats,
  .post-list-item time {
    justify-content: flex-start;
    text-align: left;
  }

  .community-sidebar {
    grid-template-columns: 1fr;
  }

  .detail-header {
    flex-direction: column;
  }

  .detail-actions {
    justify-content: flex-start;
  }
}
</style>
