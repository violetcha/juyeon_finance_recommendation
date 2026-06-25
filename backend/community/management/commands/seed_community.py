import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import UserProfile
from community.models import Post, Comment


User = get_user_model()


ACTIVE_USERS = [
    {
        'username': '주연',
        'password': 'ssafy1234!',
        'age': 25,
        'gender': 'female',
        'main_bank': '신한은행',
        'image': 'profile_images/user01.png',
    },
    {
        'username': '성용',
        'password': 'ssafy1234!',
        'age': 30,
        'gender': 'male',
        'main_bank': '농협은행',
        'image': 'profile_images/user02.png',
    },
    {
        'username': '원근',
        'password': 'ssafy1234!',
        'age': 29,
        'gender': 'male',
        'main_bank': '하나은행',
        'image': 'profile_images/user03.png',
    },
    {
        'username': '성준',
        'password': 'ssafy1234!',
        'age': 27,
        'gender': 'male',
        'main_bank': '우리은행',
        'image': 'profile_images/user04.png',
    },
    {
        'username': '유림',
        'password': 'ssafy1234!',
        'age': 31,
        'gender': 'female',
        'main_bank': 'NH농협은행',
        'image': 'profile_images/user05.png',
    },
    {
        'username': '수진',
        'password': 'ssafy1234!',
        'age': 24,
        'gender': 'female',
        'main_bank': '카카오뱅크',
        'image': 'profile_images/user06.png',
    },
    {
        'username': '희은',
        'password': 'ssafy1234!',
        'age': 28,
        'gender': 'female',
        'main_bank': '토스뱅크',
        'image': 'profile_images/user07.png',
    },
    {
        'username': '진성',
        'password': 'ssafy1234!',
        'age': 30,
        'gender': 'male',
        'main_bank': '하나은행',
        'image': 'profile_images/user08.png',
    },
    {
        'username': '한울',
        'password': 'ssafy1234!',
        'age': 33,
        'gender': 'male',
        'main_bank': '부산은행',
        'image': 'profile_images/user09.png',
    },
    {
        'username': '광주',
        'password': 'ssafy1234!',
        'age': 23,
        'gender': 'female',
        'main_bank': '광주은행',
        'image': 'profile_images/user10.png',
    },
]


