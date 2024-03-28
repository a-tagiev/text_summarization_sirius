import vk_api

main_token = "vk1.a.EWzgRDyuBxOuLGtHqS-S6vwyjGKZWsWjJ3WbyY2AhHJhfO_AszbEV1oDIXk83zX62zekUZzGNyS8qzXT1bvjH7kHyGWomE3KOzwmRQePJyXizInKu46W3vR6mXVWacdShVwYQpyCbYRBIp1pq1qI28IggEU3pUcCmhI17XmlThlDiDrB6xR5AzDf7W-ZmNQd-VZZBvJ6hi6Mx97_J2_kRw"

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()


def sender(peer_id, message):
    vk.messages.send(peer_id=peer_id, message=message, random_id=0)
