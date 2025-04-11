# # e2eテスト用だが、このテストケースはほぼつかわない
# # e2eテスト中の接続先DBを確認するためのみ
# import pytest
# from playwright.sync_api import Page, expect
# from django.db import connection

# def test_which_db_connectiong(page: Page):
#     # このテストケース中に接続しているDB名の確認
#     print("接続中のデータベース名:", connection.settings_dict["NAME"])
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT current_database();")
#         db_name = cursor.fetchone()[0]
#         # SQLでもDB名を確認
#         print("current_database() =", db_name)