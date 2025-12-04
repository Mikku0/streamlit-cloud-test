import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIG ---
st.set_page_config(
    page_title="California Housing Explorer",
    page_icon="🏠",
    layout="wide"
)

# --- CACHE DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("housing.csv")
        return df
    except:
        return None

@st.cache_data
def calculate_stats(df):
    """Obliczenia statystyk na całym datasecie"""
    return {
        'total_records': len(df),
        'avg_price': df['median_house_value'].mean(),
        'median_price': df['median_house_value'].median(),
        'avg_rooms': df['total_rooms'].mean(),
        'avg_income': df['median_income'].mean()
    }

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🏠 Strona Główna", "🗺️ Mapa Wizualizacji", "📊 Statystyki i Analiza"])

# ============================================================================
# TAB 1: STRONA GŁÓWNA (main.py)
# ============================================================================
with tab1:
    st.title("🏠 California Housing Price Prediction Project")
    st.markdown("""
    Witamy w aplikacji do eksploracji i analizy **cen nieruchomości w Kalifornii**.

    Ta aplikacja pozwala na:
    - 🔎 interaktywną **wizualizację danych na mapie**,  
    - 📊 szczegółową **analizę statystyczną**,  
    - 🤖 trenowanie i testowanie **modelu predykcyjnego cen nieruchomości**,  
    - 📁 wgrywanie własnych zbiorów danych do analizy.

    Przejdź do wybranej sekcji używając zakładek powyżej.
    """)

    st.divider()

    # --- SEKCJA 1: Szybki opis datasetu z Kaggle ---
    st.header("📁 O projekcie i danych")
    st.write("""
    Projekt wykorzystuje popularny zbiór danych 
    **California Housing Prices** pochodzący z serwisu Kaggle.

    Zawiera on informacje o:
    - 🌆 lokalizacji (geograficznej)  
    - 👨‍👩‍👧‍👦 populacji  
    - 🏡 liczbie pokoi i gospodarstw  
    - 💰 medianowych dochodach  
    - 🏠 medianowych cenach nieruchomości  

    Celem projektu jest **eksploracja danych** oraz **budowa modelu predykcji cen domów**.
    """)

    st.divider()

    # --- SEKCJA 2: Trzy duże boxy z opisami ---
    st.subheader("🔍 Główne sekcje aplikacji")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("### 🗺️ Mapa wizualizacji\nInteraktywna mapa z filtrami, wyborem kolumn i wykresami.")

    with col2:
        st.info("### 📊 Statystyki i Analiza\nHistogramy, korelacje, wykresy zależności i kluczowe metryki.")

    with col3:
        st.info("### 🤖 Predykcja (w przyszłości)\nStrona na model ML do przewidywania cen mieszkań.")

    st.divider()

    # --- SEKCJA 3: Szybki preview datasetu (opcjonalny) ---
    st.header("📌 Podgląd wbudowanego datasetu")

    df = load_data()
    if df is not None:
        st.write(f"Wczytano dane: **{df.shape[0]} rekordów, {df.shape[1]} kolumn**")
        st.dataframe(df.head(), use_container_width=True)
    else:
        st.warning("Nie znaleziono pliku *housing.csv*. Upewnij się, że znajduje się w folderze projektu lub wgraj własny plik w zakładce 'Mapa Wizualizacji'.")

    st.divider()

    # --- FOOTER ---
    st.markdown("""
    ### 🧑‍💻 Autorzy projektu  
    Anna Woźniak, Mikołaj Wróblewski, Daniil Ihnatiuhin
    """)

