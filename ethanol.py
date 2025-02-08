import streamlit as st
import pandas as pd
from forex_python.converter import CurrencyRates
import babel.numbers
from datetime import datetime

# Dictionary for translations
TRANSLATIONS = {
    'en': {
        'title': 'Ethanol Blend Calculator',
        'currency': 'Currency',
        'gas_price': 'Gas Price/L',
        'ethanol_price': 'Ethanol Price/L',
        'tank_capacity': 'Tank Capacity (L)',
        'fill_type': 'Fill Type',
        'full_fill': 'Full Fill',
        'partial': 'Partial',
        'top_off': 'Top-off',
        'ethanol_blend': 'Ethanol Blend',
        'custom_blend': 'Custom Blend %',
        'amount_to_add': 'Amount to Add (L)',
        'current_fuel': 'Current Fuel Level (L)',
        'volume_breakdown': 'VOLUME BREAKDOWN',
        'total_mix': 'Total Mix Volume',
        'gasoline_volume': 'Gasoline Volume',
        'ethanol_volume': 'Ethanol Volume',
        'cost_breakdown': 'COST BREAKDOWN',
        'total_cost': 'Total Cost',
        'gasoline_cost': 'Gasoline Cost',
        'ethanol_cost': 'Ethanol Cost',
        'performance': 'PERFORMANCE',
        'total_blend': 'Total Blend Mix',
        'gasoline_energy': 'Gasoline Energy',
        'range_impact': 'Range Impact'
    },
    'ar': {
        'title': 'حاسبة مزيج الإيثانول',
        'currency': 'العملة',
        'gas_price': 'سعر البنزين/لتر',
        'ethanol_price': 'سعر الإيثانول/لتر',
        'tank_capacity': 'سعة الخزان (لتر)',
        'fill_type': 'نوع التعبئة',
        'full_fill': 'تعبئة كاملة',
        'partial': 'تعبئة جزئية',
        'top_off': 'تعبئة علوية',
        'ethanol_blend': 'مزيج الإيثانول',
        'custom_blend': 'نسبة المزيج المخصص %',
        'amount_to_add': 'الكمية المراد إضافتها (لتر)',
        'current_fuel': 'مستوى الوقود الحالي (لتر)',
        'volume_breakdown': 'تفصيل الحجم',
        'total_mix': 'إجمالي حجم المزيج',
        'gasoline_volume': 'حجم البنزين',
        'ethanol_volume': 'حجم الإيثانول',
        'cost_breakdown': 'تفصيل التكلفة',
        'total_cost': 'التكلفة الإجمالية',
        'gasoline_cost': 'تكلفة البنزين',
        'ethanol_cost': 'تكلفة الإيثانول',
        'performance': 'الأداء',
        'total_blend': 'إجمالي المزيج',
        'gasoline_energy': 'طاقة البنزين',
        'range_impact': 'تأثير المدى'
    }
}

def get_common_currencies():
    return ['EGP', 'USD', 'EUR', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'JPY',
            'NZD', 'SGD', 'HKD', 'SEK', 'KRW', 'INR', 'BRL', 'ZAR']

def get_currency_symbol(currency_code):
    try:
        return babel.numbers.get_currency_symbol(currency_code)
    except:
        return currency_code + ' '

def get_ethanol_blend_options(lang):
    if lang == 'ar':
        return {
            "E0 (بنزين نقي)": 0,
            "E5 (قياسي)": 5,
            "E10 (شائع)": 10,
            "E15 (معتمد 2001+)": 15,
            "E20 (استخدام محدود)": 20,
            "E25 (معيار برازيلي)": 25,
            "E85 (وقود مرن)": 85,
            "مخصص": "Custom"
        }
    else:
        return {
            "E0 (Pure Gasoline)": 0,
            "E5 (Standard)": 5,
            "E10 (Common)": 10,
            "E15 (Approved 2001+)": 15,
            "E20 (Limited Use)": 20,
            "E25 (Brazil Std.)": 25,
            "E85 (Flex Fuel)": 85,
            "Custom": "Custom"
        }

def calculate_costs(total_volume, ethanol_percent, gas_price, ethanol_price):
    ethanol_volume = total_volume * (ethanol_percent / 100.0)
    gasoline_volume = total_volume - ethanol_volume
    ethanol_cost = ethanol_volume * ethanol_price
    gasoline_cost = gasoline_volume * gas_price
    total_cost = ethanol_cost + gasoline_cost
    return ethanol_volume, gasoline_volume, ethanol_cost, gasoline_cost, total_cost

