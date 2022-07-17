import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(
     page_title="Opensea Collection Stats",
     page_icon="🌊",
     layout="wide",
     initial_sidebar_state="expanded",
    #  menu_items={
    #      'Get help': 'https://www.google.com/help',
    #      'Report a bug': "https://www.google.com/bug",
    #      'About': "# Opensea Collection Stats - by Metonymy Machine GmbH"
    #  }
 )

# Opensea API requests
headers = {
    "Accept": "application/json",
    "X-API-KEY": st.secrets["opensea_api"]
}

contract_address = st.text_input('Contract Address', '0x2acAb3DEa77832C09420663b0E1cB386031bA17B')
# opensea_link = st.text_input('Opensea-Link', '')
# opensea_slug = opensea_link.split('/')[-1]
# st.write(opensea_slug)


with st.spinner('Fetching Contract Info'):
    contract_request = "https://api.opensea.io/api/v1/asset_contract/" + contract_address
# st.write(contract_request)
    response_contract = requests.get(contract_request, headers=headers)
    contract_json = json.loads(response_contract.text) #convert to dict
col1, col2, col3 = st.columns(3)
col1.title(contract_json["collection"]["name"])
col2.image(contract_json["collection"]["image_url"], width=120)
col3.write(contract_json["collection"]["description"])

with st.spinner('Getting Collection Stats'):
    slug = (contract_json["collection"]["slug"])
    url_stats = "https://api.opensea.io/api/v1/collection/" + slug + "/stats"
    response_stats = requests.get(url_stats, headers=headers)
    stats_json = json.loads(response_stats.text) #convert to dict
    stats = stats_json["stats"]

rounding = 2

with st.spinner('Fetching Assets Info'):
    url_assets = "https://api.opensea.io/api/v1/assets?collection_slug=" + slug + "&order_direction=desc&limit=10&include_orders=false"
    response_assets = requests.get(url_assets, headers=headers)
    assets_json = json.loads(response_assets.text) #convert to dict
    assets = assets_json["assets"]

df = pd.DataFrame(
    assets
    # columns=['_id', 'Total chia']
    )
 # set index
df = df.set_index('token_id')
   # change order of columns
df = df.sort_index(ascending=True)
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
col1.image(assets[0]['image_thumbnail_url'])
col2.image(assets[1]['image_thumbnail_url'])
col3.image(assets[2]['image_thumbnail_url'])
col4.image(assets[3]['image_thumbnail_url'])
col5.image(assets[4]['image_thumbnail_url'])
col6.image(assets[5]['image_thumbnail_url'])
col7.image(assets[6]['image_thumbnail_url'])
col8.image(assets[7]['image_thumbnail_url'])
col9.image(assets[8]['image_thumbnail_url'])
col10.image(assets[9]['image_thumbnail_url'])

st.subheader('Collection Stats')

col1, col2, col3, col4 = st.columns(4)
col1.metric(value=str(stats["floor_price"])+ "Ξ", label='Floor Price')
col2.metric(value=str(round(stats["total_volume"]/stats_json["stats"]["total_sales"],rounding))+ "Ξ", label='All time average price')
col3.metric(value=str(round(stats["total_volume"],rounding)) + "Ξ", label='All time volume')
col4.metric(value=int(stats["total_sales"]), label='Total # Sales')


col1, col2, col3, col4 = st.columns(4)
col1.metric(value=int(stats["count"]), label='# Items')
col3.metric(value=round(int(stats["count"])/stats_json["stats"]["num_owners"],rounding), label='average items per owner')
col2.metric(value=stats["num_owners"], label='# of Owner')
col4.metric(value=stats["num_reports"], label='# of reports')

st.markdown("""---""") 
# st.subheader('1 day')
col1, col2, col3, col4 = st.columns(4)
col1.metric(value=str(round(stats["one_day_volume"],rounding))+ "Ξ", label='one_day_volume')
col2.metric(value=str(round(stats["one_day_change"],rounding))+ "Ξ", label='one_day_change')
col3.metric(value=int(stats["one_day_sales"]), label='one_day_sales')
col4.metric(value=str(round(stats["one_day_average_price"],rounding))+ "Ξ", label='one_day_average_price')

st.markdown("""---""") 
    # st.subheader('7 day')
col1, col2, col3, col4 = st.columns(4)
col1.metric(value=str(round(stats["seven_day_volume"],rounding))+ "Ξ", label='seven_day_volume')
col2.metric(value=str(round(stats["seven_day_change"],rounding))+ "Ξ", label='seven_day_change')
col3.metric(value=int(stats["seven_day_sales"]), label='seven_day_sales')
col4.metric(value=str(round(stats["seven_day_average_price"],rounding))+ "Ξ", label='seven_day_average_price')

st.markdown("""---""") 
# st.subheader('30 day')
col1, col2, col3, col4 = st.columns(4)
col1.metric(value=str(round(stats_json["stats"]["thirty_day_volume"],rounding))+ "Ξ", label='thirty_day_volume')
col2.metric(value=str(round(stats_json["stats"]["thirty_day_change"],rounding))+ "Ξ", label='thirty_day_change')
col3.metric(value=int(stats_json["stats"]["thirty_day_sales"]), label='thirty_day_sales')
col4.metric(value=str(round(stats_json["stats"]["thirty_day_average_price"],rounding))+ "Ξ", label='thirty_day_average_price')




if st.checkbox('Show Contract Info JSON'):
    st.write(contract_json)
if st.checkbox('Show Stats JSON'):
    st.write(stats)
if st.checkbox('Show Assets JSON'):
    st.write(assets)
if st.checkbox('Show Assets Dataframe'):
    st.dataframe(df)


st.stop()


# st.write(response_json["collection"]["description"])


# st.write(response_assets_json)








st.title(collection_title)
st.image(response_json["collection"]["featured_image_url"])
st.metric(value=floor_price, label="Floor Price")


# show json of the collection info
st.write(response_json["collection"])


# st.write(response_json_stats)
st.write("Floor Price:")
st.write(floor_price)

for key in assets:
    st.image(key["image_thumbnail_url"])
    st.write(key["permalink"])
    st.write("owned by "+key["owner"]["address"])


st.write(response_stats_json)