CATEGORY_DATA = {
    'free': {
        'titles': [
            '사회초년생 첫 월급 관리 어떻게 하시나요?',
            '주거래은행 정할 때 가장 중요하게 보는 기준',
            '월급 들어오면 자동이체부터 걸어두는 편인가요?',
            '체크카드 혜택도 주거래은행 선택에 영향 있나요?',
            '금융 앱 여러 개 쓰는 분들 관리 팁 궁금해요',
            '은행 앱 UI가 생각보다 중요한 것 같아요',
        ],
        'contents': [
            '요즘 금융생활을 정리해보려고 하는데 생각보다 선택할 게 많네요. 다들 어떤 기준으로 은행을 고르셨는지 궁금합니다.',
            '처음에는 금리만 봤는데, 막상 써보니까 앱 편의성이나 지점 접근성도 꽤 중요하더라고요.',
            '월급일마다 소비가 커지는 편이라 자동저축을 먼저 걸어두는 방식으로 바꿔보려고 합니다.',
            '주거래은행을 하나 정해두면 관리가 편할 것 같은데 아직 어디가 맞는지 고민 중입니다.',
        ],
    },
    'review': {
        'titles': [
            '첫 적금 가입 후기 남겨봅니다',
            '비대면 예금 가입해본 후기',
            '우대금리 조건 맞추는 게 생각보다 어렵네요',
            '자동이체 적금 3개월차 후기',
            '예금 만기까지 유지하는 팁 공유합니다',
            '주거래은행 적금 상품 써본 후기',
        ],
        'contents': [
            '처음에는 금리만 보고 가입했는데 우대조건을 확인하는 게 더 중요하다는 걸 느꼈습니다.',
            '비대면 가입은 생각보다 간단했고, 상품 설명을 비교하면서 보니까 선택하기 편했습니다.',
            '자동이체를 걸어두니 확실히 돈을 덜 쓰게 되는 효과가 있었습니다.',
            '가입 전에는 기간과 중도해지 이율을 꼭 같이 보는 게 좋은 것 같습니다.',
        ],
    },
    'tip': {
        'titles': [
            '적금 시작할 때 금액을 너무 크게 잡지 않는 게 좋은 이유',
            '예금과 적금 차이 쉽게 정리',
            '우대금리 조건 확인할 때 체크할 것들',
            '사회초년생 통장 쪼개기 방법',
            '목돈은 예금, 매달 저축은 적금으로 나누는 방식',
            '금리 비교할 때 최고금리만 보면 안 되는 이유',
        ],
        'contents': [
            '처음부터 무리한 금액으로 적금을 들면 중도해지 가능성이 커져서 유지 가능한 금액이 더 중요합니다.',
            '최고금리보다 내가 실제로 받을 수 있는 우대금리를 기준으로 보는 게 좋습니다.',
            '생활비 통장, 저축 통장, 비상금 통장을 나누면 소비 흐름을 확인하기 편합니다.',
            '금융상품은 만기, 가입금액, 우대조건, 가입방법을 같이 비교해야 실제로 유리한 상품을 고르기 쉽습니다.',
        ],
    },
    'product': {
        'titles': [
            '예금이랑 적금 중에 뭐가 더 나을까요?',
            '월 30만원 저축이면 어떤 상품이 괜찮을까요?',
            '우대금리 조건 없는 상품도 괜찮나요?',
            '주거래은행이랑 금리 높은 은행 중 어디가 나을까요?',
            '중도해지하면 이자가 많이 줄어드나요?',
            '6개월 상품이랑 12개월 상품 중 고민입니다',
        ],
        'contents': [
            '처음 저축을 시작하려고 하는데 예금과 적금 중 어떤 쪽이 더 맞을지 고민입니다.',
            '매달 일정 금액을 넣을 수 있는 상황이라 적금이 좋아 보이는데, 기간을 어떻게 잡아야 할지 모르겠습니다.',
            '우대조건을 맞추기 어려우면 기본금리가 높은 상품을 고르는 게 나을까요?',
            '단기 목표가 있어서 6개월 상품도 보고 있는데 12개월과 차이가 꽤 있네요.',
        ],
    },
}


COMMENT_TEMPLATES = [
    '저도 비슷한 고민을 했는데 조건을 정리해보니까 선택이 쉬워졌어요.',
    '우대금리 조건은 꼭 실제로 달성 가능한지 확인하는 게 좋더라고요.',
    '저는 자동이체를 먼저 걸어두니까 확실히 저축이 쉬워졌습니다.',
    '앱 편의성도 생각보다 중요해서 자주 쓰는 은행 위주로 보게 돼요.',
    '금리만 보지 말고 기간이랑 중도해지 조건도 같이 보는 걸 추천합니다.',
    '처음이면 너무 큰 금액보다 유지 가능한 금액으로 시작하는 게 좋아요.',
    '저도 이 부분 궁금했는데 댓글 참고하고 갑니다.',
    '주거래은행 혜택까지 같이 보면 선택 기준이 더 명확해지는 것 같아요.',
    '비대면 가입 가능한 상품이면 관리가 편해서 좋았습니다.',
    '후기 감사합니다. 저도 비교해보고 결정해야겠네요.',
]


