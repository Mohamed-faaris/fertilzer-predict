"""
Reusable chart components using Matplotlib and Seaborn
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sys
sys.path.append('/home/faaris/projects/BDA/fert-predict')
from config.settings import COLOR_PALETTE
from src.utils.helpers import get_fertilizer_colors_list, get_soil_colors_list, get_crop_colors_list

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10


def create_pie_chart(data: pd.Series, title: str, colors: list = None):
    """
    Create a pie chart
    
    Args:
        data: Series with values
        title: Chart title
        colors: List of colors (optional)
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    if colors is None:
        colors = sns.color_palette("husl", len(data))
    
    wedges, texts, autotexts = ax.pie(
        data.values,
        labels=data.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        textprops={'fontsize': 11}
    )
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    return fig


def create_bar_chart(data: pd.Series, title: str, xlabel: str, ylabel: str, color: str = None):
    """
    Create a bar chart
    
    Args:
        data: Series with values
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        color: Bar color (optional)
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if color is None:
        color = COLOR_PALETTE['primary']
    
    bars = ax.bar(range(len(data)), data.values, color=color, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data.index, rotation=45, ha='right')
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9)
    
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    return fig


def create_horizontal_bar_chart(data: pd.Series, title: str, xlabel: str, ylabel: str, color: str = None):
    """Create a horizontal bar chart"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if color is None:
        color = COLOR_PALETTE['secondary']
    
    bars = ax.barh(range(len(data)), data.values, color=color, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(data.index)
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width)}',
                ha='left', va='center', fontsize=9, fontweight='bold')
    
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    
    return fig


def create_correlation_heatmap(corr_matrix: pd.DataFrame, title: str = "Correlation Heatmap"):
    """
    Create correlation heatmap
    
    Args:
        corr_matrix: Correlation matrix DataFrame
        title: Chart title
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8},
        ax=ax
    )
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    return fig


def create_box_plot(df: pd.DataFrame, column: str, group_by: str, title: str):
    """
    Create box plot
    
    Args:
        df: DataFrame
        column: Column to plot
        group_by: Column to group by
        title: Chart title
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create box plot
    df.boxplot(column=column, by=group_by, ax=ax, patch_artist=True,
               boxprops=dict(facecolor=COLOR_PALETTE['primary'], alpha=0.6),
               medianprops=dict(color='red', linewidth=2))
    
    ax.set_xlabel(group_by, fontsize=12, fontweight='bold')
    ax.set_ylabel(column, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    plt.suptitle('')  # Remove default title
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig


def create_scatter_plot(df: pd.DataFrame, x_col: str, y_col: str, title: str, hue: str = None):
    """
    Create scatter plot
    
    Args:
        df: DataFrame
        x_col: X-axis column
        y_col: Y-axis column
        title: Chart title
        hue: Column for color coding (optional)
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if hue:
        for category in df[hue].unique():
            subset = df[df[hue] == category]
            ax.scatter(subset[x_col], subset[y_col], label=category, alpha=0.6, s=50)
        ax.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        ax.scatter(df[x_col], df[y_col], alpha=0.6, s=50, color=COLOR_PALETTE['primary'])
    
    ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
    ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def create_distribution_plot(data: pd.Series, title: str, xlabel: str):
    """
    Create distribution plot (histogram + KDE)
    
    Args:
        data: Series with values
        title: Chart title
        xlabel: X-axis label
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Histogram
    ax.hist(data, bins=30, alpha=0.6, color=COLOR_PALETTE['primary'], edgecolor='black', density=True)
    
    # KDE
    data.plot(kind='kde', ax=ax, color=COLOR_PALETTE['danger'], linewidth=2)
    
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel('Density', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def create_grouped_bar_chart(df: pd.DataFrame, title: str, xlabel: str, ylabel: str):
    """
    Create grouped bar chart
    
    Args:
        df: DataFrame with multi-index or multiple columns
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    df.plot(kind='bar', ax=ax, width=0.8, edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(title='', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig
