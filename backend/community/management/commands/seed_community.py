from datetime import timedelta
import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from community.models import Post, Comment


class Command(BaseCommand):
    help = '커뮤니티 더미 게시글 30개를 생성합니다.'

    def handle(self, *args, **options):
        User = get_user_model()

        users_data = [
            ('admin', '관리자'),
            ('minji', '김민지'),
            ('seoyun', '이서윤'),
            ('hyunwoo', '박현우'),
            ('jiyoon', '최지윤'),
            ('junho', '정준호'),
        ]

        users = []

        for username, nickname in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'is_active': True,
                }
            )

            if created:
                user.set_password('1234')
                user.save()

            users.append(user)

        dummy_posts = [
            {
                'category': 'product',
                'title': '사회초년생 첫 적금 추천 부탁드려요',
                'content': '첫 월급을 받기 시작해서 매달 30만 원 정도 적금하려고 합니다. 12개월 정도 생각 중인데 우대조건이 너무 복잡하지 않은 상품이 좋을까요?',
            },
            {
                'category': 'free',
                'title': '주거래은행을 꼭 정해야 할까요?',
                'content': '은행을 여러 개 쓰고 있는데 주거래은행을 정하는 게 실제로 혜택이 큰지 궁금합니다. 급여이체 은행을 기준으로 정하는 게 좋을까요?',
            },
            {
                'category': 'review',
                'title': '모바일로 예금 가입해본 후기',
                'content': '영업점 방문 없이 앱으로 예금 가입했는데 생각보다 간단했습니다. 다만 우대금리 조건은 자세히 읽어봐야겠더라고요.',
            },
            {
                'category': 'tip',
                'title': '예금이랑 적금 차이 간단 정리',
                'content': '예금은 목돈을 한 번에 넣는 방식이고, 적금은 매달 나눠서 넣는 방식입니다. 목돈이 있으면 예금, 매달 모으는 중이면 적금이 더 적합한 것 같아요.',
            },
            {
                'category': 'product',
                'title': '우대조건 없는 예금 상품 괜찮나요?',
                'content': '최고금리는 낮아도 우대조건이 없는 상품이 더 마음 편할 것 같아요. 실제로 최고금리보다 기본금리를 보는 게 맞을까요?',
            },
            {
                'category': 'review',
                'title': '우리은행 WON플러스예금 살펴봤어요',
                'content': '가입기간 선택 폭이 넓고 우대조건이 없어서 단순한 상품을 원하는 사람에게 괜찮아 보였습니다. 12개월 금리가 제일 괜찮더라고요.',
            },
            {
                'category': 'free',
                'title': '월급통장과 적금 은행을 같은 곳으로 해야 할까요?',
                'content': '월급통장은 신한인데 적금은 국민은행 상품이 더 좋아 보입니다. 주거래은행 혜택 생각하면 같은 은행이 나을지 고민입니다.',
            },
            {
                'category': 'tip',
                'title': '적금 가입 전에 확인할 것들',
                'content': '가입기간, 기본금리, 최고우대금리, 우대조건, 중도해지이율은 꼭 확인해야 합니다. 특히 최고금리는 조건을 달성해야 받을 수 있습니다.',
            },
            {
                'category': 'product',
                'title': '6개월 단기 적금 추천 가능할까요?',
                'content': '여행자금 마련용으로 6개월만 모으고 싶습니다. 12개월 상품이 많던데 6개월 상품도 괜찮은 게 있을까요?',
            },
            {
                'category': 'free',
                'title': '금융 초보인데 예금부터 시작해도 될까요?',
                'content': '투자는 아직 무섭고 예금이나 적금부터 시작하려고 합니다. 금리가 엄청 높진 않아도 안정적인 게 좋습니다.',
            },
            {
                'category': 'review',
                'title': '농협 적금 가입 후기',
                'content': '농협을 주거래은행으로 쓰고 있어서 적금을 찾아봤습니다. 영업점도 근처에 있고 앱도 자주 써서 관리하기 편했습니다.',
            },
            {
                'category': 'tip',
                'title': '우대금리 조건 중 쉬운 조건',
                'content': '마케팅 동의, 앱 가입, 자동이체 등록 같은 조건은 비교적 쉬운 편입니다. 급여이체나 카드 실적은 사람마다 달성 가능성이 다를 수 있습니다.',
            },
            {
                'category': 'product',
                'title': '주거래은행 상품만 추천받는 게 좋을까요?',
                'content': '주거래은행은 하나은행인데 전체 은행 상품을 보면 더 높은 금리도 있어서 고민됩니다. 주거래은행 우선 추천이 더 현실적인 것 같기도 합니다.',
            },
            {
                'category': 'free',
                'title': '월 저축 가능 금액은 얼마가 적당할까요?',
                'content': '월급 250만 원 정도인데 월 50만 원 저축은 부담될까요? 처음에는 30만 원 정도로 시작하는 게 나을지 고민입니다.',
            },
            {
                'category': 'review',
                'title': '카드 실적 우대조건은 생각보다 어렵네요',
                'content': '적금 우대금리에 카드 실적 조건이 있었는데 매달 30만 원 이상 쓰는 게 생각보다 부담됐습니다. 기본금리도 같이 보는 게 중요한 것 같아요.',
            },
            {
                'category': 'tip',
                'title': '사회초년생은 비상금도 따로 필요합니다',
                'content': '적금에 모든 돈을 넣기보다 바로 꺼낼 수 있는 비상금도 필요합니다. 생활비 2~3개월 정도는 남겨두는 게 좋다고 생각합니다.',
            },
            {
                'category': 'product',
                'title': '청년 대상 우대 적금 조건 궁금합니다',
                'content': '나이 조건이 있는 적금들이 있던데 만 34세 이하 같은 조건이 많더라고요. 이런 조건은 자동으로 추천에 반영되면 좋겠습니다.',
            },
            {
                'category': 'free',
                'title': '은행 앱 편의성도 중요한 것 같아요',
                'content': '금리만 보고 가입했다가 앱이 불편하면 관리하기 어렵더라고요. 모바일 가입 가능 여부도 추천 기준에 들어가면 좋을 것 같습니다.',
            },
            {
                'category': 'review',
                'title': '12개월 적금 만기 후기',
                'content': '처음에는 1년이 길게 느껴졌는데 자동이체로 해두니까 생각보다 잘 모였습니다. 초보자는 12개월 적금이 무난한 것 같아요.',
            },
            {
                'category': 'tip',
                'title': '기본금리와 최고금리 차이',
                'content': '기본금리는 별도 조건 없이 적용되는 금리이고, 최고금리는 우대조건을 모두 만족했을 때 받을 수 있는 금리입니다. 조건을 못 맞추면 실제 이자는 낮아질 수 있습니다.',
            },
            {
                'category': 'product',
                'title': '목돈 500만 원은 예금이 나을까요?',
                'content': '현재 500만 원 정도 모아둔 돈이 있습니다. 매달 추가 저축보다는 목돈을 1년 정도 묶어두는 예금이 나을지 궁금합니다.',
            },
            {
                'category': 'free',
                'title': '급여이체 은행을 바꾸는 게 귀찮네요',
                'content': '우대금리 때문에 급여이체 은행을 바꾸라고 하는 상품이 많은데 절차가 번거로울 것 같습니다. 이런 조건은 사람마다 다르게 봐야 할 것 같아요.',
            },
            {
                'category': 'review',
                'title': '비대면 가입 상품이 편했습니다',
                'content': '은행 방문할 시간이 없어서 비대면 가입 가능한 상품 위주로 봤습니다. 사회초년생에게는 모바일 가입 여부가 꽤 중요하다고 느꼈습니다.',
            },
            {
                'category': 'tip',
                'title': '저축 기간은 너무 길게 잡지 않아도 됩니다',
                'content': '처음부터 36개월 상품을 가입하면 중간에 해지할 가능성이 있습니다. 처음에는 6개월이나 12개월부터 시작하는 것도 괜찮습니다.',
            },
            {
                'category': 'product',
                'title': '하나은행 적금 중 간단한 상품 있나요?',
                'content': '하나은행을 주거래은행으로 쓰고 있습니다. 우대조건이 단순하고 모바일 가입 가능한 적금 상품을 찾고 있습니다.',
            },
            {
                'category': 'free',
                'title': '금리가 조금 낮아도 조건 쉬운 상품이 좋네요',
                'content': '최고금리가 높아도 조건을 못 맞추면 의미가 없더라고요. 저는 조건이 쉬운 상품을 선호합니다.',
            },
            {
                'category': 'review',
                'title': '예금 상세 페이지 비교하기 좋네요',
                'content': '가입방법, 가입대상, 우대조건, 기간별 금리가 한 번에 보여서 좋았습니다. 추천 근거까지 붙으면 더 이해하기 쉬울 것 같아요.',
            },
            {
                'category': 'tip',
                'title': '주거래은행 추천과 상품 추천을 같이 보면 좋을 듯',
                'content': '집 근처 은행, 앱 편의성, 예적금 상품 조건을 같이 보면 주거래은행 선택에 도움이 될 것 같습니다.',
            },
            {
                'category': 'product',
                'title': '국민은행 예금 상품 추천 부탁드립니다',
                'content': '국민은행을 주로 쓰고 있어서 국민은행 예금 상품만 보고 싶습니다. 12개월 기준으로 괜찮은 상품이 있을까요?',
            },
            {
                'category': 'free',
                'title': '커뮤니티에서 가입 후기 많이 공유되면 좋겠어요',
                'content': '금융상품은 설명만 보면 어렵기 때문에 실제 가입 후기나 우대조건 달성 경험이 많이 공유되면 좋겠습니다.',
            },
        ]

        comment_samples = [
            '저도 비슷한 고민 중입니다.',
            '기본금리도 꼭 확인해보세요.',
            '우대조건이 쉬운 상품이 실제로는 더 편하더라고요.',
            '12개월 상품이 처음 시작하기에는 무난한 것 같아요.',
            '주거래은행 우선 추천 기능이 있으면 좋겠네요.',
            '모바일 가입 가능한 상품을 먼저 보는 걸 추천합니다.',
            '카드 실적 조건은 생각보다 달성하기 어려울 수 있어요.',
            '저는 예금보다 적금부터 시작했습니다.',
            '상품 상세에서 우대조건을 잘 읽어보는 게 중요합니다.',
            '좋은 정보 감사합니다.',
        ]

        created_count = 0

        for index, post_data in enumerate(dummy_posts):
            user = users[index % len(users)]

            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'user': user,
                    'category': post_data['category'],
                    'content': post_data['content'],
                    'view_count': random.randint(0, 80),
                }
            )

            if not created:
                post.category = post_data['category']
                post.content = post_data['content']
                post.view_count = random.randint(0, 80)
                post.user = user
                post.save()

            created_count += 1

            created_at = timezone.now() - timedelta(days=random.randint(0, 14), hours=random.randint(0, 23))
            Post.objects.filter(id=post.id).update(
                created_at=created_at,
                updated_at=created_at,
            )

            post.comments.all().delete()

            comment_count = random.randint(0, 4)

            for _ in range(comment_count):
                comment_user = random.choice(users)
                comment = Comment.objects.create(
                    user=comment_user,
                    post=post,
                    content=random.choice(comment_samples),
                )

                comment_created_at = created_at + timedelta(hours=random.randint(1, 20))
                Comment.objects.filter(id=comment.id).update(
                    created_at=comment_created_at,
                )

                if hasattr(comment, 'likes'):
                    like_users = random.sample(users, random.randint(0, min(3, len(users))))

                    for like_user in like_users:
                        comment.likes.add(like_user)

            if hasattr(post, 'likes'):
                post.likes.clear()
                like_users = random.sample(users, random.randint(0, min(5, len(users))))

                for like_user in like_users:
                    post.likes.add(like_user)

        self.stdout.write(
            self.style.SUCCESS(f'커뮤니티 더미 게시글 {created_count}개 생성 완료')
        )
        self.stdout.write(
            self.style.SUCCESS('더미 유저 비밀번호는 모두 1234 입니다.')
        )