import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import requests
import os
apiurl = os.environ['API_URL']
apikey = os.environ['API_KEY']

st.set_page_config(
        page_title="Munich Self-Checkout Finder",
        page_icon="shopping_trolley"
    )
st.title('Munich Self-Checkout Finder: Shop Smarter, Not Harder!')
intro_md = '''
Welcome to the **Munich Self-Checkout Finder**, your go-to web app for discovering shops with self-checkout options across the city!

We know how tricky it can be to find a complete and up-to-date list of shops offering self-checkout, especially since most lists out there rely on outdated community inputs. That’s where we come in! Our app provides a comprehensive overview, making it easier for you to shop faster and smarter.

### How the data is collected:
We’ve scraped reviews from Google Maps to find stores with mentions of self-checkout experiences. To ensure accuracy, we run both automatic text detection and a manual context check to minimize any false alarms.

### How the web app works:
1. Select a list of shops from the sidebar.
2. Draw an area on the map.
3. Click 'Show on Map'—and voilà! Markers for shops with self-checkout will appear on the map.

The data was last updated on **December 25, 2024**. While we’re committed to keeping it current, there may still be a few shops missing or occasional mismatches—please bear with us!

We hope this tool makes your shopping experience smoother. Happy shopping! 🌟
'''
@st.dialog("Welcome to the Munich Self-Checkout Finder")
def info():
    st.write(intro_md)

if st.button("How it works"):
    info()

sbf = st.sidebar.form(key="Parameters")
sbf.header("Choose Shops")


if "drawings" not in st.session_state:
    st.session_state.drawings = None

x = requests.get(f'{apiurl}/get_names', headers = {"API_KEY": apikey})
shops = x.json()

icon_fp = "./app/shop_logo/custom/{}".format
icon_f = {'REWE':'rewe.png',
           'PENNY':'penny.png',
           'ALDI SÜD':'aldi.png',
           'Lidl':'lidl.png',
           'Netto':'netto.png',
           'ROSSMANN':'rossmann.png',
           'dm':'dm.png',
           'EDEKA':'edeka.png'
           }
# Create an HTML string for the custom icon with resizing

if "shops" not in st.session_state:
    st.session_state.shops = []
st.session_state.shops = sbf.multiselect("Shops",
                         shops,
                         )
st.session_state.unify_marker = sbf.checkbox("Use Unify Markers")
popup_html = """
<h1>{}</h1><br>
<p>
Address: {}<br></p>
<p><b>{} review{}</b> mentioned experiences related to self-checkout.<br> 
The latest review is <b>{}</b>.<br></p>
<p><a href="{}" target="_blank">Go to Google Map</a>
</p>""".format

# Init Markers
if "fg" not in st.session_state:
    st.session_state.fg = None

# Init Warning Message
if "warning" not in st.session_state:
    st.session_state.warning = None

def load_markers(shops, drawing):
    if len(shops) == 0:
        st.session_state.warning = 'Please select at least one shop.'
        return None
    if drawing is None or len(drawing) == 0:
        st.session_state.warning = 'Please draw 1 searching area.'
        return None
    if len(drawing) > 1:
        st.session_state.warning = 'Please only draw 1 area.'
        return None

    cnt = 0
    
    sb_shop_req = requests.post(f'{apiurl}/shops', 
                                headers = {"API_KEY": apikey},
                                json= {'shop_types':shops,
                                       'area':drawing[0],
                                       'with_sb_kassen': True
                                       }
                                )
    sb_shop = sb_shop_req.json()
    if sb_shop_req.status_code == 400:
        st.session_state.warning = sb_shop['detail']
        return None
    if sb_shop_req.status_code == 500:
        st.session_state.warning = sb_shop['detail']
        return None
    if sb_shop_req.status_code != 200:
        st.session_state.warning = 'Something went wrong when querying.'
        return None
    if sb_shop is None or len(sb_shop) == 0:
        st.session_state.warning = 'No shop found.'
        return None
    
    # Summary of the reviews
    place_ids = [r['place_id'] for r in sb_shop]
    review_req = requests.post(f'{apiurl}/reviews', 
                            headers = {"API_KEY": apikey},
                            json= {'place_ids':place_ids})
    review_stat = review_req.json()
    
    fg = folium.FeatureGroup(name="Markers",overlay=True,control=True,show=True)
    for r in sb_shop:
        if cnt > 100:
            break
        if st.session_state.unify_marker:
            icon = folium.Icon(icon='cart-shopping', prefix='fa', color="red")
        else:
            icon = folium.features.CustomIcon(
                icon_fp(icon_f[r['shop']]),
                icon_size=(30, ),
                icon_anchor = (15,30)
                )
        mark = folium.Marker(
            location=[r['lat'], r['lon']],
            tooltip=r['name'],
            popup=folium.Popup(
                popup_html(
                    r['name'],
                    f'{r['complete_address']['street']}, {r['complete_address']['postal_code']} {r['complete_address']['city']}',
                    review_stat[r['place_id']]['num_review'],
                    's' if review_stat[r['place_id']]['num_review'] != 1 else '',
                    review_stat[r['place_id']]['latest_review_relative_date'],
                    r['link']), 
                max_width=300),
            icon = icon,
        )
        fg.add_child(mark)

    # Reset Warning Message
    st.session_state.warning = None
    return fg



def refresh_map():
    m = folium.Map(location=[48.1351, 11.5820], zoom_start=10)
    Draw(export=False,
         draw_options={"polyline": False,
                       "marker": False,
                       "circlemarker":False,
                       "circle":False,
                       "polygon": True,
                       "rectangle": True
                       }
         ).add_to(m)

    output = st_folium(m, width=725,key='map',feature_group_to_add=st.session_state.fg)
    
    return output

# create a function that reset the value in state back to its init state
def reset_markers():
    st.session_state.fg = None
    return

if sbf.form_submit_button("Show on Map"):
    #Update Markers
    st.session_state.fg = load_markers(st.session_state.shops, st.session_state.drawings)
    # Actually one need not to do anything in if-statement, because this already automatically trigger a rerun of the app lol

if st.session_state.warning is not None:
    st.write(f'⚠️{st.session_state.warning}')
output = refresh_map()
#create your button to clear the state of the multiselect
st.button("Clear Markers", on_click=reset_markers)
st.session_state.drawings = output['all_drawings']
