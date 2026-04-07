from django.test import TestCase
from django.urls import reverse
from django.conf import settings  # settingsをインポート
from members.models import User
from mail.models import Message, ToGroup
from django.utils import timezone


class InboxViewTests(TestCase):
    def setUp(self):
        # テスト用ユーザーを作成
        self.user_2025 = User.objects.create_user(
            email="testuser2025@example.com",
            year=2025,
        )
        self.user_2025.fullname = "Test User 2025"
        self.user_2025.furigana = "てすとゆーざー"
        self.user_2025.save()

        self.user_2024 = User.objects.create_user(
            email="testuser2024@example.com", year=2024
        )
        self.user_2024.fullname = "Test User 2024"
        self.user_2024.furigana = "てすとゆーざー"
        self.user_2024.save()

        # ToGroup 作成
        self.group_2025 = ToGroup.objects.create(year=2025, label="2025年度メンバー")
        self.group_2024 = ToGroup.objects.create(year=2024, label="2024年度メンバー")
        self.group_all = ToGroup.objects.create(
            year=0, label="全体メーリス"
        )  # 全体向けグループ

        # メッセージを作成 (異なるグループ向け)
        self.message_2025 = Message.objects.create(
            title="2025向けのお知らせ",
            content="これは2025年度向けのメッセージです。",
            sender=self.user_2025,
            writer=self.user_2025,
            created_at=timezone.now(),
        )
        self.message_2025.to_groups.add(self.group_2025)

        self.message_2024 = Message.objects.create(
            title="2024向けのお知らせ",
            content="これは2024年度向けのメッセージです。",
            sender=self.user_2024,
            writer=self.user_2024,
            created_at=timezone.now(),
        )
        self.message_2024.to_groups.add(self.group_2024)

        self.message_all = Message.objects.create(
            title="全体向けのお知らせ",
            content="これは全体向けのメッセージです。",
            sender=self.user_2025,
            writer=self.user_2025,
            created_at=timezone.now(),
        )
        self.message_all.to_groups.add(self.group_all)

        # sender/writerが異なるyearを持つメッセージ
        self.other_year_message = Message.objects.create(
            title="異なるyearのメッセージ",
            content="これは異なるyearですが、senderおよびwriterです。",
            sender=self.user_2025,  # ユーザーがsender
            writer=self.user_2025,  # ユーザーがwriter
            created_at=timezone.now(),
        )
        self.other_year_message.to_groups.add(self.group_2024)  # 異なるグループに紐づけ

        # ビューのURL
        self.inbox_url = reverse("mail:inbox")

    def create_sender_messages(self, count, title_prefix="sender", content="共通本文"):
        messages = []
        for index in range(count):
            message = Message.objects.create(
                title=f"{title_prefix} {index}",
                content=content,
                sender=self.user_2025,
                writer=self.user_2025,
                created_at=timezone.now(),
            )
            message.to_groups.add(self.group_2025)
            messages.append(message)
        return messages

    # 1. 正しいyearのメッセージが表示されるか
    def test_inbox_displays_correct_messages_for_user_year(self):
        """ユーザーのyearに一致するメッセージだけ表示される"""
        self.client.force_login(self.user_2025)
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2025向けのお知らせ")
        self.assertContains(response, "全体向けのお知らせ")  # 全体向けは常に表示
        self.assertNotContains(
            response, "2024向けのお知らせ"
        )  # 異なるyearのメッセージは非表示

    # 2. 全体メーリスが表示される
    def test_inbox_displays_general_messages(self):
        """全体メーリス (year=0) のメッセージは誰にでも表示される"""
        self.client.force_login(self.user_2024)
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "全体向けのお知らせ")

    # 3. 年度が一致しないメッセージは表示されない
    def test_inbox_does_not_display_messages_for_other_years(self):
        """ユーザーのyearと一致しないメッセージは表示されない"""
        self.client.force_login(self.user_2024)
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "2025向けのお知らせ")

    # 4. senderまたはwriterの場合はyearが異なっていても表示される
    def test_inbox_displays_messages_if_user_is_sender_or_writer(self):
        """ユーザーがsenderまたはwriterの場合、yearが異なっていてもメッセージが表示される"""
        self.client.force_login(self.user_2025)
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "異なるyearのメッセージ")

    # 5. 最新順にソートされているか
    def test_inbox_messages_are_sorted_by_created_at(self):
        """メッセージは作成日時の新しい順に表示される"""
        self.client.force_login(self.user_2025)
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["mailis"])
        created_at_list = [message.created_at for message in messages]
        self.assertEqual(created_at_list, sorted(created_at_list, reverse=True))

    def test_inbox_query_zenkai_displays_only_global_messages(self):
        self.client.force_login(self.user_2025)
        response = self.client.get(self.inbox_url, {"query": "zenkai"})

        self.assertEqual(response.status_code, 200)
        messages = list(response.context["mailis"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], self.message_all)

    def test_inbox_query_sender_displays_only_sender_or_writer_messages(self):
        self.client.force_login(self.user_2025)
        response = self.client.get(self.inbox_url, {"query": "sender"})

        self.assertEqual(response.status_code, 200)
        messages = list(response.context["mailis"])
        self.assertIn(self.message_2025, messages)
        self.assertIn(self.message_all, messages)
        self.assertIn(self.other_year_message, messages)
        self.assertNotIn(self.message_2024, messages)

    def test_inbox_text_search_with_multiple_words_uses_and_condition(self):
        target = Message.objects.create(
            title="特別 キーワード",
            content="青い 空",
            sender=self.user_2025,
            writer=self.user_2025,
            created_at=timezone.now(),
        )
        target.to_groups.add(self.group_2025)
        Message.objects.create(
            title="特別だけ",
            content="青い海",
            sender=self.user_2025,
            writer=self.user_2025,
            created_at=timezone.now(),
        ).to_groups.add(self.group_2025)

        self.client.force_login(self.user_2025)
        response = self.client.get(self.inbox_url, {"text": "特別 青い"})

        self.assertEqual(response.status_code, 200)
        messages = list(response.context["mailis"])
        self.assertIn(target, messages)
        self.assertEqual(sum(1 for m in messages if m.title == "特別 キーワード"), 1)

    def test_inbox_distinct_prevents_duplicate_messages(self):
        duplicated = Message.objects.create(
            title="重複防止メッセージ",
            content="同じメッセージが重複しない",
            sender=self.user_2025,
            writer=self.user_2025,
            created_at=timezone.now(),
        )
        duplicated.to_groups.add(self.group_2025, self.group_all)

        self.client.force_login(self.user_2025)
        response = self.client.get(self.inbox_url)

        self.assertEqual(response.status_code, 200)
        messages = list(response.context["mailis"])
        self.assertEqual(sum(1 for m in messages if m.id == duplicated.id), 1)

    def test_inbox_pagination_links_preserve_query_and_text(self):
        self.create_sender_messages(12, title_prefix="特定語", content="検索対象")

        self.client.force_login(self.user_2025)
        response = self.client.get(
            self.inbox_url,
            {"query": "sender", "text": "特定語"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "?query=sender&amp;text=%E7%89%B9%E5%AE%9A%E8%AA%9E&amp;page=2")
        self.assertEqual(response.context["preserved_query"], "query=sender&text=%E7%89%B9%E5%AE%9A%E8%AA%9E")

    def test_inbox_pagination_second_page_keeps_filters(self):
        matching_messages = self.create_sender_messages(
            12, title_prefix="特定語", content="絞り込み対象"
        )
        self.create_sender_messages(3, title_prefix="別件", content="対象外")

        self.client.force_login(self.user_2025)
        response = self.client.get(
            self.inbox_url,
            {"query": "sender", "text": "特定語", "page": 2},
        )

        self.assertEqual(response.status_code, 200)
        page_messages = list(response.context["mailis"])
        self.assertEqual(response.context["mailis"].number, 2)
        self.assertEqual(response.context["preserved_query"], "query=sender&text=%E7%89%B9%E5%AE%9A%E8%AA%9E")
        self.assertEqual(len(page_messages), len(matching_messages) - 10)
        self.assertTrue(all("特定語" in message.title for message in page_messages))

    def test_inbox_pagination_links_preserve_text_only(self):
        self.create_sender_messages(12, title_prefix="検索語", content="本文")

        self.client.force_login(self.user_2025)
        response = self.client.get(self.inbox_url, {"text": "検索語"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "?text=%E6%A4%9C%E7%B4%A2%E8%AA%9E&amp;page=2")
        self.assertNotContains(response, "?text=%E6%A4%9C%E7%B4%A2%E8%AA%9E&amp;page=2&amp;page=")

    def test_inbox_pagination_links_preserve_query_only(self):
        for index in range(12):
            message = Message.objects.create(
                title=f"全体連絡 {index}",
                content="全回向け",
                sender=self.user_2024,
                writer=self.user_2024,
                created_at=timezone.now(),
            )
            message.to_groups.add(self.group_all)

        self.client.force_login(self.user_2025)
        response = self.client.get(self.inbox_url, {"query": "zenkai"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "?query=zenkai&amp;page=2")
        self.assertEqual(response.context["preserved_query"], "query=zenkai")

    def test_inbox_pagination_links_without_filters_use_only_page_param(self):
        self.create_sender_messages(12, title_prefix="通常一覧", content="本文")

        self.client.force_login(self.user_2025)
        response = self.client.get(self.inbox_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "?page=2")
        self.assertEqual(response.context["preserved_query"], "")
