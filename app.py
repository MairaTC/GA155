import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

PAGE_CONFIG = {"page_title":"Violência contra a Mulher","page_icon":":womens:","layout":"centered"}
st.set_page_config(**PAGE_CONFIG)

def load_data():
    df = pd.read_excel("data/homicidios_mulheres.xlsx")
    return df

def main():
    st.title("Violência contra a Mulher — Homicídios 2021")
    
    # Carrega os dados
    df = load_data()
    
    #sidebar
    menu = ["Home", "Dashboard", "Mapa"]
    choice = st.sidebar.selectbox('Menu', menu)
    
    st.sidebar.divider()
    st.sidebar.subheader("Filtros")
    
    estados = sorted(df["Estado/Região"].unique())
    sel = st.sidebar.multiselect("Selecione os Estados", estados, default=estados)
    df_filtrado = df[df["Estado/Região"].isin(sel)]
    
    if choice == 'Home':
        st.subheader("Homicídios de mulheres no Brasil em 2021")
        st.write("""
        Dados do IBGE - Estatísticas de Gênero (Tabela 5.a)
        Ano: 2021
        """)
  
    elif choice == 'Dashboard':
        st.subheader("Dashboard de Indicadores")
        
        #indicadores
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de homicídios", f"{df_filtrado['Total de Homicídios'].sum():,}".replace(",", "."))
        col2.metric("Vítimas mulheres", f"{df_filtrado['Mulheres — Total'].sum():,}".replace(",", "."))
        col3.metric("Taxa média (por 100 mil hab.)", f"{df_filtrado['Mulheres — Taxa'].mean():.1f}")
        
        st.divider()
        
        #por estado
        st.subheader("Homicídios de mulheres por estado")
        df_graf1 = df_filtrado.set_index("Estado/Região")[["Mulheres — Total"]].sort_values("Mulheres — Total", ascending=False)
        st.bar_chart(df_graf1)
        
        st.divider()
        
        #por raça
        st.subheader("Vítimas por raça e local")
        df_graf2 = pd.DataFrame({
            "Vítimas": {
                "Branca – domicílio": df_filtrado["Mulheres Brancas — No domicílio"].sum(),
                "Preta/Parda – domicílio": df_filtrado["Mulheres Pretas/Pardas — No domicílio"].sum(),
                "Branca – fora": df_filtrado["Mulheres Brancas — Fora do domicílio"].sum(),
                "Preta/Parda – fora": df_filtrado["Mulheres Pretas/Pardas — Fora do domicílio"].sum(),
            }
        })
        st.bar_chart(df_graf2)
        
        #tabela
        st.divider()
        st.subheader("Dados detalhados")
        st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
    
    elif choice == 'Mapa':
        st.subheader("Mapa de Taxa de Homicídios de Mulheres por Estado")
        
        #mapa
        m = folium.Map(location=[-14.2, -51.9], zoom_start=4)
        
        folium.Choropleth(
            geo_data="data/brasil.geojson",
            data=df_filtrado,
            columns=["Estado/Região", "Mulheres — Taxa"],
            key_on="feature.properties.NM_UF",
            fill_color="Reds",
            fill_opacity=0.7,
            line_opacity=0.5,
            legend_name="Taxa de homicídios de mulheres (por 100 mil hab.)",
            nan_fill_color="white",
        ).add_to(m)
        
        folium_static(m)

if __name__ == '__main__':
    main()