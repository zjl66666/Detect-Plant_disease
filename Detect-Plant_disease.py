import requests as rq
from apig_sdk import signer
import streamlit as st
import json

identification_scope = """
南瓜白粉病
柑橘黄龙病（柑橘绿化）
桃树叶斑病
樱桃白粉病
没有叶子
玉米北方叶枯病
玉米尾孢叶斑病 灰斑病
玉米锈病
甜椒菌斑病
番茄叶斑病
番茄叶螨、二斑叶螨病
番茄叶霉菌
番茄斑点疫霉病
番茄早疫病
番茄晚疫病
番茄细菌斑
番茄花叶病毒病
番茄黄化曲叶病毒病
苹果雪松苹果锈病
苹果黑星病
苹果黑腐病
草莓叶枯病
葡萄叶枯病（叶斑病）
葡萄埃斯卡（黑麻疹）
葡萄黑腐病
马铃薯早疫病
马铃薯晚疫病
"""

@st.cache_data(ttl=600)
def get_prediction(img_data):
    url = 'https://7cdcf16693a1461a8d20e3f339732871.apig.cn-north-4.huaweicloudapis.com/v1/infers/00f75539-a8b9-4af6-95e0-be2f9182e9e5'
    app_key = "db941e4460c0448e805a1d46471bad30"
    app_secret = "d50b85c6d8e54708a1f880fac30e1399"

    method = 'POST'
    headers = {"x-sdk-content-sha256": "UNSIGNED-PAYLOAD"}
    request = signer.HttpRequest(method, url, headers)

    sig = signer.Signer()
    sig.Key = app_key
    sig.Secret = app_secret
    sig.Sign(request)
    # files读取的
    files = {'images': img_data}
    res = rq.request(request.method, request.scheme + "://" + request.host + request.uri, headers=request.headers,
                     files=files)
    return res.json()


st.set_page_config(page_title='植物病虫害识别', page_icon='🌼', layout='centered', initial_sidebar_state='auto')
st.balloons()
st.title("植物病虫害识别🌼 ")
st.sidebar.subheader('识别范围🔍')
st.sidebar.text(identification_scope)
uploaded_file = st.file_uploader('选择一张植物病虫害叶子照片🐛')
if uploaded_file:
    st.image(uploaded_file, caption='上传的文件')
    img_data = uploaded_file.read()
    with st.spinner('识别中...'):
        pred = get_prediction(img_data)
    pred_label = pred['predicted_label']
    st.success('✅识别成功')
    st.subheader(f'识别结果为{pred_label}')
    with st.expander('查看更多信息'):
        st.write('预测结果及其可能的概率')
        for data in pred['scores']:
            st.write('可能的病害:', data[0], '概率:', data[1])
    # 读取json文件并展示info
    if '健康' in pred_label:
        st.subheader('该叶子健康😃')
    else:
        with open(f'./json数据/{pred_label}.json', 'r') as f:
            data = json.load(f)
            st.text(data['info'])
            # if sound:
            #     info = f'该病害最有可能为{pred_label}'+data['info']
            #     import pyttsx3
            #     engine = pyttsx3.init()
            #     rate = engine.getProperty('rate')
            #     engine.setProperty('rate', rate - 50)
            #     engine.say(info)
            #     # 设置使其停止的功能
            #
            #     engine.runAndWait()
            #     engine.stop()