class Command(BaseCommand):
    help = '커뮤니티 발표용 더미 유저, 게시글, 댓글, 좋아요를 생성합니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='기존 커뮤니티 글/댓글과 dummy/active/like 유저를 삭제한 뒤 다시 생성합니다.',
        )

    def handle(self, *args, **options):
        if options['reset']:
            Comment.objects.all().delete()
            Post.objects.all().delete()

            User.objects.filter(username__startswith='active').delete()
            User.objects.filter(username__startswith='like').delete()
            User.objects.filter(username__in=[item['username'] for item in ACTIVE_USERS]).delete()

            self.stdout.write(self.style.WARNING('기존 커뮤니티 더미데이터를 삭제했습니다.'))

        active_users = self.create_active_users()
        like_users = self.create_like_users(count=230)

        posts = self.create_posts(active_users, count=100)
        comments = self.create_comments(active_users, posts)
        self.create_likes(active_users, like_users, posts, comments)

        self.stdout.write(self.style.SUCCESS(f'활성 유저 {len(active_users)}명 생성 완료'))
        self.stdout.write(self.style.SUCCESS(f'좋아요 유저 {len(like_users)}명 생성 완료'))
        self.stdout.write(self.style.SUCCESS(f'게시글 {len(posts)}개 생성 완료'))
        self.stdout.write(self.style.SUCCESS(f'댓글 {len(comments)}개 생성 완료'))
        self.stdout.write(self.style.SUCCESS('커뮤니티 더미데이터 생성 완료'))

    def create_active_users(self):
        users = []

        for item in ACTIVE_USERS:
            user, created = User.objects.get_or_create(
                username=item['username'],
                defaults={
                    'email': f'{item["username"]}@example.com',
                },
            )

            if created:
                user.set_password(item['password'])
                user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.age = item['age']
            profile.gender = item['gender']
            profile.main_bank = item['main_bank']
            profile.monthly_income_range = random.choice([
                '100_200',
                '200_300',
                '300_400',
                '400_500',
            ])
            profile.monthly_saving_amount = random.choice([
                '10_30',
                '30_50',
                '50_100',
                'over_100',
            ])
            profile.lump_sum_amount = random.choice([
                'none',
                '100_500',
                '500_1000',
                '1000_3000',
            ])
            profile.personal_info_agree = True
            profile.profile_image = item['image']
            profile.save()

            users.append(user)

        return users

    def create_like_users(self, count):
        users = []

        for index in range(1, count + 1):
            username = f'like{index:03d}'

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                },
            )

            if created:
                user.set_password('likeuser1234!')
                user.save()

            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'age': random.randint(20, 39),
                    'gender': random.choice(['male', 'female', 'unknown']),
                    'main_bank': random.choice([
                        '국민은행',
                        '신한은행',
                        '하나은행',
                        '우리은행',
                        'NH농협은행',
                        '카카오뱅크',
                        '토스뱅크',
                    ]),
                    'personal_info_agree': True,
                },
            )

            users.append(user)

        return users

    def create_posts(self, users, count):
        posts = []
        categories = ['free', 'review', 'tip', 'product']
        now = timezone.now()

        for index in range(count):
            category = categories[index % len(categories)]
            data = CATEGORY_DATA[category]

            title = random.choice(data['titles'])
            content = random.choice(data['contents'])

            post = Post.objects.create(
                user=random.choice(users),
                title=f'{title}',
                content=content,
                category=category,
                view_count=random.randint(15, 3800),
            )

            created_at = now - timedelta(
                days=random.randint(0, 35),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            Post.objects.filter(id=post.id).update(
                created_at=created_at,
                updated_at=created_at + timedelta(minutes=random.randint(0, 180)),
            )

            posts.append(post)

        return posts

    def create_comments(self, users, posts):
        comments = []
        now = timezone.now()

        for post in posts:
            comment_count = random.randint(1, 7)

            for _ in range(comment_count):
                comment = Comment.objects.create(
                    user=random.choice(users),
                    post=post,
                    content=random.choice(COMMENT_TEMPLATES),
                )

                created_at = post.created_at + timedelta(
                    minutes=random.randint(5, 2400),
                )

                if created_at > now:
                    created_at = now - timedelta(minutes=random.randint(1, 60))

                Comment.objects.filter(id=comment.id).update(
                    created_at=created_at,
                )

                comments.append(comment)

        return comments

    def create_likes(self, active_users, like_users, posts, comments):
        all_like_users = active_users + like_users

        popular_posts = random.sample(posts, min(8, len(posts)))
        normal_posts = [post for post in posts if post not in popular_posts]

        for post in popular_posts:
            like_count = random.randint(180, 225)
            selected_users = random.sample(all_like_users, min(like_count, len(all_like_users)))
            post.likes.set(selected_users)

        for post in normal_posts:
            like_count = random.randint(0, 65)
            selected_users = random.sample(all_like_users, min(like_count, len(all_like_users)))
            post.likes.set(selected_users)

        popular_comments = random.sample(comments, min(20, len(comments)))

        for comment in popular_comments:
            like_count = random.randint(15, 90)
            selected_users = random.sample(all_like_users, min(like_count, len(all_like_users)))
            comment.likes.set(selected_users)

        for comment in comments:
            if comment in popular_comments:
                continue

            like_count = random.randint(0, 18)
            selected_users = random.sample(all_like_users, min(like_count, len(all_like_users)))
            comment.likes.set(selected_users)