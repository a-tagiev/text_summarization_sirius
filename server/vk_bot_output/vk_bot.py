import vk_api

main_token = "vk1.a.22r2Or2m_5-ZpzDxkuhh-FcS1Cja56dfQXwgchZCMbBQNFQY-IROuV_eLJTCVEplutDVDGl7B8iYKoJs6fTrZWvlOQxbG2VtTuL5ubZfpPZ6BB3_kq-rD3En1JQXMbl2t_etlpE-lnUDzV06Nytcbz_KjBwQh_qxR1uSJF6VcMuLr_B5aRVCdQkwoXf_6kwQwgJ-aMpKyVxFsKqnxHlkpQ"

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()


def sender(peer_id, message):
    vk.messages.send(peer_id=peer_id, message=message, random_id=0)
