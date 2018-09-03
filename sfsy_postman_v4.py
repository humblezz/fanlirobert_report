import requests
import time
import re
import json
import random

class SFReg(object):
    def __init__(self):
        self.jiema_code = {
            "1001": "����token����Ϊ��",
            "1002": "����action����Ϊ��",
            "1003": "����action����",
            "1004": "tokenʧЧ",
            "1005": "�û������������",
            "1006": "�û�������Ϊ��",
            "1007": "���벻��Ϊ��",
            "1008": "�˻�����",
            "1009": "�˻�������",
            "1010": "��������",
            "1011": "�˻������",
            "1012": "��¼���ﵽ����",
            "2001": "����itemid����Ϊ��",
            "2002": "��Ŀ������",
            "2003": "��Ŀδ����",
            "2004": "��ʱû�п��õĺ���",
            "2005": "��ȡ���������Ѵﵽ����",
            "2006": "����mobile����Ϊ��",
            "2007": "�����ѱ��ͷ�",
            "2008": "����������",
            "2009": "�������ݲ���Ϊ��",
            "2010": "��������ʹ����",
            "3001": "��δ�յ�����",
            "3002": "�ȴ�����",
            "3003": "���ڷ���",
            "3004": "����ʧ��",
            "3005": "����������",
            "3006": "ר��ͨ��������",
            "3007": "ר��ͨ��δ����",
            "3008": "ר��ͨ����������Ŀ��ƥ��",
            "9001": "ϵͳ����",
            "9002": "ϵͳ�쳣",
            "9003": "ϵͳ��æ",
            "": "���󷵻�Ϊ��"
        }

        self.USER_AGENTS=["Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.17 NetType/WIFI Language/zh_HK",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.16 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0; MX6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A405 MicroMessenger/6.5.15 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; VTR-AL00 Build/HUAWEIVTR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 wxwork/2.1.3 MicroMessenger/6.3.22",
            "Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 wxwork/2.1.3 MicroMessenger/6.3.22",
            "Mozilla/5.0 (Linux; Android 5.1; m3 note Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 wxwork/2.1.3 MicroMessenger/6.3.22",
            "Mozilla/5.0 (Linux; Android 6.0; MX6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 wxwork/2.1.3 MicroMessenger/6.3.22",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 wxwork/2.1.5 MicroMessenger/6.3.22",
            "Mozilla/5.0 (Linux; Android 7.0; EVA-AL00 Build/HUAWEIEVA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A402 MicroMessenger/6.5.16 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A402 wxwork/2.1.5 MicroMessenger/6.3.22",
            "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 5.1; vivo X6D Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Mobile/14F89 MicroMessenger/6.5.16 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; EVA-AL10 Build/HUAWEIEVA-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0; ALE-TL00 Build/HuaweiALE-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; WAS-AL00 Build/HUAWEIWAS-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E277 MicroMessenger/6.5.16 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.17 NetType/WIFI Language/en",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.15 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 4.4.2; Coolpad 8675 Build/KOT49H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.3.18.800 NetType/cmnet Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; vivo X9i Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0; Redmi Note 4 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.17 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.7 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0; M5 Note Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A3000 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 8.0; G8342 Build/47.1.A.2.324; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.14.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.17 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; EVA-TL00 Build/HUAWEIEVA-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.16 NetType/4G Language/zh_TW",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.5.16 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0; EVA-TL00 Build/HUAWEIEVA-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; SM-C5000 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 MicroMessenger/6.5.15 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; FRD-AL00 Build/HUAWEIFRD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; vivo X9Plus Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Mobile/14F89 MicroMessenger/6.5.16 NetType/3G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; MI 5 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; HTC A9w Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 MicroMessenger/6.5.17 NetType/3G Language/en",
            "Mozilla/5.0 (Linux; Android 5.1.1; Redmi Note 3 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; PRA-AL00X Build/HONORPRA-AL00X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; SM-C5000 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.15 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.1.1; vivo X9i Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.4.1000 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.16 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 wxwork/2.1.5 MicroMessenger/6.3.22",
            "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0; NEM-AL10 Build/HONORNEM-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.1.1; vivo X9i Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.10 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1080 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0; Redmi Note 4X Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.8 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.17 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 5.1.1; Redmi Note 3 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.15 NetType/4G Language/en",
            "Mozilla/5.0 (Linux; Android 7.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; MI 5s Plus Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.16 NetType/2G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 MicroMessenger/6.5.16 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 MicroMessenger/6.5.10.1060 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.16 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.16 NetType/4G Language/zh_HK",
            "Mozilla/5.0 (Linux; Android 6.0; MI 5 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 5.1; CUN-TL00 Build/HUAWEICUN-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0; PLK-AL10 Build/HONORPLK-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.16 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11t Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304 MicroMessenger/6.5.15 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13E238 MicroMessenger/6.5.15 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0; 1505-A01 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.5.5 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 5.1; CUN-TL00 Build/HUAWEICUN-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; SM-C5000 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 MicroMessenger/6.5.16 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 5.0.2; HTC_E9x Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/3G Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.16 NetType/4G Language/en",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A452 MicroMessenger/6.5.15 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; Mi Note 2 Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; EVA-AL00 Build/HUAWEIEVA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; MI 5s Plus Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 5.1; OPPO R9tm Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; KNT-AL10 Build/HUAWEIKNT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; EVA-DL00 Build/HUAWEIEVA-DL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; STF-AL00 Build/HUAWEISTF-AL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone 92; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.7.2 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "MQQBrowser/5.3/Mozilla/5.0 (Linux; Android 6.0; TCL 580 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone 92; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.7.2 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (Linux; Android 7.0; FRD-AL00 Build/HUAWEIFRD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.1.0_0_TIM_D TIM2.0/1.2.0.1692 QQ/6.5.5  NetType/2G WebP/0.3.0 Pixel/1080 IMEI/869953022249635",
            "Mozilla/5.0 (iPhone 91; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14C92 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; MX5 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; NX531J Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.8 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone 6; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/6.0 MQQBrowser/6.6.1 Mobile/13E238 Safari/8536.25",
            "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; EVA-DL00 Build/HUAWEIEVA-DL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 4.4.4; HM NOTE 1LTE Build/KTU84P; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_6.6.9_482_YYB_D QQ/6.6.9.3060 NetType/WIFI WebP/0.3.0 Pixel/720",
            "Mozilla/5.0 (Linux; Android 7.0; MIX Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/WIFI WebP/0.3.0 Pixel/1080",
            "Mozilla/5.0 (Linux; Android 5.1; OPPO R9m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080",
            "Mozilla/5.0 (Linux; Android 7.1.1; NX563J Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080",
            "Mozilla/5.0 (Linux; Android 5.1; vivo X6Plus D Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080",
            "Mozilla/5.0 (Linux; Android 7.0; ZUK Z2121 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080",
            "Mozilla/5.0 (iPhone 6p; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; SM-G9550 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone 6sp; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.8.0 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (iPhone 6p; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 MQQBrowser/7.8.0 Mobile/12B436 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/WIFI WebP/0.3.0 Pixel/720",
            "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; KIW-CL00 Build/HONORKIW-CL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 6.0.1; MI 4LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.1.5_708_YYB_D QQ/7.1.5.3215 NetType/4G WebP/0.3.0 Pixel/1080",
            "Mozilla/5.0 (Linux; Android 6.0.1; MI 5s Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/WIFI WebP/0.3.0 Pixel/1080",
            "Mozilla/5.0 (Linux; Android 7.0; HUAWEI CAZ-AL10 Build/HUAWEICAZ-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.1.0_692_YYB_D QQ/7.1.0.3175 NetType/WIFI WebP/0.3.0 Pixel/1080",
            "Mozilla/5.0 (iPhone 6s; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 MQQBrowser/7.8.0 Mobile/13F69 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (iPhone 6s; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/6.0 MQQBrowser/6.9 Mobile/14B100 Safari/8536.25 MttCustomUA/2",
            "Mozilla/5.0 (iPhone 92; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.2.1 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1",
            "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; HUAWEI MT7-CL00 Build/HuaweiMT7-CL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.3 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone 92; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.8.0 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MHA-AL00 Build/HUAWEIMHA-AL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; WAS-AL00 Build/HUAWEIWAS-AL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; WAS-TL10 Build/HUAWEIWAS-TL10) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; H60-L01 Build/HDH60-L01) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.2 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; HUAWEI VNS-DL00 Build/HUAWEIVNS-DL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone 5SGLOBAL; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 MQQBrowser/7.2 Mobile/13A404 Safari/8536.25 MttCustomUA/2 QBWebViewType/1",
            "Mozilla/5.0 (iPhone 6s; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.7.2 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1",
            "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; vivo Y66L Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.7 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; vivo Y67 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.2 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; Redmi Note 3 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; Lenovo K32c36 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone 6; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.7.2 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MIX Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; PRO 6 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; KING 7S Build/PP6000_230I) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; SM-G9300 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.2 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone 5; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.7.2 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI CAZ-AL10 Build/HUAWEICAZ-AL10) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone 6p; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 MQQBrowser/7.7.2 Mobile/13G36 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; DUK-AL20 Build/HUAWEIDUK-AL20) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (iPad; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.4.1 Mobile/14E277 Safari/8536.25 MttCustomUA/2 QBWebViewType/1",
            "Mozilla/5.0 (iPad; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.4.1 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (iPad; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.4.1 Mobile/14F89 Safari/8536.25",
            "Mozilla/5.0 (iPad; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.4.1 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1",
            "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; lephone W7 Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone 5SGLOBAL; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.7.2 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (iPad; CPU iPhone OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.4.1 Mobile/14B72 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (iPad; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.4.1 Mobile/14C92 Safari/8536.25 MttCustomUA/2 QBWebViewType/1",
            "Mozilla/5.0 (iPad; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 MQQBrowser/7.4.1 Mobile/13F69 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (iPhone 91; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.2.1 Mobile/14A346 Safari/8536.25 MttCustomUA/2 QBWebViewType/1",
            "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; PE-CL00 Build/HuaweiPE-CL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.0 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone 6sp; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.7.2 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (iPhone 92; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.4.1 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (Linux; Android 6.0; Le X620 Build/HEXCNFN5902606111S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043507 Safari/537.36 V1_AND_SQ_7.1.8_718_YYB_D QQ/7.1.8.3240 NetType/WIFI WebP/0.3.0 Pixel/1080",
            "Mozilla/5.0 (iPhone 92; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.7.2 Mobile/14B100 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; STF-AL00 Build/HUAWEISTF-AL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; KIW-CL00 Build/HONORKIW-CL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36"
        ]

        self.sms_headers = {
            'cache-control': "no-cache",
            'postman-token': "87406b65-75a6-d843-cd8e-cac1c4eaefea",
            'user-agent':self.USER_AGENTS[random.randint(0, len(self.USER_AGENTS))]
        }

    def login_jiema(self, jiema_account, jiema_password, invite_code):
        self.invite_code = invite_code
        self.jiema_account = jiema_account
        self.jiema_token = ""
        login_jiema_url = "http://api.fxhyd.cn/UserInterface.aspx"
        querystring = {
            "action": "login",
            "username": jiema_account,
            "password": jiema_password
        }
        response = requests.request("GET", login_jiema_url, headers=self.sms_headers,  params=querystring)
        if 'success' in response.text:
            self.jiema_token = response.text.split('|')[1]
            print('����ƽ̨��¼�ɹ�token:' + self.jiema_token)
        return self.jiema_token

    # ��ȡ�ֻ�����
    def get_phone_number(self):
        get_jiema_phonenumber_url = "http://api.fxhyd.cn/UserInterface.aspx"
        querystring = {
            "action": "getmobile",
            "token": self.jiema_token,
            "itemid": "1333",
            "excludeno": "170.171.180",
            "isp": 1
        }
        response = requests.request(
            "POST",
            get_jiema_phonenumber_url,
            headers=self.sms_headers,
            params=querystring)
        self.phone_num = ''
        if 'success' in response.text:
            self.phone_num = response.text.split('|')[1]
            print("��ȡ���ֻ����룺" + self.phone_num)
        return self.phone_num

    # ��ȡhttp����
    def get_proxy(self):
        self.headers = {
            'host':"s.sfddj.com",
            'user-agent':self.USER_AGENTS[random.randint(0, len(self.USER_AGENTS))],
            'accept': "*/*",
            'path': '/fxfront/loginapp/sendAppLoginCode?appid=APPID',
            'accept-language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            'accept-encoding':"gzip, deflate, br",
            'referer':"https://s.sfddj.com/Shop/WebApp/app_share_down.html?sell_member_id="+ self.invite_code,
            'content-type':"application/x-www-form-urlencoded; charset=UTF-8",
            'connection':"keep-alive",
            'cache-control':"no-cache",
        }
        get_proxyurl = "http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1000&fa=0&fetch_key=MTg2OTE0OTk3NjN8MTA%253D&qty=1&time=1&pro=&city=&port=1&format=json&ss=5&css=&ipport=1&et=1&pi=1&co=1&dt=1&specialTxt=3&specialJson="
        response = requests.get(get_proxyurl)
        self.proxy = {}
        ip_port = ''
        ip_proxy_lst = json.loads(response.text)
        if ip_proxy_lst['success'] == 'true':
            ip_port = ip_proxy_lst['data'][0]['IP']
            self.proxy = {
                "http": "http://" + ip_port
                #   "https":"https://"+ip_port
            }
        self.req = requests.Session()
        res= self.req.get("https://s.sfddj.com/Shop/WebApp/app_share_down.html?sell_member_id="+ self.invite_code,headers=self.headers,proxies=self.proxy) 
        # requests.utils.add_dict_to_cookiejar(self.req.cookies, res.cookies.get_dict())  
        print(self.proxy)

    # ��ȡ������֤��
    def getSF_SMS(self):
        url = "http://api.fxhyd.cn/UserInterface.aspx"
        querystring = {
            "action": "getsms",
            "token": self.jiema_token,
            "itemid": "1333",
            "mobile": self.phone_num,
            "release": "1"
        }

        for counter in range(1, 10):
            response = requests.request(
                "POST", url, headers=self.sms_headers, params=querystring)
            sms_txt = response.text
            varified_code = ''
            if 'success' in sms_txt:
                varified_code = re.sub("\D", "", sms_txt)
                print(self.phone_num + "�Ķ�����֤����" + varified_code)
                break
            print("�ȴ����Ž��յ�" + str(counter) + "�Σ�" + self.jiema_code[sms_txt])
            time.sleep(5)
            continue
        return varified_code

    #��ȡ����
    def SF_Send_code(self, sms_code):
        if len(self.phone_num) == 0:
            print("δ��ȡ���ֻ�����")
            return ''
        if len(sms_code) == 0:
            print("δ��ȡ��������֤��")
            return ''
        url = "https://s.sfddj.com/fxfront/loginapp/appInviteRegister?appid=APPID"
        reqbody = 'cellphone=' + self.phone_num + '&code=' + sms_code + '&temp_id=' + self.invite_code
        response = self.req.request(
            "POST",
            url,
            data=reqbody,
            headers=self.headers,
            proxies=self.proxy)
        print(response.text)
        # with open(self.jiema_account + ".txt", 'w+') as phone_txt:
        #     phone_txt.write(response.text)

    # ///��ȡ˳�������֤��
    def getPhoneCode(self):
        if len(self.phone_num) == 0:
            print("�ֻ�����Ϊ��")
            return ''
        url = "https://s.sfddj.com/fxfront/loginapp/sendAppLoginCode"
        querystring = {"appid": "APPID"}
        payload = "cellphone=" + self.phone_num 
        response = self.req.request(
            "POST",
            url,
            data=payload,
            headers=self.headers,
            params=querystring,
            proxies=self.proxy)
        print(response.text + self.phone_num)


if __name__ == '__main__':
    sp = SFReg()
    #��һ�������˺� �����룬������
    sp.login_jiema("account", "password", "invitecode")
    # sp.get_proxy()
    for tick in range(1, 1000):
        print("��" + str(tick) + "��ע��")
        phone_num = sp.get_phone_number()
        if len(phone_num) == 0:
            continue
        sp.get_proxy()
        sp.getPhoneCode()
        varified_code = sp.getSF_SMS()
        if len(varified_code) == 6:
            sp.SF_Send_code(varified_code)
