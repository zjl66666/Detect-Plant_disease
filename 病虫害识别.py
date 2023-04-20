import requests as rq
from apig_sdk import signer
import streamlit as st


def get_prediction(img_data):
    url = "https://7cdcf16693a1461a8d20e3f339732871.apig.cn-north-4.huaweicloudapis.com/v1/infers/5ebf7d61-188a-4a49" \
          "-8031-c0bee020b469"
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
uploaded_file = st.file_uploader('选择一张植物病虫害叶子照片🐛')
if uploaded_file:
    st.image(uploaded_file, caption='上传的文件')
    img_data = uploaded_file.read()
    try:
        pred = get_prediction(img_data)
        pred_label = pred['predicted_label']
        st.subheader(f'该病害最有可能为{pred_label}')
        with st.expander('查看更多信息'):
            st.write('预测结果及其可能的概率')
            for data in pred['scores']:
                st.write('可能的病害:', data[0], '概率:', data[1])
        import openai
        messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        st.write('下面是针对这种病害的简单介绍及防治方法')
        openai.api_key = "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"
        user_msg = '简单介绍一下' + pred_label + '及其防治方法'
        messages.append({'role': 'user', 'content': user_msg})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.9,  # 对于温度，较高的值（如 0.8）将使输出更加随机，而较低的值（如 0.2）将使其更加集中和确定
            max_tokens=500)
        assistant_msg = response.choices[0]['message']['content']
        messages.append({'role': 'assistant', 'content': assistant_msg})
        st.write(assistant_msg)
    except:
        st.error('识别失败,请重新上传图片,下面是识别成功的示例')
        pred_label = '苹果黑星病'
        st.subheader(f'该病害最有可能为{pred_label}')
        st.write("""下面是针对这种病害的简单介绍及防治方法苹果黑星病是一种由真菌引起的病害，其症状包括果实表面出现黑褐色斑点或斑块，严重的情况下会使整个果实腐烂。以下是预防和控制苹果黑星病的方法：清理果园：将树枝、落叶等有病害的植物部分及时清理掉，减少病菌生存环境。喷洒农药：在果树芽展期至花后初期，每7-10天喷洒一次杀菌剂，可有效控制黑星病。喷洒草酸铜：在果实成形前期进行喷洒，可以预防苹果黑星病的发生。换栽抗病品种：选择抗黑星病的苹果品种进行种植，可有效减少病害的发生。加强管理：对果园中的营养、灌溉等要进行科学的管理，增强苹果树的抗病性。""")


#######################################################################################
#
# import requests as rq
# import streamlit as st
#
#
# def get_translate(text):
#     # 先处理text
#     st.write(text)
#     text = text.split('___')[1]
#     name = text.split('_')[0]
#     disease = text.split('_')[1]
#     post_text = name.lower() + ' ' + disease
#     st.write(post_text)
#     url = "https://fanyi.baidu.com/sug"
#     data = {"kw": f"{post_text}"}
#     response = rq.post(url, data=data)
#     TranslateResult = response.json()['data']
#     st.write(f"该词语的意思是:{TranslateResult[0]['v']}")
#
#
# st.set_page_config(page_title='植物病虫害识别', page_icon='🌼', layout='centered', initial_sidebar_state='auto')
# st.balloons()
# st.title("植物病虫害识别🌼 ")
# uploaded_file = st.file_uploader('选择一张植物病虫害叶子照片📷 ')
# if uploaded_file:
#     st.image(uploaded_file, caption='上传的文件')
#     img_data = uploaded_file.read()
#     pred_label = '苹果黑心病'
#     st.subheader(f'该病害最有可能为{pred_label}🐛')
#     st.write('下面是针对这种病害的简单介绍及防治方法')