# ============================================================================
# TAB 2: MAPA WIZUALIZACJI (map.py)
# ============================================================================
with tab2:
    st.title("🗺️ Mapa Wizualizacji")
    st.markdown("""
    Upload your housing dataset (CSV format) and explore housing prices on an interactive map.
    Select columns for location and price, enable filters, and customize what's shown on the map.
    """)

    # Sidebar for controls
    st.sidebar.header("Controls")
    
    # File uploader
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV file",
        type=["csv"],
        help="Upload a CSV file containing housing data"
    )

    # Opcja użycia wbudowanego datasetu
    use_builtin = st.sidebar.checkbox("Użyj wbudowanego datasetu (housing.csv)", value=True)
    manual_input = st.sidebar.checkbox("Wprowadź własne dane ręcznie")

    df_map = None
    
    if use_builtin:
        df_map = load_data()
        if df_map is None:
            st.error("Nie można wczytać pliku housing.csv")
    elif uploaded_file is not None:
        try:
            df_map = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    elif manual_input:
        st.subheader("Manual Data Entry")
        num_points = st.number_input("Ile punktów chcesz dodać?", min_value=1, max_value=20, value=1)

        manual_data = []
        for i in range(num_points):
            st.markdown(f"**Punkt {i+1}**")
            lon = st.number_input(f"Longitude {i+1}", value=-120.0, key=f"lon_{i}")
            lat = st.number_input(f"Latitude {i+1}", value=35.0, key=f"lat_{i}")
            housing_median_age = st.number_input(f"Housing Median Age {i+1}", value=20.0, key=f"age_{i}")
            total_rooms = st.number_input(f"Total Rooms {i+1}", value=1000.0, key=f"rooms_{i}")
            total_bedrooms = st.number_input(f"Total Bedrooms {i+1}", value=200.0, key=f"bedrooms_{i}")
            population = st.number_input(f"Population {i+1}", value=500.0, key=f"pop_{i}")
            households = st.number_input(f"Households {i+1}", value=150.0, key=f"households_{i}")
            median_income = st.number_input(f"Median Income {i+1}", value=3.0, key=f"income_{i}")
            
            # Placeholder predykcji – średnia cena z datasetu lub stała wartość
            placeholder_price = 200000.0
            manual_data.append({
                "longitude": lon,
                "latitude": lat,
                "housing_median_age": housing_median_age,
                "total_rooms": total_rooms,
                "total_bedrooms": total_bedrooms,
                "population": population,
                "households": households,
                "median_income": median_income,
                "predicted_price": placeholder_price
            })

        df_map = pd.DataFrame(manual_data)

        # Pokazanie przewidywanej ceny (placeholder)
        st.success(f"Przewidywana cena domu (placeholder): **${placeholder_price:,.0f}**")

        # Wizualizacja punktu na mapie
        fig_pred = px.scatter_mapbox(
            df_map,
            lat="latitude",
            lon="longitude",
            color="predicted_price",
            size_max=15,
            zoom=6,
            mapbox_style="open-street-map",
            title="Predykcja ceny domu (placeholder)",
            hover_data=df_map.columns
        )
        st.plotly_chart(fig_pred, use_container_width=True)

    # --- Jeśli dane pochodzą z pliku lub wbudowanego datasetu ---
    if df_map is not None and not manual_input:
        try:
            st.success(f"Successfully loaded dataset with {df_map.shape[0]} rows and {df_map.shape[1]} columns.")
            
            # Display basic info about the dataset
            st.subheader("Dataset Overview")
            st.write(f"**Shape:** {df_map.shape}")
            st.write("**First few rows:**")
            st.dataframe(df_map.head())
            
            # Column selection
            numeric_columns = df_map.select_dtypes(include=['number']).columns.tolist()
            all_columns = df_map.columns.tolist()
            
            if not numeric_columns:
                st.error("No numeric columns found in the dataset.")
            else:
                st.subheader("Column Selection")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    longitude_col = st.selectbox(
                        "Select Longitude Column",
                        options=numeric_columns,
                        index=min(0, len(numeric_columns)-1),
                        help="Column containing longitude values"
                    )
                    
                with col2:
                    latitude_col = st.selectbox(
                        "Select Latitude Column",
                        options=numeric_columns,
                        index=min(1, len(numeric_columns)-1) if len(numeric_columns) > 1 else min(0, len(numeric_columns)-1),
                        help="Column containing latitude values"
                    )
                    
                with col3:
                    price_col = st.selectbox(
                        "Select Price Column",
                        options=numeric_columns,
                        index=min(2, len(numeric_columns)-1) if len(numeric_columns) > 2 else -1,
                        help="Column containing housing price values"
                    )
                
                # Filter controls
                st.subheader("Filters")
                available_filters = [col for col in df_map.columns if col not in [longitude_col, latitude_col, price_col]]
                
                selected_filters = st.multiselect(
                    "Select columns to use for filtering:",
                    options=available_filters,
                    default=None
                )
                
                active_filters = {}
                for col in selected_filters:
                    col_type = df_map[col].dtype
                    if pd.api.types.is_numeric_dtype(col_type):
                        min_val = float(df_map[col].min())
                        max_val = float(df_map[col].max())
                        default_range = (min_val, max_val)
                        filter_range = st.slider(
                            f"Filter by {col}",
                            min_value=min_val,
                            max_value=max_val,
                            value=default_range,
                            key=f"filter_{col}"
                        )
                        if filter_range != (min_val, max_val):
                            active_filters[col] = filter_range
                    else:
                        unique_vals = df_map[col].dropna().unique()
                        selected_vals = st.multiselect(
                            f"Filter by {col}",
                            options=unique_vals,
                            default=unique_vals,
                            key=f"filter_{col}_multi"
                        )
                        if len(selected_vals) != len(unique_vals):
                            active_filters[col] = selected_vals
                            
                filtered_df = df_map.copy()    
                for col, filter_val in active_filters.items():
                    if isinstance(filter_val, tuple):  # Numeric range
                        filtered_df = filtered_df[
                            (filtered_df[col] >= filter_val[0]) & 
                            (filtered_df[col] <= filter_val[1])
                        ]
                    else:  # Categorical values
                        filtered_df = filtered_df[filtered_df[col].isin(filter_val)]
                
                st.write(f"Filtered dataset: {filtered_df.shape[0]} rows (out of {df_map.shape[0]} total)")
                
                # Map visualization
                if longitude_col in filtered_df.columns and latitude_col in filtered_df.columns:
                    st.subheader("Map Visualization")
                    
                    # Allow user to select which columns to show on the map
                    map_columns = st.multiselect(
                        "Select columns to display on map hover:",
                        options=all_columns,
                        default=[longitude_col, latitude_col, price_col] if price_col else [longitude_col, latitude_col]
                    )
                    
                    # Create a dataframe with only the selected columns for the map
                    map_df = filtered_df[map_columns].copy()
                    # Add the lat/lon columns to the map dataframe if not already included
                    if longitude_col not in map_df.columns:
                        map_df[longitude_col] = filtered_df[longitude_col]
                    if latitude_col not in map_df.columns:
                        map_df[latitude_col] = filtered_df[latitude_col]
                    
                    # Check if required columns exist
                    if price_col in filtered_df.columns:
                        # Create map with price as color
                        fig = px.scatter_mapbox(
                            map_df,
                            lat=latitude_col,
                            lon=longitude_col,
                            color=price_col,
                            color_continuous_scale=px.colors.sequential.Viridis,
                            size_max=15,
                            zoom=10,
                            mapbox_style="open-street-map",
                            title="Housing Prices Map",
                            hover_data=[c for c in map_columns if c not in [longitude_col, latitude_col, price_col]]
                        )
                        
                        fig.update_layout(
                            margin={"r":0,"t":30,"l":0,"b":0},
                            height=600
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        # Create map without price color if price column not selected
                        fig = px.scatter_mapbox(
                            map_df,
                            lat=latitude_col,
                            lon=longitude_col,
                            size_max=15,
                            zoom=10,
                            mapbox_style="open-street-map",
                            title="Housing Locations Map",
                            hover_data=[c for c in map_columns if c not in [longitude_col, latitude_col]]
                        )
                        
                        fig.update_layout(
                            margin={"r":0,"t":30,"l":0,"b":0},
                            height=600
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error processing the data: {str(e)}")
            st.info("Please ensure the uploaded file is a valid CSV with numeric columns for longitude, latitude, and price.")
    else:
        st.info("Please upload a CSV file or check 'Użyj wbudowanego datasetu' to begin exploring housing data.")

# ============================================================================
# TAB 3: STATYSTYKI (statistics.py)
# ============================================================================
with tab3:
    st.header("📊 Dane i Statystyki")

    df_stats = load_data()
    
    if df_stats is None:
        st.error("Nie można wczytać pliku housing.csv. Upewnij się, że plik znajduje się w folderze projektu.")
    else:
        stats = calculate_stats(df_stats)

        # KLUCZOWE METRYKI
        st.subheader("Kluczowe Metryki")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Liczba nieruchomości", len(df_stats))

        with col2:
            avg_price = df_stats['median_house_value'].mean()
            st.metric("Średnia cena domu", f"${avg_price:,.0f}")

        with col3:
            median_price = df_stats['median_house_value'].median()
            st.metric("Mediana ceny", f"${median_price:,.0f}")

        with col4:
            avg_rooms_per_house = (df_stats['total_rooms'] / df_stats['households']).mean()
            st.metric("Średnia liczba pokoi na dom", f"{avg_rooms_per_house:.2f}")

        st.divider()

        # WIZUALIZACJE
        st.subheader("Wizualizacje")

        col1, col2 = st.columns(2)

        with col1:
            # Rozkład cen
            fig_price = px.histogram(
                df_stats,
                x='median_house_value',
                nbins=30,
                title="Rozkład cen domów",
                labels={'median_house_value': 'Cena domu ($)', 'count': 'Liczba nieruchomości'}
            )
            st.plotly_chart(fig_price, use_container_width=True)

        with col2:
            # Zależność: dochód vs cena
            fig_scatter = px.scatter(
                df_stats,
                x='median_income',
                y='median_house_value',
                color='housing_median_age',
                title="Dochód vs Cena Domu",
                labels={
                    'median_income': 'Dochód medianowy',
                    'median_house_value': 'Cena domu ($)',
                    'housing_median_age': 'Wiek domu (lata)'
                }
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            # Cena vs liczba pokoi
            fig_rooms = px.scatter(
                df_stats,
                x='total_rooms',
                y='median_house_value',
                title="Cena vs Liczba Pokoi",
                labels={
                    'total_rooms': 'Całkowita liczba pokoi',
                    'median_house_value': 'Cena domu ($)'
                }
            )
            st.plotly_chart(fig_rooms, use_container_width=True)

        with col4:
            # Wiek domu vs cena
            df_age = df_stats.copy()
            df_age['age_group'] = pd.cut(df_stats['housing_median_age'], bins=5).astype(str)
            fig_age = px.box(
                df_age,
                x='age_group',
                y='median_house_value',
                title="Cena w Zależności od Wieku",
                labels={
                    'age_group': 'Wiek domu',
                    'median_house_value': 'Cena domu ($)'
                }
            )
            st.plotly_chart(fig_age, use_container_width=True)

        col5, col6 = st.columns(2)

        with col5:
            # Populacja vs cena
            fig_pop = px.scatter(
                df_stats,
                x='population',
                y='median_house_value',
                title="Populacja vs Cena Domu",
                labels={
                    'population': 'Populacja',
                    'median_house_value': 'Cena domu ($)'
                }
            )
            st.plotly_chart(fig_pop, use_container_width=True)

        with col6:
            # Liczba gospodarstw vs cena
            fig_households = px.scatter(
                df_stats,
                x='households',
                y='median_house_value',
                title="Liczba Gospodarstw vs Cena",
                labels={
                    'households': 'Liczba gospodarstw',
                    'median_house_value': 'Cena domu ($)'
                }
            )
            st.plotly_chart(fig_households, use_container_width=True)

        st.divider()

        # STATYSTYKI OPISOWE
        st.subheader("Statystyki Opisowe")
        stats_table = df_stats.describe().round(2)
        st.dataframe(stats_table, use_container_width=True)

        st.divider()

        # MACIERZ KORELACJI I TOP KORELACJE
        st.subheader("Analiza Korelacji")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Macierz Korelacji**")
            num_df = df_stats.select_dtypes(include=['int64', 'float64'])
            corr_table = num_df.corr().round(3)

            fig_corr = px.imshow(corr_table,
                                title="Macierz Korelacji",
                                labels=dict(color="Korelacja"),
                                color_continuous_scale='RdBu',
                                zmin=-1, zmax=1)
            st.plotly_chart(fig_corr, use_container_width=True)

        with col2:
            st.write("**Top 10 Korelacji z Ceną Domu**")
            price_corr = corr_table['median_house_value'].sort_values(ascending=False)[1:11]
            fig_top = px.bar(price_corr, title="Top 10 Cech Skorelowanych z Ceną",
                            labels={'value': 'Korelacja', 'index': 'Cecha'})
            st.plotly_chart(fig_top, use_container_width=True)

        st.divider()

        # SUROWE DANE
        st.subheader("Surowe Dane")
        st.dataframe(df_stats, use_container_width=True)