def calculate_energy_content(ethanol_volume, gasoline_volume):
    gasoline_energy = gasoline_volume * 1.0
    ethanol_energy = ethanol_volume * 0.7
    total_energy = gasoline_energy + ethanol_energy
    return (total_energy / (ethanol_volume + gasoline_volume)) * 100

def get_rtl_css():
    return """
    body {
        direction: rtl;
    }
    .stSelectbox, .stNumberInput {
        text-align: right;
    }
    .metric-label, .metric-value, .section-label {
        text-align: right;
    }
    """

def get_base_css():
    return """
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .stSelectbox label, .stNumberInput label {
        color: #ffffff !important;
    }
    .results {
        background: linear-gradient(45deg, #2d2d2d, #363636);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        border: 1px solid #3498db22;
    }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }
    .column {
        display: flex;
        flex-direction: column;
    }
    .section-label {
        color: #3498db;
        font-size: 1rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
    }
    .metric-group {
        margin-bottom: 1.5rem;
    }
    .metric-label {
        color: #ffffff99;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        color: #3498db;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .lang-button {
        background-color: #2d2d2d;
        border: 1px solid #3498db;
        color: white;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
        margin: 0 5px;
        transition: background-color 0.3s;
    }
    .lang-button:hover {
        background-color: #3498db;
    }
    .lang-button.active {
        background-color: #3498db;
    }
    .language-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 20px;
        padding-top: 1rem;
    }
    """

