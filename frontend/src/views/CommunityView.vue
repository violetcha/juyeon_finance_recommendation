<template>
  <main class="community-page">
    <section class="page-header">
      <p class="eyebrow">Community</p>
      <h1>커뮤니티</h1>
      <p>
        예적금 상품 질문, 가입 후기, 금융 팁을 자유롭게 공유하는 공간입니다.
      </p>
    </section>

    <section v-if="viewMode === 'list'" class="board-card">
      <div class="board-header">
        <div>
          <h2>게시글 목록</h2>
          <p>총 {{ filteredPosts.length }}개 게시글</p>
        </div>

        <button type="button" class="primary-button" @click="openCreateForm">
          글쓰기
        </button>
      </div>

      <div class="board-tools">
        <select v-model="selectedCategory">
          <option value="all">전체 카테고리</option>
          <option value="free">자유게시판</option>
          <option value="product">상품질문</option>
          <option value="review">가입후기</option>
          <option value="tip">금융팁</option>
        </select>

        <select v-model="searchTarget">
          <option value="all">제목 + 내용</option>
          <option value="title">제목</option>
          <option value="content">내용</option>
          <option value="author">작성자</option>
        </select>

        <input
          v-model.trim="keyword"
          type="text"
          placeholder="검색어를 입력하세요"
        />

        <select v-model="sortType">
          <option value="latest">생성일 최신순</option>
          <option value="oldest">생성일 오래된순</option>
          <option value="likes">좋아요 순</option>
          <option value="views">조회수 순</option>
          <option value="comments">댓글 순</option>
        </select>
      </div>

      <p v-if="loading" class="message">게시글을 불러오는 중입니다...</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <div v-if="!loading && filteredPosts.length === 0" class="empty-box">
        조건에 맞는 게시글이 없습니다.
      </div>

      <div v-else class="board-table-wrap">
        <table class="board-table">
          <thead>
            <tr>
              <th class="col-category">분류</th>
              <th>제목</th>
              <th class="col-author">작성자</th>
              <th class="col-number">조회</th>
              <th class="col-number">댓글</th>
              <th class="col-number">좋아요</th>
              <th class="col-date">작성일</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="post in filteredPosts"
              :key="post.id"
              @click="openPost(post.id)"
            >
              <td>
                <span class="category-badge">
                  {{ getCategoryLabel(post.category) }}
                </span>
              </td>

              <td class="title-cell">
                <strong>{{ post.title }}</strong>
                <p>{{ getPreview(post.content) }}</p>
              </td>

              <td>{{ post.username || '익명' }}</td>
              <td>{{ post.view_count || 0 }}</td>
              <td>{{ post.comment_count || 0 }}</td>
              <td>{{ post.like_count || 0 }}</td>
              <td>{{ formatDate(post.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section v-else-if="viewMode === 'write'" class="post-form-card">
      <div class="detail-header">
        <div>
          <p class="eyebrow">Write</p>
          <h2>{{ editingPostId ? '게시글 수정' : '새 게시글 작성' }}</h2>
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
          />
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
          <span class="category-badge">
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
  max-width: 1180px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}

.page-header {
  margin-bottom: 28px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #2563eb;
  font-size: 14px;
  font-weight: 900;
}

.page-header h1 {
  margin: 0 0 10px;
  color: #111827;
  font-size: 36px;
}

.page-header p {
  margin: 0;
  color: #6b7280;
  line-height: 1.6;
}

.board-card,
.post-detail-card,
.post-form-card {
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  background: #ffffff;
  padding: 24px;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
}

.board-header,
.detail-header,
.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.board-header {
  margin-bottom: 20px;
}

.board-header h2,
.detail-header h2 {
  margin: 0;
  color: #111827;
  font-size: 26px;
}

.board-header p {
  margin: 6px 0 0;
  color: #6b7280;
  font-size: 14px;
}

.board-tools {
  display: grid;
  grid-template-columns: 1.1fr 1fr 2fr 1.1fr;
  gap: 10px;
  margin-bottom: 20px;
}

.board-tools select,
.board-tools input,
.post-form input,
.post-form select,
.post-form textarea,
.comment-form textarea,
.comment-edit-box textarea {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 12px 13px;
  background: #ffffff;
  color: #111827;
  font-size: 14px;
}

.primary-button,
.comment-form button {
  border: none;
  border-radius: 10px;
  padding: 11px 15px;
  background: #111827;
  color: #ffffff;
  font-weight: 900;
  cursor: pointer;
}

.primary-button:hover,
.comment-form button:hover {
  background: #1f2937;
}

.message {
  color: #6b7280;
}

.error-message {
  margin: 12px 0;
  color: #dc2626;
  font-weight: 800;
}

.empty-box,
.empty-comment {
  border: 1px dashed #d1d5db;
  border-radius: 16px;
  padding: 36px 18px;
  color: #6b7280;
  text-align: center;
  background: #f9fafb;
}

.board-table-wrap {
  overflow-x: auto;
}

.board-table {
  width: 100%;
  border-collapse: collapse;
}

.board-table th {
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
  padding: 14px 12px;
  background: #f9fafb;
  color: #4b5563;
  font-size: 13px;
  text-align: left;
}

.board-table td {
  border-bottom: 1px solid #e5e7eb;
  padding: 16px 12px;
  color: #111827;
  vertical-align: middle;
}

.board-table tbody tr {
  cursor: pointer;
}

.board-table tbody tr:hover {
  background: #f8fbff;
}

.col-category {
  width: 110px;
}

.col-author {
  width: 110px;
}

.col-number {
  width: 70px;
  text-align: center;
}

.col-date {
  width: 110px;
}

.title-cell strong {
  display: block;
  margin-bottom: 6px;
  color: #111827;
  font-size: 16px;
}

.title-cell p {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
  line-height: 1.4;
}

.category-badge {
  display: inline-flex;
  width: fit-content;
  border-radius: 999px;
  padding: 5px 9px;
  background: #eff6ff;
  color: #2563eb;
  font-size: 12px;
  font-weight: 900;
}

.detail-header {
  margin-bottom: 24px;
}

.detail-header h2 {
  margin-top: 12px;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 8px;
  color: #6b7280;
  font-size: 13px;
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
  border: 1px solid #d1d5db;
  border-radius: 10px;
  padding: 9px 12px;
  background: #ffffff;
  color: #111827;
  font-weight: 800;
  cursor: pointer;
}

.danger-button {
  border-color: #fecaca;
  color: #dc2626;
}

.like-button {
  border-color: #fecaca;
  color: #dc2626;
  font-weight: 900;
}

.like-button.liked {
  border-color: #dc2626;
  background: #fef2f2;
}

.post-content {
  min-height: 260px;
  margin-top: 20px;
  padding: 24px;
  border-radius: 16px;
  background: #f9fafb;
  color: #111827;
  line-height: 1.8;
  white-space: pre-wrap;
}

.post-form {
  margin-top: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.form-group label {
  color: #4b5563;
  font-size: 13px;
  font-weight: 900;
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
  color: #111827;
  font-size: 20px;
}

.comment-form {
  display: grid;
  gap: 10px;
  margin-bottom: 18px;
}

.comment-form button {
  justify-self: end;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-item {
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 14px;
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
  color: #111827;
}

.comment-item span {
  color: #9ca3af;
  font-size: 12px;
}

.comment-item p {
  margin: 0;
  color: #374151;
  line-height: 1.6;
  white-space: pre-wrap;
}

.comment-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 10px;
}

.comment-like-button,
.comment-delete-button,
.comment-edit-button,
.comment-save-button,
.comment-cancel-button {
  border: none;
  background: transparent;
  font-weight: 900;
  cursor: pointer;
  padding: 0;
}

.comment-like-button {
  color: #dc2626;
}

.comment-like-button.liked {
  color: #be123c;
}

.comment-edit-button,
.comment-save-button {
  color: #2563eb;
}

.comment-delete-button {
  color: #dc2626;
}

.comment-cancel-button {
  color: #6b7280;
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

@media (max-width: 960px) {
  .board-tools {
    grid-template-columns: 1fr;
  }

  .detail-header {
    flex-direction: column;
  }

  .detail-actions {
    justify-content: flex-start;
  }

  .col-author,
  .col-number,
  .col-date {
    width: auto;
  }
}
</style>