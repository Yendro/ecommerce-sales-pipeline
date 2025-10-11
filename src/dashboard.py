import streamlit as streamlit_interface
import pandas as pandas_dataframe
import plotly.express as plotly_express
import warnings

# Note: Some fixings were made using DeepSeek

streamlit_interface.set_page_config(
    page_title="Amazon Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global Plotly settings to avoid warnings
# Note: Using obsolete keywords. ⚠️ Quick fix to warning messages using DeepSeek DeepThink.
plotly_config = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d']
}

def load_sales_data():
    try:
        sales_dataframe = pandas_dataframe.read_csv("data/standardized_sales.csv")
        return sales_dataframe
    except FileNotFoundError:
        streamlit_interface.error("❌ The standardized data file was not found. Run the ETL process first.")
        return None

def create_dashboard():
    streamlit_interface.title("Amazon Sales Analytics Dashboard")
    streamlit_interface.markdown("---")
    
    sales_dataframe = load_sales_data()
    if sales_dataframe is None:
        return

    streamlit_interface.sidebar.header("Analysis Filters")
    
    # Filter by category
    if 'category' in sales_dataframe.columns:
        available_categories = ['All Categories'] + sorted(sales_dataframe['category'].dropna().unique().tolist())
        selected_category = streamlit_interface.sidebar.selectbox("Select Category", available_categories)
        
        if selected_category != 'All Categories':
            sales_dataframe = sales_dataframe[sales_dataframe['category'] == selected_category]
    
    # Filter by rating range
    if 'rating' in sales_dataframe.columns:
        minimum_rating, maximum_rating = streamlit_interface.sidebar.slider(
            "Product Rating Range",
            min_value=0.0,
            max_value=5.0,
            value=(0.0, 5.0),
            step=0.1
        )
        sales_dataframe = sales_dataframe[(sales_dataframe['rating'] >= minimum_rating) & (sales_dataframe['rating'] <= maximum_rating)]
    
    # === KEY BUSINESS METRICS ===
    streamlit_interface.header("📈 Key Business Metrics")
    
    first_column, second_column, third_column, fourth_column = streamlit_interface.columns(4)
    
    with first_column:
        if 'discounted_price' in sales_dataframe.columns:
            total_revenue = sales_dataframe['discounted_price'].sum()
            streamlit_interface.metric("💰 Estimated Total Revenue", f"${total_revenue:,.0f}")
    
    with second_column:
        if 'profit_margin' in sales_dataframe.columns:
            average_profit_margin = sales_dataframe['profit_margin'].mean()
            streamlit_interface.metric("📊 Average Profit Margin", f"${average_profit_margin:.2f}")
    
    with third_column:
        if 'discount_percentage' in sales_dataframe.columns:
            average_discount_percentage = sales_dataframe['discount_percentage'].mean()
            streamlit_interface.metric("🎯 Average Discount Percentage", f"{average_discount_percentage:.1f}%")
    
    with fourth_column:
        if 'rating' in sales_dataframe.columns:
            average_rating = sales_dataframe['rating'].mean()
            streamlit_interface.metric("⭐ Average Product Rating", f"{average_rating:.2f}/5.0")
    
    streamlit_interface.markdown("---")
    
    # === MOST POPULAR PRODUCTS ===
    streamlit_interface.header("🏆 Top 10 Most Popular Products")

    if 'rating_count' in sales_dataframe.columns and 'product_name' in sales_dataframe.columns:
        top_products_dataframe = sales_dataframe.nlargest(10, 'rating_count')[['product_name', 'rating_count', 'discounted_price', 'rating']]
        
        top_products_chart = plotly_express.bar(
            top_products_dataframe,
            x='rating_count',
            y='product_name',
            orientation='h',
            title="Top 10 Products by Number of Ratings",
            labels={'rating_count': 'Ratings Count', 'product_name': 'Product Name'},
            color='rating',
            color_continuous_scale='viridis'
        )
        top_products_chart.update_layout(height=500)
        streamlit_interface.plotly_chart(top_products_chart, width='stretch', config=plotly_config)
    
    # === ANALYSIS BY CATEGORY ===
    streamlit_interface.header("📂 Distribution and Analysis by Category")
    
    left_column, right_column = streamlit_interface.columns(2)
    
    with left_column:
        if 'category' in sales_dataframe.columns:
            category_distribution = sales_dataframe['category'].value_counts().head(10)
            
            category_pie_chart = plotly_express.pie(
                values=category_distribution.values,
                names=category_distribution.index,
                title="Product Distribution by Category (Top 10)"
            )
            streamlit_interface.plotly_chart(category_pie_chart, width='stretch', config=plotly_config)
    
    with right_column:
        if 'category' in sales_dataframe.columns and 'discounted_price' in sales_dataframe.columns:
            category_revenue_distribution = sales_dataframe.groupby('category')['discounted_price'].sum().nlargest(10)
            
            revenue_by_category_chart = plotly_express.bar(
                x=category_revenue_distribution.values,
                y=category_revenue_distribution.index,
                orientation='h',
                title="Total Revenue by Category (Top 10)",
                labels={'x': 'Estimated Total Revenue', 'and': 'Product Category'}
            )
            streamlit_interface.plotly_chart(revenue_by_category_chart, width='stretch', config=plotly_config)
    
    # === PROFITABILITY ANALYSIS ===
    streamlit_interface.header("💹 Profitability and Margin Analysis")
    
    profitability_left_column, profitability_right_column = streamlit_interface.columns(2)
    
    with profitability_left_column:
        if 'profit_margin' in sales_dataframe.columns:
            profit_margin_distribution_chart = plotly_express.histogram(
                sales_dataframe,
                x='profit_margin',
                nbins=20,
                title="Profit Margin Distribution",
                labels={'profit_margin': 'Profit Margin by Product'}
            )
            streamlit_interface.plotly_chart(profit_margin_distribution_chart, width='stretch', config=plotly_config)
    
    with profitability_right_column:
        if 'rating' in sales_dataframe.columns and 'profit_margin' in sales_dataframe.columns:
            rating_profit_correlation_chart = plotly_express.scatter(
                sales_dataframe,
                x='rating',
                y='profit_margin',
                title="Relationship between Rating and Profit Margin",
                labels={'rating': 'Product Rating', 'profit_margin': 'Profit Margin'},
                trendline="ols"
            )
            streamlit_interface.plotly_chart(rating_profit_correlation_chart, width='stretch', config=plotly_config)
    
    # === DISCOUNT STRATEGY ANALYSIS ===
    streamlit_interface.header("🎪 Discount Strategy Analysis")
    
    discounts_left_column, discounts_right_column = streamlit_interface.columns(2)
    
    with discounts_left_column:
        if 'discount_percentage' in sales_dataframe.columns:
            discount_distribution_chart = plotly_express.histogram(
                sales_dataframe,
                x='discount_percentage',
                nbins=20,
                title="Distribution of Applied Discount Percentages",
                labels={'discount_percentage': 'Discount Percentage (%)'}
            )
            streamlit_interface.plotly_chart(discount_distribution_chart, width='stretch', config=plotly_config)
    
    with discounts_right_column:
        if 'discount_percentage' in sales_dataframe.columns and 'rating' in sales_dataframe.columns:
            # Fix: 'observed' parameter was removed to avoid warnings
            discount_ranges = pandas_dataframe.cut(sales_dataframe['discount_percentage'], bins=5)
            average_rating_by_discount_range = sales_dataframe.groupby(discount_ranges, observed=False)['rating'].mean()
            
            discount_rating_relationship_chart = plotly_express.bar(
                x=[str(range_label) for range_label in average_rating_by_discount_range.index],
                y=average_rating_by_discount_range.values,
                title="Average Rating by Discount Range",
                labels={'x': 'Discount Percentage Range', 'y': 'Average Grade'}
            )
            streamlit_interface.plotly_chart(discount_rating_relationship_chart, width='stretch', config=plotly_config)
    
    # === DETAILED PRODUCT TABLE ===
    streamlit_interface.header("📋 Product Details and Metrics")
    
    columns_to_display = []
    for column_name in ['product_name', 'category', 'discounted_price', 'actual_price', 
                'discount_percentage', 'rating', 'rating_count', 'profit_margin']:
        if column_name in sales_dataframe.columns:
            columns_to_display.append(column_name)
    
    if columns_to_display:
        streamlit_interface.markdown("**Showing the first 20 products:**")
        with streamlit_interface.container():
            styled_dataframe = sales_dataframe[columns_to_display].head(20).style.format({
                'discounted_price': '${:,.2f}',
                'actual_price': '${:,.2f}',
                'discount_percentage': '{:.1f}%',
                'rating': '{:.2f}',
                'profit_margin': '${:,.2f}'
            })
            
            streamlit_interface.dataframe(
                styled_dataframe,
                width='stretch',
                height=600
            )

        filtered_data_csv = sales_dataframe[columns_to_display].to_csv(index=False)
        streamlit_interface.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=filtered_data_csv,
            file_name="amazon_sales_analytics_filtered_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    # Note: Quick Fix using DeepSeek to Suppress Plotly-specific warnings
    warnings.filterwarnings("ignore", message="The keyword arguments have been deprecated")
    
    create_dashboard()