def main():
    st.set_page_config(page_title="Ethanol Blend Calculator", layout="centered")

    # Initialize language in session state
    if 'language' not in st.session_state:
        st.session_state.language = 'en'

    # Add CSS
    st.markdown(f"<style>{get_base_css()}</style>", unsafe_allow_html=True)

    # Create two columns for the top bar - title and language selector
    lang_col1, lang_col2 = st.columns([3, 1])

    # Language selection buttons
    lang_buttons_html = f"""
        <div class="language-container">
            <button class="lang-button {'active' if st.session_state.language == 'en' else ''}"
                    onclick="window.location.href='?lang=en'">English</button>
            <button class="lang-button {'active' if st.session_state.language == 'ar' else ''}"
                    onclick="window.location.href='?lang=ar'">العربية</button>
        </div>
    """
    with lang_col2:
        st.markdown('<div class="language-container">', unsafe_allow_html=True)
        col_en, col_ar = st.columns(2)
        with col_en:
            if st.button("English", key="en_btn",
                        use_container_width=True,
                        type="primary" if st.session_state.language == 'en' else "secondary"):
                st.session_state.language = 'en'
                st.query_params['lang'] = 'en'
                st.rerun()

        with col_ar:
            if st.button("العربية", key="ar_btn",
                        use_container_width=True,
                        type="primary" if st.session_state.language == 'ar' else "secondary"):
                st.session_state.language = 'ar'
                st.query_params['lang'] = 'ar'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Get the language parameter from URL
    if 'lang' in st.query_params:
        st.session_state.language = st.query_params['lang']

    current_lang = st.session_state.language

    # Apply RTL styling for Arabic
    if current_lang == 'ar':
        st.markdown(f"<style>{get_rtl_css()}</style>", unsafe_allow_html=True)

    # Get translations for current language
    t = TRANSLATIONS[current_lang]

    with lang_col1:
        st.title(t['title'])

    # Input Section
    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        selected_currency = st.selectbox(t['currency'], get_common_currencies())
        currency_symbol = get_currency_symbol(selected_currency)

    with col2:
        gas_price = st.number_input(
            t['gas_price'],
            value=17.00 if selected_currency == 'EGP' else 1.50,
            step=1.0,
            format="%.2f"
        )

    with col3:
        ethanol_price = st.number_input(
            t['ethanol_price'],
            value=100.00 if selected_currency == 'EGP' else 1.20,
            step=1.0,
            format="%.2f"
        )

    col1, col2 = st.columns(2)
    with col1:
        tank_capacity = st.number_input(
            t['tank_capacity'],
            value=50.0,
            min_value=0.0,
            max_value=300.0,
            step=1.0
        )

        fill_options = [t['full_fill'], t['partial'], t['top_off']]
        fill_choice = st.selectbox(t['fill_type'], fill_options)

    with col2:
        blend_options = get_ethanol_blend_options(current_lang)
        chosen_blend = st.selectbox(
            t['ethanol_blend'],
            list(blend_options.keys())
        )

        if blend_options[chosen_blend] == "Custom" or blend_options[chosen_blend] == "مخصص":
            ethanol_percent = st.number_input(
                t['custom_blend'],
                min_value=0,
                max_value=85,
                value=10
            )
        else:
            ethanol_percent = blend_options[chosen_blend]

    # Calculate total volume based on fill type
    if fill_choice == t['full_fill']:
        total_volume = tank_capacity
    elif fill_choice == t['partial']:
        total_volume = st.number_input(
            t['amount_to_add'],
            min_value=0.0,
            max_value=tank_capacity,
            value=min(30.0, tank_capacity)
        )
    else:  # Top-off
        current_level = st.number_input(
            t['current_fuel'],
            min_value=0.0,
            max_value=tank_capacity,
            value=tank_capacity * 0.25
        )
        total_volume = tank_capacity - current_level

    # Calculations
    ethanol_volume, gasoline_volume, ethanol_cost, gasoline_cost, total_cost = calculate_costs(
        total_volume, ethanol_percent, gas_price, ethanol_price
    )
    relative_energy = calculate_energy_content(ethanol_volume, gasoline_volume)
    range_impact = 100 - relative_energy

    # Results Display
    results_html = f"""
    <div class="results">
        <div class="grid-container">
            <div class="column">
                <div class="section-label">{t['volume_breakdown']}</div>
                <div class="metric-group">
                    <div class="metric-label">{t['total_mix']}</div>
                    <div class="metric-value">{total_volume:.1f} L</div>
                </div>
                <div class="metric-group">
                    <div class="metric-label">{t['gasoline_volume']}</div>
                    <div class="metric-value">{gasoline_volume:.1f} L</div>
                </div>
                <div class="metric-group">
                    <div class="metric-label">{t['ethanol_volume']}</div>
                    <div class="metric-value">{ethanol_volume:.1f} L</div>
                </div>
            </div>
            <div class="column">
                <div class="section-label">{t['cost_breakdown']}</div>
                <div class="metric-group">
                    <div class="metric-label">{t['total_cost']}</div>
                    <div class="metric-value">{currency_symbol}{total_cost:.2f}</div>
                </div>
                <div class="metric-group">
                    <div class="metric-label">{t['gasoline_cost']}</div>
                    <div class="metric-value">{currency_symbol}{gasoline_cost:.2f}</div>
                </div>
                <div class="metric-group">
                    <div class="metric-label">{t['ethanol_cost']}</div>
                    <div class="metric-value">{currency_symbol}{ethanol_cost:.2f}</div>
                </div>
            </div>
            <div class="column">
                <div class="section-label">{t['performance']}</div>
                <div class="metric-group">
                    <div class="metric-label">{t['total_blend']}</div>
                    <div class="metric-value">E{ethanol_percent:.0f}</div>
                </div>
                <div class="metric-group">
                    <div class="metric-label">{t['gasoline_energy']}</div>
                    <div class="metric-value">{relative_energy:.1f}%</div>
                </div>
                <div class="metric-group">
                    <div class="metric-label">{t['range_impact']}</div>
                    <div class="metric-value">-{range_impact:.1f}%</div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(results_html, unsafe_allow_html=True)

    # Optional Tips Section
    if current_lang == 'ar':
        tips_title = "نصائح ومعلومات"
        safety_note = """
        ### ملاحظات السلامة:
        - تحقق دائمًا من الحد الأقصى للإيثانول الموصى به لسيارتك
        - أضف الإيثانول أولاً ثم البنزين
        - لا تتجاوز نسبة الخلط الموصى بها من الشركة المصنعة
        """
    else:
        tips_title = "Tips & Information"
        safety_note = """
        ### Safety Notes:
        - Always verify your vehicle's recommended maximum ethanol content
        - Add ethanol first, then gasoline
        - Don't exceed manufacturer's recommended blend ratio
        """

    with st.expander(tips_title):
        st.markdown(safety_note)

if __name__ == "__main__":
    main()
