import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import requests
import os
from app_text import app_text

apiurl = os.environ["API_URL"]
apikey = os.environ["API_KEY"]

st.set_page_config(
    page_title="München SB-Kassen Finder | Munich Self-Checkout Finder",
    page_icon="shopping_trolley",
)

_, _, col = st.columns([3, 2, 1])
options = ["DE", "EN"]
lang = col.segmented_control(
    "Languages",
    options,
    selection_mode="single",
    default=options[0],
    label_visibility="collapsed",
).lower()
# col.button("DE")
st.title(app_text[lang]["title"])


@st.dialog(app_text[lang]["intro_title"])
def info():
    st.write(app_text[lang]["intro_md"])


if st.button(app_text[lang]["help"]):
    info()

sbf = st.sidebar.form(key="Parameters")
sbf.header(app_text[lang]["selector"])


if "drawings" not in st.session_state:
    st.session_state.drawings = None

x = requests.get(f"{apiurl}/get_names", headers={"API_KEY": apikey})
shops = x.json()

icon_fp = "./app/shop_logo/custom/{}".format
icon_f = {
    "REWE": "rewe.png",
    "PENNY": "penny.png",
    "ALDI SÜD": "aldi.png",
    "Lidl": "lidl.png",
    "Netto": "netto.png",
    "ROSSMANN": "rossmann.png",
    "dm": "dm.png",
    "EDEKA": "edeka.png",
}
# Create an HTML string for the custom icon with resizing

if "shops" not in st.session_state:
    st.session_state.shops = []
st.session_state.shops = sbf.multiselect(
    app_text[lang]["shops"],
    #  icon_f.keys(),
    shops,
)
st.session_state.unify_marker = sbf.checkbox(app_text[lang]["marker_choice"])
popup_html = app_text[lang]["popup_html"]

# Init Markers
if "fg" not in st.session_state:
    st.session_state.fg = None

# Init Warning Message
if "warning" not in st.session_state:
    st.session_state.warning = None


def load_markers(shops, drawing):
    if len(shops) == 0:
        st.session_state.warning = app_text[lang]["warning_no_shop"]
        return None
    if drawing is None or len(drawing) == 0:
        st.session_state.warning = app_text[lang]["warning_no_area"]
        return None
    if len(drawing) > 1:
        st.session_state.warning = app_text[lang]["warning_multiple_area"]
        return None

    cnt = 0

    sb_shop_req = requests.post(
        f"{apiurl}/shops",
        headers={"API_KEY": apikey},
        json={"shop_types": shops, "area": drawing[0], "with_sb_kassen": True},
    )
    sb_shop = sb_shop_req.json()
    if sb_shop_req.status_code == 400:
        st.session_state.warning = sb_shop["detail"]
        return None
    if sb_shop_req.status_code == 500:
        st.session_state.warning = sb_shop["detail"]
        return None
    if sb_shop_req.status_code != 200:
        st.session_state.warning = app_text[lang]["warning_not_200"]
        return None
    if sb_shop is None or len(sb_shop) == 0:
        st.session_state.warning = app_text[lang]["warning_no_shop_found"]
        return None

    # Summary of the reviews
    place_ids = [r["place_id"] for r in sb_shop]
    review_req = requests.post(
        f"{apiurl}/reviews", headers={"API_KEY": apikey}, json={"place_ids": place_ids}
    )
    review_stat = review_req.json()

    fg = folium.FeatureGroup(name="Markers", overlay=True, control=True, show=True)
    for r in sb_shop:
        if cnt > 100:
            break
        if st.session_state.unify_marker:
            icon = folium.Icon(icon="cart-shopping", prefix="fa", color="red")
        else:
            icon = folium.features.CustomIcon(
                icon_fp(icon_f[r["shop"]]), icon_size=(30,), icon_anchor=(15, 30)
            )
        mark = folium.Marker(
            location=[r["lat"], r["lon"]],
            tooltip=r["name"],
            popup=folium.Popup(
                popup_html(
                    r["name"],
                    f"{r['complete_address']['street']}, {r['complete_address']['postal_code']} {r['complete_address']['city']}",
                    review_stat[r["place_id"]]["num_review"],
                    (
                        app_text[lang]["popup_pl"]
                        if review_stat[r["place_id"]]["num_review"] != 1
                        else ""
                    ),
                    (
                        app_text[lang]["popup_verb_tense"]
                        if review_stat[r["place_id"]]["num_review"] != 1
                        else ""
                    ),
                    review_stat[r["place_id"]]["latest_review_relative_date"][lang],
                    r["link"],
                ),
                max_width=300,
            ),
            icon=icon,
        )  # .add_to(mc)
        fg.add_child(mark)
    # Reset Warning Message
    st.session_state.warning = None
    return fg


def refresh_map():
    m = folium.Map(location=[48.1351, 11.5820], zoom_start=10)
    Draw(
        export=False,
        draw_options={
            "polyline": False,
            "marker": False,
            "circlemarker": False,
            "circle": False,
            "polygon": True,
            "rectangle": True,
        },
    ).add_to(m)

    output = st_folium(
        m, width=725, key="map", feature_group_to_add=st.session_state.fg
    )

    return output


# create a function that reset the value in state back to its init state
def reset_markers():
    st.session_state.fg = None
    return


if sbf.form_submit_button(app_text[lang]["show"]):
    # st.write('Reloading map...')
    # Update Markers
    st.session_state.fg = load_markers(
        st.session_state.shops, st.session_state.drawings
    )
    # Actually one need not to do anything in if-statement, because this already automatically trigger a rerun of the app lol

if st.session_state.warning is not None:
    st.write(f"⚠️{st.session_state.warning}")
output = refresh_map()
# create your button to clear the state of the multiselect
st.button(app_text[lang]["clear"], on_click=reset_markers)
st.session_state.drawings = output["all_drawings"]
